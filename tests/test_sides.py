"""Synthetic nations: team setup tests do not assume a political allegiance roster."""
import copy
import unittest
from rules.sides import default_setup, validate_setup, balanced_assignments, count_placed_nations


def roster():
    return [{"nation_id": f"{side}-{i}", "name": f"{side} nation {i}", "allegiance": side,
             "aliases": [f"{side} alias {i}"]}
            for side in ("axis", "allied", "neutral") for i in range(3)]


def team_setup(axis=1, allied=1):
    setup = default_setup(roster())
    setup["mode"] = "pass_and_play"
    for side, count in (("axis", axis), ("allied", allied)):
        setup["players"][side] = [{"player_id": f"{side}-{i}", "name": f"Player {side} {i}", "controller": "human"}
                                   for i in range(1, count + 1)]
    setup["assignments"] = balanced_assignments(setup["nations"], setup["players"], {})
    return setup


class SideSetupTests(unittest.TestCase):
    def test_local_chart_roster_caps_count_nations_not_inter_allied_pool(self):
        from game.nation_roster import initial_roster
        from rules.sides import max_team_size
        nations = initial_roster()
        self.assertEqual(max_team_size(nations, "axis"), 8)
        self.assertEqual(max_team_size(nations, "allied"), 10)
        self.assertEqual(validate_setup(default_setup(nations)), default_setup(nations))
        self.assertFalse(any(n["allegiance"] == "neutral" for n in nations))
    def test_default_one_player_per_side_and_neutral_unowned(self):
        setup = default_setup(roster())
        self.assertEqual(setup["mode"], "two_player")
        self.assertEqual(len(setup["players"]["axis"]), 1)
        self.assertEqual(len(setup["players"]["allied"]), 1)
        self.assertNotIn("neutral-0", setup["assignments"])
        self.assertEqual(validate_setup(setup), setup)

    def test_asymmetric_and_maximum_teams(self):
        for axis, allied in ((2, 1), (1, 3), (3, 3)):
            setup = team_setup(axis, allied)
            self.assertEqual(validate_setup(setup), setup)
        setup = team_setup(3, 3)
        setup["players"]["axis"].append({"player_id": "extra", "name": "Extra", "controller": "human"})
        with self.assertRaises(ValueError):
            validate_setup(setup)

    def test_balancing_counts_instances_and_does_not_split_nations(self):
        setup = team_setup(2, 1)
        counts = {"axis-0": 100, "axis-1": 60, "axis-2": 40}
        assignments = balanced_assignments(setup["nations"], setup["players"], counts)
        self.assertNotEqual(assignments["axis-0"], assignments["axis-1"])
        self.assertEqual(assignments["axis-1"], assignments["axis-2"])
        self.assertEqual(assignments, balanced_assignments(setup["nations"], setup["players"], counts))

    def test_verified_nationality_alias_counts_and_unknowns(self):
        units = {"one": {"type_id": "known"}, "two": {"type_id": "known"},
                 "three": {"type_id": "missing"}, "four": {"type_id": "draft"},
                 "five": {"type_id": "blank"}}
        definitions = {"known": {"review_status": "Verified", "nationality": "  AXIS ALIAS 0 "},
                       "draft": {"review_status": "In progress", "nationality": "axis alias 0"},
                       "blank": {"review_status": "Verified", "nationality": "Unknown"}}
        counts, unknown = count_placed_nations(units, definitions, roster())
        self.assertEqual(counts["axis-0"], 2)
        self.assertEqual(set(unknown), {"three", "four", "five"})

    def test_ai_and_two_player_modes_reject_multiplayer(self):
        setup = team_setup(2, 1)
        setup["mode"] = "two_player"
        with self.assertRaises(ValueError):
            validate_setup(setup)
        setup = default_setup(roster())
        setup["mode"] = "ai"
        setup["players"]["allied"][0]["controller"] = "ai"
        self.assertEqual(validate_setup(setup), setup)
        setup["players"]["axis"][0]["controller"] = "ai"
        with self.assertRaises(ValueError):
            validate_setup(setup)

    def test_reject_missing_cross_side_and_ambiguous_assignments(self):
        for change in (
            lambda s: s["assignments"].pop("axis-0"),
            lambda s: s["assignments"].update({"axis-0": "allied-1"}),
            lambda s: s["assignments"].update({"neutral-0": "axis-1"}),
            lambda s: s["nations"][0]["aliases"].append(s["nations"][1]["name"]),
        ):
            setup = default_setup(roster())
            change(setup)
            with self.assertRaises(ValueError):
                validate_setup(setup)

    def test_unknown_fields_and_inputs_are_preserved(self):
        setup = default_setup(roster())
        setup["future"] = {"keep": True}
        setup["nations"][0]["future"] = 42
        before = copy.deepcopy(setup)
        restored = validate_setup(setup)
        self.assertEqual(restored, before)
        restored["future"]["keep"] = False
        self.assertEqual(setup, before)
