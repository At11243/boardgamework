"""Campaign counter records, independent of catalog definitions and Qt graphics."""
def restore_units(records, canonical_key, hexes):
    if not isinstance(records, list):
        raise ValueError("Invalid campaign counters list.")
    units = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Invalid campaign counter record.")
        unit = record.copy()
        for field in ("unit_id", "type_id", "name", "image_path"):
            if not isinstance(unit.get(field), str) or not unit[field].strip():
                raise ValueError(f"Invalid counter {field}.")
        if unit["unit_id"] in units:
            raise ValueError("Duplicate counter instance ID.")
        key = unit.get("hex_key")
        if (not isinstance(key, (list, tuple)) or len(key) != 4
                or not all(isinstance(x, str) for x in key[:2])
                or any(type(x) is not int for x in key[2:])):
            raise ValueError("Invalid counter hex key.")
        key = canonical_key(key)
        if key not in hexes:
            raise ValueError("Counter hex is missing from the campaign save.")
        unit["hex_key"] = key
        unit.setdefault("active_face", "unassigned")
        if unit["active_face"] not in ("front", "back", "unassigned"):
            raise ValueError("Invalid counter active face.")
        unit.setdefault("stack_order", len(units))
        if type(unit["stack_order"]) is not int or unit["stack_order"] < 0:
            raise ValueError("Invalid counter stack order.")
        units[unit["unit_id"]] = unit
    return units


def stack_ids(units, key):
    return sorted((uid for uid, unit in units.items() if unit["hex_key"] == key),
                  key=lambda uid: (units[uid]["stack_order"], uid))
