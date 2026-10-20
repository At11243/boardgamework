"""Temporary-fixture tests: never load or save the user's real definitions."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap
from counters import unit_editor


class UnitEditorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.directory = self.root / "assets" / "counters"
        self.directory.mkdir(parents=True)
        image = QPixmap(10, 10)
        image.fill()
        image.save(str(self.root / "front.png"))
        image.save(str(self.root / "back.png"))
        self.path = self.directory / "unit_definitions.json"
        self.original = {
            "format": "tsww-barbarossa-unit-definitions", "version": 1,
            "future_metadata": {"keep": True},
            "definitions": {"one": {
                "designation": "Test", "counter_category": "Ground unit",
                "nationality": "German", "service": "Army",
                "unit_type": "Infantry", "unit_size": "Division",
                "front_image": "front.png", "back_image": "back.png",
                "back_appearance": "Printed image", "review_status": "Verified",
                "future_field": 42,
                "ground": {"format": "Combined combat strength / movement",
                           "front": {"combat_strength": "0", "movement": "N/A", "future": 7},
                           "back": {"combat_strength": "6", "movement": "6"}},
            }, "other": {"notes": "untouched"}},
        }
        self.path.write_text(json.dumps(self.original), encoding="utf-8")
        (self.directory / "counter_catalog.json").write_text(json.dumps({
            "format": "tsww-barbarossa-counter-catalog", "version": 1,
            "counter_types": {"one": {"name": "Test", "palette": [],
                "image_names": ["front.png", "back.png"],
                "image_paths": ["front.png", "back.png"]}},
        }), encoding="utf-8")
        self.patcher = patch.object(unit_editor, "project_dir", self.root)
        self.patcher.start()
        self.editor = unit_editor.UnitEditor()

    def tearDown(self):
        self.editor.dirty = False
        self.editor.close()
        self.patcher.stop()
        self.temp.cleanup()

    def test_open_legacy_and_round_trip(self):
        before = self.path.read_bytes()
        self.assertEqual(self.editor.review_status.currentText(), "Verified")
        self.assertFalse(self.editor.dirty)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.editor.definition_issues(), [])
        for choice in self.editor.ground_formats.values():
            self.assertEqual(choice.currentText(), "Combined combat strength / movement")
        self.assertTrue(self.editor.save_definition())
        saved = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(saved["future_metadata"], {"keep": True})
        self.assertEqual(saved["definitions"]["other"], {"notes": "untouched"})
        one = saved["definitions"]["one"]
        self.assertEqual(one["future_field"], 42)
        self.assertEqual(one["ground"]["front"]["future"], 7)
        self.assertEqual(one["ground"]["front"]["combat_strength"], "0")
        self.assertEqual(one["ground"]["front"]["movement"], "N/A")
        backups = list((self.directory / "unit_definition_backups").glob("*.json"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), before)
        self.editor.load_definitions()
        self.assertEqual(self.editor.unit_definitions, saved["definitions"])

    def add_second_counter(self):
        self.editor.browser.counter_types["two"] = {
            "name": "Second counter", "palette": [],
            "image_names": ["front.png", "back.png"],
            "image_paths": ["front.png", "back.png"],
        }
        self.editor.apply_review_filter()

    def test_save_prompt_during_navigation_keeps_target_item_alive(self):
        self.add_second_counter()
        self.editor.notes.setPlainText("Edited before navigating")
        with patch.object(unit_editor.QMessageBox, "question", return_value=unit_editor.QMessageBox.StandardButton.Save), \
                patch("sys.excepthook") as errors:
            self.editor.browser.results.setCurrentRow(1)
        errors.assert_not_called()
        self.assertEqual(self.editor.selected_type_id, "two")
        self.assertEqual(self.editor.name_label.text(), "Second counter")
        saved = json.loads(self.path.read_text(encoding="utf-8"))["definitions"]
        self.assertEqual(saved["one"]["notes"], "Edited before navigating")
        self.assertNotIn("two", saved)

    def test_save_prompt_during_search_selects_matching_counter(self):
        self.add_second_counter()
        self.editor.notes.setPlainText("Saved before search")
        with patch.object(unit_editor.QMessageBox, "question", return_value=unit_editor.QMessageBox.StandardButton.Save), \
                patch("sys.excepthook") as errors:
            self.editor.browser.search.setText("Second")
        errors.assert_not_called()
        self.assertEqual(self.editor.selected_type_id, "two")
        self.assertEqual(self.editor.browser.results.count(), 1)
        self.assertEqual(self.editor.unit_definitions["one"]["notes"], "Saved before search")

    def test_cancel_navigation_preserves_selection_and_unsaved_edits(self):
        self.add_second_counter()
        before = self.path.read_bytes()
        self.editor.notes.setPlainText("Keep editing this")
        with patch.object(unit_editor.QMessageBox, "question", return_value=unit_editor.QMessageBox.StandardButton.Cancel), \
                patch("sys.excepthook") as errors:
            self.editor.browser.results.setCurrentRow(1)
        errors.assert_not_called()
        self.assertEqual(self.editor.selected_type_id, "one")
        self.assertEqual(self.editor.browser.results.currentRow(), 0)
        self.assertEqual(self.editor.notes.toPlainText(), "Keep editing this")
        self.assertTrue(self.editor.dirty)
        self.assertEqual(self.path.read_bytes(), before)

    def test_navigation_save_refreshes_status_filter_without_rebuild(self):
        self.add_second_counter()
        self.editor.unit_definitions["two"] = {"review_status": "Verified"}
        self.editor.review_filter.setCurrentText("Verified")
        self.editor.review_status.setCurrentText("In progress")
        with patch.object(unit_editor.QMessageBox, "question", return_value=unit_editor.QMessageBox.StandardButton.Save), \
                patch("sys.excepthook") as errors:
            self.editor.browser.results.setCurrentRow(1)
        errors.assert_not_called()
        self.assertEqual(self.editor.selected_type_id, "two")
        self.assertTrue(self.editor.browser.results.item(0).isHidden())
        self.assertIn("1 matching", self.editor.browser.count_label.text())

    def test_faces_and_blank_reverse(self):
        self.editor.ground_formats["back"].setCurrentText("Coastal defense")
        issues = self.editor.definition_issues()
        self.assertTrue(any("Back ratings: Coastal-defense level" in x for x in issues))
        for key in ("cd_level", "cd_short", "cd_long"):
            self.editor.ground_controls["back"][key].setText("N/A")
        self.assertEqual(self.editor.definition_issues(), [])
        self.editor.back_appearance.setCurrentText("Blank color")
        self.editor.ground_formats["back"].setCurrentText("Unknown")
        self.assertEqual(self.editor.definition_issues(), [])

    def test_face_sizes_round_trip_without_changing_printed_text(self):
        self.editor.unit_size.setCurrentText("Wing")
        self.editor.face_details_controls["back"]["unit_size_override"].setCurrentText("Squadron")
        self.editor.unit_definitions["one"]["faces"] = {"back": {"future_field": 42}}
        self.assertTrue(self.editor.dirty)
        self.assertTrue(self.editor.save_definition())
        saved = json.loads(self.path.read_text(encoding="utf-8"))["definitions"]["one"]
        self.assertEqual(saved["unit_size"], "Wing")
        self.assertIsNone(saved["faces"]["front"]["unit_size_override"])
        self.assertEqual(saved["faces"]["back"]["unit_size_override"], "Squadron")
        self.assertEqual(saved["faces"]["back"]["future_field"], 42)
        self.assertEqual(saved["faces"]["back"]["printed_size_status"], "")
        self.editor.load_definitions()
        self.editor.show_definition(self.editor.browser.results.currentItem(), None)
        self.assertEqual(self.editor.face_details_controls["front"]["unit_size_override"].currentText(), "Use shared unit size")
        self.assertEqual(self.editor.face_details_controls["back"]["unit_size_override"].currentText(), "Squadron")
        self.assertFalse(self.editor.dirty)

    def test_effective_face_size_checks_and_fallback(self):
        self.editor.unit_size.setCurrentText("Unknown")
        self.assertTrue(any("Front unit size" in issue for issue in self.editor.definition_issues()))
        for face, value in (("front", "Wing"), ("back", "Squadron")):
            self.editor.face_details_controls[face]["unit_size_override"].setCurrentText(value)
        self.assertEqual(self.editor.definition_issues(), [])
        self.editor.face_details_controls["back"]["unit_size_override"].setCurrentText("Use shared unit size")
        self.assertTrue(any("Back unit size" in issue for issue in self.editor.definition_issues()))
        self.editor.back_appearance.setCurrentText("Blank color")
        self.assertEqual(self.editor.definition_issues(), [])
        self.editor.unit_size.setCurrentText("N/A")
        self.editor.face_details_controls["front"]["unit_size_override"].setCurrentText("Use shared unit size")
        self.assertEqual(self.editor.definition_issues(), [])

    def test_invalid_face_size_override_rejected(self):
        data = json.loads(self.path.read_text(encoding="utf-8"))
        data["definitions"]["one"]["faces"] = {"front": {"unit_size_override": 123}}
        self.path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unit-size override"):
            self.editor.load_definitions()

    def test_incomplete_draft_and_verified_choices(self):
        self.editor.designation.clear()
        self.editor.front_image.setCurrentIndex(0)
        self.assertTrue(self.editor.definition_issues())
        before = self.path.read_bytes()
        with patch.object(self.editor, "confirm_verified_issues", return_value=False):
            self.assertFalse(self.editor.save_definition())
        self.assertEqual(self.path.read_bytes(), before)
        with patch.object(self.editor, "confirm_verified_issues", return_value=True):
            self.assertTrue(self.editor.save_definition())
        self.assertEqual(self.editor.review_status.currentText(), "In progress")
        self.assertIn("0 of 1 verified", self.editor.review_progress.text())
        self.assertIn("In progress", self.editor.browser.results.item(0).toolTip())
        self.editor.review_status.setCurrentText("Unreviewed")
        self.assertTrue(self.editor.save_definition())
        self.assertIsNone(self.editor.front_image.currentData())
        self.assertEqual(self.editor.designation.text(), "")

    def test_images_and_review_filter(self):
        (self.root / "front.png").write_text("not an image")
        self.editor.back_appearance.setCurrentText("Not yet reviewed")
        issues = self.editor.definition_issues()
        self.assertTrue(any("missing or unreadable" in x for x in issues))
        self.assertTrue(any("not yet reviewed" in x for x in issues))
        self.editor.dirty = False
        self.editor.review_filter.setCurrentText("Verified")
        self.editor.review_status.setCurrentText("In progress")
        self.assertTrue(self.editor.save_definition())
        self.assertTrue(self.editor.browser.results.item(0).isHidden())
        self.assertIn("0 matching", self.editor.browser.count_label.text())

    def test_glider_fields_completeness_and_mode_switch_preserves_ratings(self):
        self.editor.counter_category.setCurrentText("Air unit")
        self.editor.unit_type.setCurrentText("Glider")
        self.editor.back_appearance.setCurrentText("Blank color")
        controls = self.editor.aircraft_controls["front"]
        controls["attack_factor"].setText("7")
        controls["aircraft_type_code"].setText("G")
        self.assertTrue(controls["attack_factor"].isHidden())
        self.assertFalse(controls["tug_attack_modifier"].isHidden())
        self.assertTrue(any("Tug air attack" in issue for issue in self.editor.definition_issues()))
        for field, value in {
            "tug_attack_modifier": "-1", "tug_defense_modifier": "0",
            "tug_bombing_restriction": "N/A", "tug_range_modifier": "-25%",
            "capacity_code": "*",
        }.items():
            controls[field].setText(value)
        self.assertEqual(self.editor.definition_issues(), [])
        self.editor.review_status.setCurrentText("Verified")
        self.assertTrue(self.editor.save_definition())
        saved = json.loads(self.path.read_text(encoding="utf-8"))["definitions"]["one"]
        self.assertEqual(saved["aircraft"]["front"]["attack_factor"], "7")
        self.assertEqual(saved["aircraft"]["front"]["tug_range_modifier"], "-25%")
        self.editor.load_definitions()
        self.editor.show_definition(self.editor.browser.results.currentItem(), None)
        self.assertEqual(self.editor.aircraft_controls["front"]["tug_attack_modifier"].text(), "-1")
        controls = self.editor.aircraft_controls["front"]
        self.editor.unit_type.setCurrentText("Fighter")
        controls["aircraft_type_code"].setText("F")
        self.assertFalse(controls["attack_factor"].isHidden())
        self.assertTrue(controls["tug_attack_modifier"].isHidden())
        self.assertEqual(controls["attack_factor"].text(), "7")
        self.assertEqual(controls["tug_attack_modifier"].text(), "-1")

    def test_glider_printed_back_requires_its_own_fields(self):
        self.editor.counter_category.setCurrentText("Air unit")
        self.editor.unit_type.setCurrentText("Glider")
        for field, _ in unit_editor.glider_fields:
            self.editor.aircraft_controls["front"][field].setText("N/A")
        self.editor.aircraft_controls["front"]["aircraft_type_code"].setText("G")
        self.editor.aircraft_controls["front"]["capacity_code"].setText("0")
        self.assertTrue(any("Back ratings" in issue for issue in self.editor.definition_issues()))
        self.editor.back_appearance.setCurrentText("Blank color")
        self.assertEqual(self.editor.definition_issues(), [])

    def test_glider_fields_loader_rejects_non_text(self):
        data = json.loads(self.path.read_text(encoding="utf-8"))
        data["definitions"]["one"]["aircraft"] = {"front": {"tug_attack_modifier": -1}}
        self.path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Tug air attack"):
            self.editor.load_definitions()

    def test_optional_modifiers(self):
        for category, section, required in (
            ("Air unit", "aircraft", ("attack_factor", "aircraft_type_code", "air_defense", "range")),
            ("Naval unit", "naval", ("ship_type", "gunnery", "protection", "tactical_speed")),
            ("Commander", "commander", ("rank", "movement")),
        ):
            self.editor.counter_category.setCurrentText(category)
            self.editor.back_appearance.setCurrentText("Blank color")
            controls = (self.editor.aircraft_controls if section == "aircraft"
                        else self.editor.special_rating_controls[section])
            self.assertTrue(self.editor.definition_issues())
            for field in required:
                controls["front"][field].setText("0")
            self.assertEqual(self.editor.definition_issues(), [])


if __name__ == "__main__":
    unittest.main()
