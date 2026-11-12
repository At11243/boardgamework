"""Batch policy and persistence checks use temporary data only."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from counters.batch_review import prepare_batch, record_fingerprint, save_batch


class BatchReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "front.png").write_bytes(b"artwork fixture")
        self.current = {"format": "tsww-barbarossa-unit-definitions", "version": 1,
                        "future": {"keep": True}, "definitions": {"old": {"review_status": "Verified", "custom": 7}}}
        self.catalog = {"counter_types": {"new": {"image_paths": ["front.png"]}, "old": {}}}
        self.batch = {"format": "tsww-counter-review-batch", "version": 1,
                      "source": "Assistant visual review", "entries": [{
                          "type_id": "new", "definition": {"front_image": "front.png",
                              "back_appearance": "Blank color", "notes": "Keep note", "custom": 42},
                          "image_sha256": {"front.png": hashlib.sha256(b"artwork fixture").hexdigest()},
                          "review": {aspect: {"checked": True, "confidence": 0.99, "evidence": "Printed evidence checked"}
                                     for aspect in ("identity", "front", "back")}}]}

    def plan(self, issues=()):
        return prepare_batch(self.root, self.catalog, self.current, self.batch,
                             lambda uid, value: list(issues))

    def test_checked_artwork_and_complete_metadata_verify_without_mutating_inputs(self):
        snapshot = deepcopy((self.current, self.batch))
        result, report = self.plan()
        self.assertEqual(report["verified"], ["new"])
        self.assertEqual(result["definitions"]["new"]["review_status"], "Verified")
        self.assertEqual(result["definitions"]["new"]["custom"], 42)
        self.assertEqual(result["definitions"]["old"], self.current["definitions"]["old"])
        self.assertEqual((self.current, self.batch), snapshot)

    def test_completeness_alone_never_verifies(self):
        self.batch["entries"][0]["review"]["front"]["checked"] = "true"
        result, report = self.plan()
        self.assertIn("new", report["in_progress"])
        self.assertEqual(result["definitions"]["new"]["review_status"], "In progress")

    def test_missing_fingerprint_or_unresolved_issue_stays_draft(self):
        self.batch["entries"][0]["image_sha256"] = {}
        self.batch["entries"][0]["issues"] = ["Uncertain symbol"]
        result, report = self.plan(["Back appearance not reviewed"])
        self.assertEqual(len(report["in_progress"]["new"]), 3)
        self.assertIn("Uncertain symbol", result["definitions"]["new"]["notes"])

    def test_changed_artwork_aborts(self):
        (self.root / "front.png").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Artwork changed"):
            self.plan()

    def test_confidence_threshold_is_strict_and_not_a_probability_guarantee(self):
        for confidence in (0.95, 0.94, None, True, float("nan"), 1.1):
            self.batch["entries"][0]["review"]["front"]["confidence"] = confidence
            result, report = self.plan()
            self.assertIn("new", report["in_progress"])
            self.assertEqual(result["definitions"]["new"]["review_status"], "In progress")
        self.batch["entries"][0]["review"]["front"]["confidence"] = 0.96
        self.assertEqual(self.plan()[1]["verified"], ["new"])

    def test_existing_entries_are_never_overwritten(self):
        self.batch["entries"][0]["type_id"] = "old"
        result, report = self.plan()
        self.assertEqual(result, self.current)
        self.assertEqual(report["skipped_existing"], ["old"])

    def add_queue_placeholder(self):
        value = {"review_status": "In progress", "designation": "", "nationality": "Unknown",
                 "service": "Unknown", "unit_type": "Unknown", "unit_size": "Unknown",
                 "front_image": None, "back_image": None, "back_appearance": "Not yet reviewed",
                 "notes": "Imported name: fixture\nREVIEW QUEUE ONLY: generated\nMy own note\nBatch review issues: generated",
                 "future_data": {"keep": True}, "batch_review": {"review": {
                     aspect: {"checked": False} for aspect in ("identity", "front", "back")}}}
        self.current["definitions"]["new"] = value
        self.batch["entries"][0]["replace_placeholder_sha256"] = record_fingerprint(value)
        return value

    def test_opt_in_queue_promotion_preserves_unknown_fields_and_user_notes(self):
        self.add_queue_placeholder()
        result, report = self.plan()
        self.assertEqual(report["verified"], ["new"])
        value = result["definitions"]["new"]
        self.assertEqual(value["future_data"], {"keep": True})
        self.assertIn("My own note", value["notes"])
        self.assertNotIn("REVIEW QUEUE ONLY", value["notes"])
        self.assertEqual(value["front_image"], "front.png")

    def test_changed_or_manually_edited_queue_cannot_be_replaced(self):
        for field, changed in (("review_status", "Verified"), ("designation", "Manual unit"),
                               ("ground", {"front": {"combat_strength": "0"}}),
                               ("front_image", "front.png"), ("future_data", {"changed": True})):
            value = self.add_queue_placeholder()
            value[field] = changed
            with self.assertRaisesRegex(ValueError, "Queue entry changed"):
                self.plan()

    def test_duplicate_and_outside_paths_rejected(self):
        self.batch["entries"].append(deepcopy(self.batch["entries"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.plan()
        self.batch["entries"].pop()
        self.batch["entries"][0]["definition"]["front_image"] = "../outside.png"
        with self.assertRaisesRegex(ValueError, "outside project"):
            self.plan()

    def test_stale_save_rejected_and_exact_backup_retained(self):
        path = self.root / "unit_definitions.json"
        raw = json.dumps(self.current).encode()
        path.write_bytes(raw)
        result, _ = self.plan()
        save_batch(path, raw, result)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), result)
        backup = list((self.root / "unit_definition_backups").glob("*.json"))
        self.assertEqual(len(backup), 1)
        self.assertEqual(backup[0].read_bytes(), raw)
        with self.assertRaisesRegex(ValueError, "Definitions changed"):
            save_batch(path, raw, self.current)


if __name__ == "__main__":
    unittest.main()
