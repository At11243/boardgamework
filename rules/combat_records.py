"""Attack-result records for future AAR/combat integration; no combat resolution."""
from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4
from .dice import validate_roll


def attack_result_record(*, attacker_ids, defender_ids, target_hex, result, rolls=(), notes=""):
    """AAR scaffolding only: records a manual result, applies no combat effects.

    This schema is an application design, not implementation of Rule 10.
    Participants are stable campaign instance IDs, not catalog type IDs.
    """
    if any(not isinstance(ids, (list, tuple)) for ids in (attacker_ids, defender_ids, target_hex, rolls)):
        raise ValueError("Attack participants, target and rolls must be lists or tuples.")
    record = {"version": 1, "attack_id": uuid4().hex,
              "timestamp": datetime.now(timezone.utc).isoformat(),
              "attacker_ids": list(attacker_ids), "defender_ids": list(defender_ids),
              "target_hex": list(target_hex), "result": result, "notes": notes,
              "resolution": "manual", "rolls": [validate_roll(roll) for roll in rolls]}
    return validate_attack_result(record)


def validate_attack_result(record):
    if not isinstance(record, dict) or record.get("version") != 1:
        raise ValueError("Invalid attack result record.")
    for field in ("attack_id", "timestamp", "result"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"Attack {field} must be nonempty text.")
    for field in ("attacker_ids", "defender_ids"):
        ids = record.get(field)
        if (not isinstance(ids, list) or not ids
                or any(not isinstance(uid, str) or not uid.strip() for uid in ids)
                or len(set(ids)) != len(ids)):
            raise ValueError("Attack participants must be unique instance IDs on each side.")
    if set(record["attacker_ids"]) & set(record["defender_ids"]):
        raise ValueError("A counter cannot be on both sides of an attack.")
    key = record.get("target_hex")
    if (not isinstance(key, (list, tuple)) or len(key) != 4
            or any(not isinstance(value, str) or not value.strip() for value in key[:2])
            or any(type(value) is not int for value in key[2:])):
        raise ValueError("Invalid attack target hex.")
    if (record.get("resolution") != "manual" or not isinstance(record.get("notes"), str)
            or not isinstance(record.get("rolls"), list)):
        raise ValueError("Invalid manual attack result.")
    for roll in record["rolls"]:
        validate_roll(roll)
    return deepcopy(record)
