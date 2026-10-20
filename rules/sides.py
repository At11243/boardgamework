"""Sides and local team setup, grounded in v1.6a 2.D-F (pp8-9 / PDF pp10-11).

Team sizes and balancing are user-requested setup policy, not historical
allegiance rules. No roster, declaration of war or defection is inferred here.
"""
from copy import deepcopy

SIDES = ("axis", "allied")
ALLEGIANCES = SIDES + ("neutral",)
MODES = ("two_player", "pass_and_play", "online", "pbem", "ai")


def default_setup(nations=()):
    nations = list(nations)
    setup = {"version": 1, "mode": "two_player", "ai_side": "allied",
             "nations": deepcopy(list(nations)),
             "players": {side: [{"player_id": f"{side}-1", "name": f"{side.title()} player 1",
                                  "controller": "human"}] for side in SIDES},
             "assignments": {nation["nation_id"]: f"{nation['allegiance']}-1"
                             for nation in nations if nation["allegiance"] in SIDES}}
    return validate_setup(setup)


def nationality_key(value):
    return " ".join(value.casefold().split())


def nations_by_side(setup):
    """Separate side/neutral lists without conflating allegiance and ownership."""
    validate_roster(setup["nations"])
    return {side: deepcopy([nation for nation in setup["nations"] if nation["allegiance"] == side])
            for side in ALLEGIANCES}


def max_team_size(nations, side):
    """Inter-Allied control pools do not increase the maximum nation/player count."""
    return max(1, sum(n["allegiance"] == side and n.get("kind", "nation") == "nation" for n in nations))


def validate_roster(nations):
    if not isinstance(nations, list):
        raise ValueError("Nation roster must be a list.")
    ids, labels = set(), {}
    for nation in nations:
        if not isinstance(nation, dict):
            raise ValueError("Invalid nation entry.")
        for field in ("nation_id", "name"):
            if not isinstance(nation.get(field), str) or not nation[field].strip():
                raise ValueError(f"Nation {field} must be nonempty text.")
        uid = nation["nation_id"]
        if uid in ids or nation.get("allegiance") not in ALLEGIANCES:
            raise ValueError("Nation IDs must be unique and allegiance must be Axis, Allied or neutral.")
        ids.add(uid)
        if nation.get("kind", "nation") not in ("nation", "control_group"):
            raise ValueError("Invalid nation/control-group kind.")
        aliases = nation.get("aliases", [])
        if not isinstance(aliases, list) or any(not isinstance(x, str) or not x.strip() for x in aliases):
            raise ValueError("Nation aliases must be nonempty text.")
        for label in [nation["name"], *aliases]:
            key = nationality_key(label)
            if key in labels and labels[key] != uid:
                raise ValueError(f"Ambiguous nationality label: {label}.")
            labels[key] = uid
    return labels


def validate_setup(setup):
    if not isinstance(setup, dict) or setup.get("version") != 1 or setup.get("mode") not in MODES:
        raise ValueError("Invalid player setup.")
    validate_roster(setup.get("nations"))
    if setup.get("ai_side") not in SIDES:
        raise ValueError("Select which side the AI controls.")
    players, assignments = setup.get("players"), setup.get("assignments")
    if not isinstance(players, dict) or set(players) != set(SIDES) or not isinstance(assignments, dict):
        raise ValueError("Invalid players or nation assignments.")
    all_ids = set()
    for side in SIDES:
        team = players[side]
        if not isinstance(team, list) or not 1 <= len(team) <= max_team_size(setup["nations"], side):
            raise ValueError(f"{side.title()} player count cannot exceed its number of nations.")
        if setup["mode"] in ("two_player", "ai") and len(team) != 1:
            raise ValueError("Two-player and AI games require 1 x 1 teams.")
        for player in team:
            if not isinstance(player, dict):
                raise ValueError("Invalid player record.")
            for field in ("player_id", "name"):
                if not isinstance(player.get(field), str) or not player[field].strip():
                    raise ValueError("Player IDs and names must be nonempty text.")
            if player["player_id"] in all_ids:
                raise ValueError("Player IDs must be unique across both sides.")
            all_ids.add(player["player_id"])
            expected = "ai" if setup["mode"] == "ai" and setup["ai_side"] == side else "human"
            if player.get("controller") != expected:
                raise ValueError("Player controller does not match the selected play mode.")
    active = {n["nation_id"]: n for n in setup["nations"] if n["allegiance"] in SIDES}
    if set(assignments) != set(active):
        raise ValueError("Assign every non-neutral nation exactly once; neutral nations stay unassigned.")
    for uid, nation in active.items():
        allowed = {p["player_id"] for p in players[nation["allegiance"]]}
        if not isinstance(assignments[uid], str) or assignments[uid] not in allowed:
            raise ValueError(f"{nation['name']} must be assigned to a player on its own side.")
    for side in SIDES:
        if len(players[side]) > 1 and any(p["player_id"] not in assignments.values() for p in players[side]):
            raise ValueError("Every team player must control at least one nation.")
    return deepcopy(setup)


def count_placed_nations(units, definitions, nations):
    """Count instances, not catalog types; require reviewed metadata and exact aliases."""
    labels = validate_roster(nations)
    counts = {nation["nation_id"]: 0 for nation in nations}
    unknown = {}
    for uid, unit in units.items():
        definition = definitions.get(unit["type_id"], {})
        if not isinstance(definition, dict) or definition.get("review_status") != "Verified":
            unknown[uid] = "Definition not Verified"
            continue
        nationality = definition.get("nationality")
        key = nationality_key(nationality) if isinstance(nationality, str) else ""
        if not key or key not in labels:
            unknown[uid] = f"Unknown or unmatched nationality: {nationality or '(blank)'}"
            continue
        counts[labels[key]] += 1
    return counts, unknown


def balanced_assignments(nations, players, counts):
    """Greedy whole-nation balancing; deterministic, approximate, never splits a nation."""
    validate_roster(nations)
    result = {}
    for side in SIDES:
        team = players.get(side, [])
        active = [nation for nation in nations if nation["allegiance"] == side]
        if not team or len(team) > max_team_size(nations, side):
            raise ValueError("Player count cannot exceed the number of nations on that side.")
        loads = {player["player_id"]: [0, 0] for player in team}
        if len(loads) != len(team):
            raise ValueError("Duplicate player IDs.")
        for nation in active:
            weight = counts.get(nation["nation_id"], 0)
            if type(weight) is not int or weight < 0:
                raise ValueError("Counter counts must be nonnegative integers.")
        for nation in sorted(active, key=lambda n: (-counts.get(n["nation_id"], 0), n["nation_id"])):
            # Empty-player priority guarantees at least one nation per player,
            # including when some nations have zero placed counters.
            uid = min(loads, key=lambda pid: (loads[pid][1] != 0, loads[pid][0], loads[pid][1], pid))
            result[nation["nation_id"]] = uid
            loads[uid][0] += counts.get(nation["nation_id"], 0)
            loads[uid][1] += 1
    return result
