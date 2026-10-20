"""Versioned counter actions with complete instance snapshots and a replay cursor."""
from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4
from counters.counter_state import restore_units
from rules import validate_roll, validate_attack_result

COUNTER_ACTIONS = ("place", "flip", "move")
EVENT_ACTIONS = ("dice_roll", "attack_result")


def empty_history():
    return {"version": 1, "entries": [], "cursor": 0}


def append_action(history, kind, before, after, description):
    if before == after:
        return
    entry = {"action_id": uuid4().hex, "timestamp": datetime.now(timezone.utc).isoformat(),
             "kind": kind, "unit_id": (after or before)["unit_id"],
             "description": description, "before": deepcopy(before), "after": deepcopy(after)}
    # A new action after Undo replaces the abandoned redo branch.
    history["entries"][history["cursor"]:] = [entry]
    history["cursor"] += 1


def append_event(history, kind, payload, description):
    validator = {"dice_roll": validate_roll, "attack_result": validate_attack_result}.get(kind)
    if validator is None:
        raise ValueError("Unsupported history event.")
    entry = {"action_id": uuid4().hex, "timestamp": datetime.now(timezone.utc).isoformat(),
             "kind": kind, "description": description, "payload": validator(payload),
             "before": None, "after": None}
    history["entries"][history["cursor"]:] = [entry]
    history["cursor"] += 1


def restore_history(saved, units, canonical_key, hexes):
    if saved is None:
        return empty_history()
    if (not isinstance(saved, dict) or saved.get("version") != 1
            or not isinstance(saved.get("entries"), list)
            or type(saved.get("cursor")) is not int
            or not 0 <= saved["cursor"] <= len(saved["entries"])):
        raise ValueError("Invalid campaign action history.")
    history = deepcopy(saved)
    ids = set()
    for entry in history["entries"]:
        if not isinstance(entry, dict) or entry.get("kind") not in COUNTER_ACTIONS + EVENT_ACTIONS:
            raise ValueError("Invalid history action.")
        for field in ("action_id", "timestamp", "description"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError(f"Invalid history {field}.")
        if entry["action_id"] in ids:
            raise ValueError("Duplicate history action ID.")
        ids.add(entry["action_id"])
        if entry["kind"] in EVENT_ACTIONS:
            if entry.get("before", "missing") is not None or entry.get("after", "missing") is not None:
                raise ValueError("Result-only history events cannot change counters.")
            validator = validate_roll if entry["kind"] == "dice_roll" else validate_attack_result
            entry["payload"] = validator(entry.get("payload"))
            if entry["kind"] == "attack_result":
                key = canonical_key(entry["payload"]["target_hex"])
                if key not in hexes:
                    raise ValueError("History attack target is missing from campaign.")
                entry["payload"]["target_hex"] = list(key)
            continue
        if not isinstance(entry.get("unit_id"), str) or not entry["unit_id"].strip():
            raise ValueError("Invalid history unit_id.")
        for field in ("before", "after"):
            if field not in entry:
                raise ValueError("History action is missing its snapshots.")
            value = entry[field]
            if value is not None:
                restored = restore_units([value], canonical_key, hexes)
                if entry["unit_id"] not in restored:
                    raise ValueError("History snapshot instance ID mismatch.")
                entry[field] = restored[entry["unit_id"]]
        if (entry["after"] is None or (entry["kind"] == "place") != (entry["before"] is None)
                or entry["before"] == entry["after"]):
            raise ValueError("Invalid action snapshots.")

    # Derive the starting state, then replay the entire chain, including redo.
    state = deepcopy(units)
    for entry in reversed(history["entries"][:history["cursor"]]):
        if entry["kind"] in EVENT_ACTIONS:
            continue
        uid = entry["unit_id"]
        if state.get(uid) != entry["after"]:
            raise ValueError("History does not match saved counter state.")
        if entry["before"] is None:
            state.pop(uid)
        else:
            state[uid] = deepcopy(entry["before"])
    for index, entry in enumerate(history["entries"]):
        if entry["kind"] in EVENT_ACTIONS:
            continue
        uid = entry["unit_id"]
        if state.get(uid) != entry["before"]:
            raise ValueError("Inconsistent history action sequence.")
        state[uid] = deepcopy(entry["after"])
        if index + 1 == history["cursor"] and state != units:
            raise ValueError("History cursor does not match campaign state.")
    return history
