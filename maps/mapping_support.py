from copy import deepcopy 

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPolygonF

from maps.campaign_layout import barbarossa_boards 
from maps.campaign_grid_definitions import barbarossa_grids
from maps.hex_model import (
    nearest_hex, 
    hex_vertices, 
    nearest_hexside, 
    is_playable_hex,
    printed_hex_number, 
)

shared_fields = (
    "waterway",
    "navigation",
    "border",
    "escarpment",
    "coastal_cliff",
    "high_mountain", 
    "reflief",
    "navigable_strait",
    "higher_ground",
)

def merge_records(left, right, location):
    """Combine matching records without discarding conflicting values."""



    result = deepcopy(left)

    for field, value in right.items():
        if field not in result or result[field] == value:
            result[field] = deepcopy(value)

        elif (
            isinstance(result[field], dict)
            and isinstance(value, dict)
        ):
            result[field] = merge_records(
                result[field],
                value,
                f"{location}/{field}",
            )

        elif result[field] is None or result[field] == "Unknown":
            result[field] = deepcopy(value)

        elif value is not None and value != "Unknown":
            raise ValueError(
                f"Conflicting saved information at {location}/{field}."
                "No data was discarded."
            )

    return result

def normalize_campaign(view, records):
    normalized = {}

    for old_key, values in records.items():
        key = view.canonical_hex_key(old_key)
        board, name, column, row = key

        region = next(
            region 
            for region in barbarossa_grids[board]["regions"]
            if region["name"] == name
        )

        grid, x, y = view.hex_key_geometry(key)
        number = printed_hex_number(region, column, row)

        updated = deepcopy(values)
        updated.update({
            "board_id": board,
            "region": name,
            "column": column,
            "row": row,
            "printed_number": number,
            "game_reference": f"{name}:{number}",
            "center": (x, y),
        })

        normalized[key] = merge_records(
            normalized.get(key, {}),
            updated,
            str(key)
        )

    return normalized 

def neighbor_side(view, key, side):
    """Return the neighboring key and its matching side, or None."""


    key = view.canonical_hex_key(key)
    grid, x, y = view.hex_key_geometry(key)

    vertices = hex_vertices(grid, x, y)
    start = vertices[side]
    end = vertices[(side + 1) % 6]

    target_x = start[0] + end[0] - x 
    target_y = start[1] + end[1] - y

    candidates = {}

    for (
        board, filename, origin_x, origin_y, width, height
    ) in barbarossa_boards:
        image_x = target_x - origin_x 
        image_y = target_y - origin_y

        if not (
            0 <= image_x < width
            and 0 <= image_y < height
        ):
            continue 

        for region in barbarossa_grids[board]["regions"]:
            column, row, center_x, center_y = nearest_hex(
                region["grid"], image_x, image_y
            )

            if not is_playable_hex(
                board, region["name"], column, row
            ):
                continue 

            tolerance = min(
                grid["dx"],
                grid["dy"],
                region["grid"]["dx"],
                region["grid"]["dy"],
            ) * 0.05

            if (
                (center_x - image_x) ** 2 
                + (center_y - image_y) ** 2 
            ) > tolerance ** 2 :
                continue

            boundary = QPolygonF([
                QPointF(px, py)
                for px, py in region["boundary"]
            ])

            if not boundary.containsPoint(
                QPointF(center_x, center_y),
                Qt.FillRule.OddEvenFill,
            ):
                continue 

            other_key = view.canonical_hex_key(
                (board, region["name"], column, row)
            )

            if other_key == key:
                continue 

            other_grid, neighbor_x, neighbor_y = (
                view.hex_key_geometry(other_key)
            )

            opposite, other_start, other_end = nearest_hexside(
                other_grid,
                neighbor_x,
                neighbor_y,
                x,
                y,
            )

            center_error = (
                (neighbor_x - target_x) ** 2 
                + (neighbor_y - target_y) ** 2
            )

            edge_error = (
                (
                    start[0] + end[0]
                    - other_start[0] - other_end[0]
                ) / 2
            ) ** 2 + (
                (
                    start[1] + end[1]
                    - other_start[1] - other_end[1]
                ) / 2
            ) ** 2

            if max(center_error, edge_error) <= tolerance ** 2:
                candidates[(other_key, opposite)] = center_error

    if not candidates:
        return None 

    return min(
        candidates,
        key=lambda item: (candidates[item], item),
    )

def opposite_value(field, value):
    if field == "higher_ground":
        return {
            "This hex": "Neighbor hex",
            "Neighbor hex": "This hex",
        }.get(value, value)

    return value 

def synchronize_sides(view, definitions, key, previous):
    """Copy changed shared features onto the neighboring side."""

    result = deepcopy(definitions)
    current = result[key].get("hexsides", {})

    for side_text, values in current.items():
        neighbor = neighbor_side(view, key, int(side_text))

        print(
            f"Shared edge: {key}, side {side_text} -> {neighbor}",
            flush = True,
        )

        if neighbor is None:
            continue

        other_key, other_side = neighbor 

        other_values = (
            result.get(other_key, {})
            .get("hexsides", {})
            .get(str(other_side), {})
        )

        old_values = (
            previous.get("hexsides", {})
            .get(side_text, {})
        )

        changes = {}

        for field in shared_fields:
            value = values.get(field, "Unknown")

            changed = value != old_values.get(field, "Unknown")
            missing = other_values.get(field, "Unknown") == "Unknown"

            if changed or (missing and value != "Unknown"):
                changes[field] = opposite_value(field, value)

        if changes:
            target = result.setdefault(other_key, {})
            sides = target.setdefault("hexsides", {})
            target_side = sides.setdefault(str(other_side), {})

            for field in shared_fields + ("fortification",):
                target_side.setdefault(field, "Unknown")

            target_side.update(changes)

    return result

def audit_sides(view):
    """Report mismatches without changing saved information."""

    messages = []
    checked = set()

    for key, properties in view.map_definitions.items():
        for side_text, values in properties.get("hexsides", {}).items():
            if all(
                values.get(field, "Unknown") == "Unknown"
                for field in shared_fields
            ):
                continue 

            neighbor = neighbor_side(view, key, int(side_text))

            if neighbor is None:
                continue 

            other_key, other_side = neighbor 

            pair = tuple(sorted((
                (key, int(side_text)),
                (other_key, other_side),
            )))

            if pair in checked:
                continue 

            checked.add(pair)

            other_values = (
                view.map_definitions.get(other_key, {})
                .get("hexsides", {})
                .get(str(other_side), {})
            )

            for field in shared_fields:
                first = values.get(field, "Unknown")
                second = opposite_value(
                    field, 
                    other_values.get(field, "Unknown"),
                )

                if first != second:
                    messages.append(
                        f"{key} side {side_text} / "
                        f"{other_key} side {other_side}: "
                        f"{field}: {first} vs {second}" 
                    )
    return messages 




