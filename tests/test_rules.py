"""Rule 2.C boundary cases; no campaign data or network required."""
import copy
import itertools
import unittest
from unittest.mock import Mock
from rules import DiceService, dice_value, roll_dice, validate_roll, attack_result_record, validate_attack_result


class DiceRulesTests(unittest.TestCase):
    def test_service_reuses_injected_generator_and_manual_entry_does_not_draw(self):
        generator = Mock()
        generator.randrange.side_effect = [0, 5, 2]
        service = DiceService(rng=generator)
        self.assertEqual(service.roll("1D10")["value"], 10)
        self.assertEqual(service.roll("1D10", manual_faces=[7])["value"], 7)
        self.assertEqual(service.roll("2D10", controller="ai")["value"], 7)
        self.assertEqual(generator.randrange.call_count, 3)
        with self.assertRaises(ValueError):
            service.roll("1D10", controller="ai", manual_faces=[3])
        self.assertEqual(generator.randrange.call_count, 3)

    def test_d10_all_faces(self):
        self.assertEqual([dice_value("1D10", [face]) for face in range(10)],
                         [10, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_two_dice_sum_and_percentile_are_distinct(self):
        self.assertEqual(dice_value("2D10", [0, 0]), 20)
        self.assertEqual(dice_value("2D10", [0, 5]), 15)
        self.assertEqual(dice_value("percentile", [0, 0]), 100)
        self.assertEqual(dice_value("percentile", [0, 5]), 5)
        self.assertEqual(dice_value("percentile", [5, 0]), 50)
        pairs = list(itertools.product(range(10), repeat=2))
        self.assertEqual(sorted(dice_value("percentile", pair) for pair in pairs), list(range(1, 101)))
        sums = [dice_value("2D10", pair) for pair in pairs]
        self.assertEqual((min(sums), max(sums)), (2, 20))
        self.assertEqual(sums.count(11), 10)

    def test_automatic_manual_and_ai(self):
        generator = Mock()
        generator.randrange.side_effect = [0, 9]
        auto = roll_dice("2D10", controller="ai", purpose="test", rng=generator)
        self.assertEqual(auto["faces"], [0, 9])
        self.assertEqual(auto["value"], 19)
        self.assertEqual(auto["method"], "automatic")
        self.assertEqual(generator.randrange.call_count, 2)
        generator.reset_mock()
        manual = roll_dice("percentile", manual_faces=[0, 0], rng=generator)
        generator.randrange.assert_not_called()
        self.assertEqual(manual["value"], 100)
        self.assertEqual(manual["method"], "manual")
        self.assertEqual(validate_roll(auto), auto)
        with self.assertRaises(ValueError):
            roll_dice("1D10", controller="ai", manual_faces=[5])

    def test_invalid_faces_and_unsupported_requests(self):
        for kind, faces in (("3D10", [1, 2, 3]), ("1D10", []), ("1D10", [10]),
                            ("1D10", [-1]), ("1D10", [True]), ("1D10", [1.5]),
                            ("2D10", [5]), ("percentile", [100]), ("1D10", ["0"])):
            with self.subTest(kind=kind, faces=faces), self.assertRaises(ValueError):
                dice_value(kind, faces)
        with self.assertRaises(ValueError):
            roll_dice("1D10", manual_faces="0")
        with self.assertRaises(ValueError):
            roll_dice("1D10", controller="unknown")

    def test_tampered_roll_rejected_and_unknown_fields_retained(self):
        record = roll_dice("1D10", manual_faces=[0])
        record["future"] = {"keep": True}
        checked = validate_roll(record)
        self.assertEqual(checked, record)
        checked["future"]["keep"] = False
        self.assertTrue(record["future"]["keep"])
        record["value"] = 0
        with self.assertRaises(ValueError):
            validate_roll(record)


class AttackRecordTests(unittest.TestCase):
    def test_attack_record_copies_participants_and_rolls(self):
        roll = roll_dice("1D10", manual_faces=[6], purpose="combat result")
        attackers = ["instance-a"]
        record = attack_result_record(attacker_ids=attackers, defender_ids=["instance-b"],
                                      target_hex=["Map 2", "region", 8, 45], result="DR",
                                      rolls=[roll], notes="Manually resolved")
        self.assertEqual(record["resolution"], "manual")
        self.assertEqual(validate_attack_result(record), record)
        attackers.append("another")
        roll["faces"][0] = 0
        self.assertEqual(record["attacker_ids"], ["instance-a"])
        self.assertEqual(record["rolls"][0]["faces"], [6])

    def test_attack_validation(self):
        valid = attack_result_record(attacker_ids=["a"], defender_ids=["b"],
                                     target_hex=["Map 2", "region", 8, 45], result="DR")
        for update in ({"attacker_ids": []}, {"defender_ids": ["a"]}, {"result": ""},
                       {"target_hex": ["bad"]}, {"resolution": "automatic"}):
            record = copy.deepcopy(valid)
            record.update(update)
            with self.subTest(update=update), self.assertRaises(ValueError):
                validate_attack_result(record)


if __name__ == "__main__":
    unittest.main()
