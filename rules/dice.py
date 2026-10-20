"""UI-independent TSWW rules foundations.

Dice: v1.6a Rule 2.C.1, printed p8 / PDF p10.
Rounding: Rule 2.A and 2.C.2 on the same page retain fractions unless the
specific mechanic says otherwise. No generic rounding is applied here.
"""
from copy import deepcopy
from datetime import datetime, timezone
from random import SystemRandom
from uuid import uuid4

ROLL_TYPES = ("1D10", "2D10", "percentile")
DICE_SOURCE = {"edition": "1.6a", "rule": "2.C.1", "printed_page": 8, "pdf_page": 10}


def dice_value(roll_type, faces):
    """Faces are physical digits 0..9; percentile order is tens, then ones.

    2D10 here explicitly means the SUM of two D10s, not a percentile roll.
    Callers must choose percentile when a mechanic asks for a percentage.
    """
    if roll_type not in ROLL_TYPES:
        raise ValueError("Choose 1D10, 2D10 (sum), or percentile.")
    count = 1 if roll_type == "1D10" else 2
    if (not isinstance(faces, (list, tuple)) or len(faces) != count
            or any(type(face) is not int or not 0 <= face <= 9 for face in faces)):
        raise ValueError(f"Enter {count} die digit(s), each from 0 to 9.")
    if roll_type == "percentile":
        return faces[0] * 10 + faces[1] or 100
    return sum(face or 10 for face in faces)


class DiceService:
    """Roll dice using one injectable random source; no UI or campaign state."""

    def __init__(self, rng=None):
        self._rng = rng if rng is not None else SystemRandom()

    def roll(self, roll_type, *, controller="human", manual_faces=None, purpose=""):
        """Return a JSON-ready immutable-by-convention result; AI cannot supply dice.

        An injectable randrange source is for deterministic tests. Production uses
        SystemRandom. Presentation/animation consumes the result, never rerolls it.
        """
        if controller not in ("human", "ai"):
            raise ValueError("Controller must be human or ai.")
        if roll_type not in ROLL_TYPES:
            raise ValueError("Unsupported dice request.")
        if not isinstance(purpose, str):
            raise ValueError("Roll purpose must be text.")
        if controller == "ai" and manual_faces is not None:
            raise ValueError("AI rolls must be automatic.")
        if manual_faces is not None and not isinstance(manual_faces, (list, tuple)):
            raise ValueError("Manual dice must be a list of die digits.")
        count = 1 if roll_type == "1D10" else 2
        generator = self._rng
        faces = ([generator.randrange(10) for _ in range(count)]
                 if manual_faces is None else list(manual_faces))
        return {"version": 1, "roll_id": uuid4().hex,
                "timestamp": datetime.now(timezone.utc).isoformat(), "roll_type": roll_type,
                "controller": controller, "method": "automatic" if manual_faces is None else "manual",
                "faces": faces, "value": dice_value(roll_type, faces), "purpose": purpose.strip(),
                "source": DICE_SOURCE.copy()}


def roll_dice(roll_type, *, controller="human", manual_faces=None, purpose="", rng=None):
    """Convenience entry point retained for callers of the original rules module."""
    return DiceService(rng=rng).roll(roll_type, controller=controller,
                                     manual_faces=manual_faces, purpose=purpose)


def validate_roll(record):
    if not isinstance(record, dict) or record.get("version") != 1:
        raise ValueError("Invalid recorded dice roll.")
    for field in ("roll_id", "timestamp"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"Invalid dice {field}.")
    if (record.get("controller") not in ("human", "ai")
            or record.get("method") not in ("automatic", "manual")
            or (record["controller"] == "ai" and record["method"] != "automatic")
            or not isinstance(record.get("purpose"), str)):
        raise ValueError("Invalid recorded roll method/controller/purpose.")
    if (type(record.get("value")) is not int
            or record["value"] != dice_value(record.get("roll_type"), record.get("faces"))):
        raise ValueError("Recorded dice value does not match the dice.")
    source = record.get("source")
    if not isinstance(source, dict) or any(source.get(key) != value for key, value in DICE_SOURCE.items()):
        raise ValueError("Recorded dice roll is missing its governing rule reference.")
    return deepcopy(record)


