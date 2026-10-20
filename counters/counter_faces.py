"""Reviewed face assignments and rendering; no gameplay effects are inferred."""
import json
import re
from PySide6.QtGui import QColor, QPixmap


def face_pixmap(unit, root):
    assignment = unit.get("face_assignment")
    if assignment is not None:
        validate_assignment(assignment)
    if unit.get("active_face") == "back" and assignment is not None:
        if assignment["back_appearance"] == "Blank color":
            front = read_image(root, assignment["front_image"])
            blank = QPixmap(front.size())
            blank.fill(QColor(assignment["blank_back_color"]))
            return blank
    return read_image(root, unit["image_path"])


def read_image(root, path):
    if not isinstance(path, str) or not path.strip():
        raise ValueError("A required face image has not been assigned.")
    pixmap = QPixmap(str(root / path))
    if pixmap.isNull():
        raise ValueError(f"Cannot load counter image: {path}")
    return pixmap


def validate_assignment(assignment):
    if not isinstance(assignment, dict):
        raise ValueError("Invalid saved face assignment.")
    if not isinstance(assignment.get("front_image"), str) or not assignment["front_image"].strip():
        raise ValueError("Front image has not been assigned.")
    appearance = assignment.get("back_appearance")
    if appearance == "Printed image":
        if not isinstance(assignment.get("back_image"), str) or not assignment["back_image"].strip():
            raise ValueError("Back image has not been assigned.")
        if assignment["front_image"] == assignment["back_image"]:
            raise ValueError("Front and back use the same image; review the definition.")
    elif appearance == "Blank color":
        color = assignment.get("blank_back_color")
        if not isinstance(color, str) or re.fullmatch(r"#[0-9a-fA-F]{6}", color) is None:
            raise ValueError("Blank reverse needs a valid stored color.")
    else:
        raise ValueError("Back appearance has not been reviewed.")


def flipped_instance(unit, root):
    """Return a new record and pixmap; leave the current instance untouched on failure."""
    assignment = unit.get("face_assignment")
    if assignment is None:
        path = root / "assets" / "counters" / "unit_definitions.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise ValueError("Cannot read unit definitions; review the definition in Unit Editor.") from error
        if (not isinstance(data, dict)
                or data.get("format") != "tsww-barbarossa-unit-definitions"
                or data.get("version") != 1
                or not isinstance(data.get("definitions"), dict)):
            raise ValueError("Invalid unit definitions file.")
        definition = data["definitions"].get(unit["type_id"])
        if not isinstance(definition, dict) or definition.get("review_status") != "Verified":
            raise ValueError("Flipping requires a Verified definition with reviewed face assignments.")
        assignment = {field: definition.get(field) for field in (
            "front_image", "back_image", "back_appearance", "blank_back_color"
        )}
    validate_assignment(assignment)
    read_image(root, assignment["front_image"])
    if assignment["back_appearance"] == "Printed image":
        read_image(root, assignment["back_image"])
    face = unit.get("active_face", "unassigned")
    if face == "unassigned":
        current = (root / unit["image_path"]).resolve()
        matches = [name for name in ("front", "back")
                   if isinstance(assignment.get(f"{name}_image"), str)
                   and (name != "back" or assignment["back_appearance"] == "Printed image")
                   and (root / assignment[f"{name}_image"]).resolve() == current]
        if len(matches) != 1:
            raise ValueError("The placed image does not identify one reviewed face; review its assignment.")
        face = matches[0]
    updated = unit.copy()
    updated["face_assignment"] = assignment.copy()
    updated["active_face"] = "back" if face == "front" else "front"
    updated["image_path"] = (assignment["back_image"]
                             if updated["active_face"] == "back"
                             and assignment["back_appearance"] == "Printed image"
                             else assignment["front_image"])
    return updated, face_pixmap(updated, root)
