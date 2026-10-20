"""Counter mechanics tests use temporary saves/images and no original artwork."""
import copy
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QApplication, QMainWindow
from maps.map_view import MapView
from maps.campaign_layout import barbarossa_boards
from maps.campaign_grid_definitions import barbarossa_grids
from counters.counter_state import restore_units, stack_ids
from counters.stack_inspector import StackInspector
from counters.counter_browser import CounterBrowser


class CounterMechanicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.image = self.root / "counter.png"
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.blue)
        pixmap.save(str(self.image))
        self.window = QMainWindow()
        self.view = MapView(self.window)
        self.view.counter_project_dir = self.root
        self.window.setCentralWidget(self.view)
        self.boards = {bid: {"origin": (x, y), "size": (w, h)}
                       for bid, filename, x, y, w, h in barbarossa_boards}
        region = barbarossa_grids["Map 2"]["regions"][0]["name"]
        self.key = self.view.canonical_hex_key(("Map 2", region, 8, 45))
        self.load_maps(None)
        self.view.selected_hex_key = self.key
        self.view.hexes = {self.key: {"units": [], "game_reference": "test"}}
        self.inspector = StackInspector(self.view)

    def tearDown(self):
        self.inspector.close()
        self.window.close()
        self.temp.cleanup()

    def load_maps(self, unused):
        self.view.reset_counter_selection()
        self.view.map_scene.clear()
        self.view.board_records = copy.deepcopy(self.boards)
        self.view.debug_marker = self.view.map_scene.addRect(0, 0, 1, 1)
        self.view.map_item = self.view.debug_marker

    def place(self):
        return self.view.place_counter({"type_id": "same-type", "name": "Test counter",
                                        "image_path": str(self.image)})

    def test_selection_stack_and_round_trip(self):
        first, second = self.place(), self.place()
        self.assertNotEqual(first, second)
        self.assertEqual(stack_ids(self.view.units, self.key), [first, second])
        self.assertEqual(self.inspector.results.count(), 2)
        self.assertEqual(self.inspector.results.item(0).data(Qt.ItemDataRole.UserRole), second)
        self.inspector.results.setCurrentRow(1)
        self.assertEqual(self.view.selected_unit_id, first)
        self.assertIsNotNone(self.view.unit_highlight)
        self.assertLess(self.view.unit_items[first].zValue(), self.view.unit_items[second].zValue())
        self.view.units[first]["future_state"] = {"keep": True}
        # Simulate a newer writer that records an additional instance field.
        self.view.action_history["entries"][0]["after"]["future_state"] = {"keep": True}
        self.view.campaign_metadata = {"future_header": "preserve"}
        path = self.root / "campaign.json"
        self.view.save_campaign(path)
        before = json.loads(path.read_text(encoding="utf-8"))
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        self.assertEqual(self.view.selected_unit_id, first)
        self.assertEqual(stack_ids(self.view.units, self.key), [first, second])
        self.assertEqual(self.view.units[first]["future_state"], {"keep": True})
        self.assertEqual(self.view.unit_items[first].pixmap().size().width(), 24)
        self.view.save_campaign(path)
        after = json.loads(path.read_text(encoding="utf-8"))
        # Hex loading intentionally recalculates derived geometry/reference fields.
        self.assertEqual(after["units"], before["units"])
        self.assertEqual(after["selected_unit_id"], before["selected_unit_id"])
        self.assertEqual(after["future_header"], before["future_header"])
        self.assertFalse(path.with_suffix(".json.tmp").exists())

    def test_old_saves_and_invalid_data(self):
        uid = self.place()
        path = self.root / "campaign.json"
        self.view.save_campaign(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        for mutate in (
            lambda d: d["units"].append(copy.deepcopy(d["units"][0])),
            lambda d: d["units"][0].update(stack_order=-1),
            lambda d: d["units"][0].update(hex_key=["bad", "region", 1, 1]),
            lambda d: d["units"][0].update(image_path=str(self.root / "missing.png")),
            lambda d: d.update(selected_unit_id="missing"),
        ):
            bad = copy.deepcopy(data)
            mutate(bad)
            path.write_text(json.dumps(bad), encoding="utf-8")
            with patch.object(self.view, "load_campaign") as loader:
                with self.assertRaises(ValueError):
                    self.view.load_campaign_save(path, self.root)
                loader.assert_not_called()
            self.assertIn(uid, self.view.units)
        data.pop("units")
        data.pop("selected_unit_id")
        data.pop("action_history")
        path.write_text(json.dumps(data), encoding="utf-8")
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        self.assertEqual(self.view.units, {})
        self.assertIsNone(self.view.selected_unit_id)
        self.assertEqual(self.inspector.results.count(), 0)

    def test_click_and_mapping_modes(self):
        uid = self.place()
        _, x, y = self.view.hex_key_geometry(self.key)
        event = SimpleNamespace(position=lambda: QPointF(QPoint(0, 0)))
        with patch.object(self.view, "mapToScene", return_value=QPointF(x, y)), \
                patch.object(self.view, "select_campaign_point", return_value=True):
            self.view.select_unit(None)
            self.view.select_hex(event)
            self.assertEqual(self.view.selected_unit_id, uid)
            self.view.select_unit(None)
            self.view.transport_draw_mode = True
            with patch.object(self.view, "draw_transport_to") as draw:
                self.view.select_hex(event)
                draw.assert_called_once()
            self.assertIsNone(self.view.selected_unit_id)

    def test_minimal_instance_defaults(self):
        uid = self.place()
        record = self.view.units[uid].copy()
        record.pop("active_face")
        record.pop("stack_order")
        restored = restore_units([record], self.view.canonical_hex_key, self.view.hexes)
        self.assertEqual(restored[uid]["active_face"], "unassigned")
        self.assertEqual(restored[uid]["stack_order"], 0)

    def write_definition(self, appearance="Printed image", status="Verified"):
        back = self.root / "alternate.png"
        image = QPixmap(32, 20)
        image.fill(Qt.GlobalColor.red)
        image.save(str(back))
        definition = {"review_status": status, "front_image": str(self.image),
                      "back_image": str(back), "back_appearance": appearance,
                      "blank_back_color": "#123456"}
        path = self.root / "assets" / "counters" / "unit_definitions.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"format": "tsww-barbarossa-unit-definitions",
                                   "version": 1, "definitions": {"same-type": definition}}),
                        encoding="utf-8")
        return path

    def test_printed_flip_preserves_instance_and_stack(self):
        self.write_definition()
        first, second = self.place(), self.place()
        original = self.view.units[first].copy()
        self.view.select_unit(first)
        self.assertTrue(self.inspector.flip_button.isEnabled())
        self.assertTrue(self.view.flip_selected_counter())
        self.assertEqual(self.view.units[first]["active_face"], "back")
        self.assertEqual(self.view.unit_items[first].pixmap().width(), 32)
        self.assertEqual(self.view.units[second]["active_face"], "unassigned")
        for field in ("unit_id", "type_id", "name", "hex_key", "stack_order"):
            self.assertEqual(self.view.units[first][field], original[field])
        path = self.root / "flipped.json"
        self.view.save_campaign(path)
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        self.assertEqual(self.view.units[first]["active_face"], "back")
        self.assertEqual(self.view.unit_items[first].pixmap().width(), 32)
        self.assertEqual(stack_ids(self.view.units, self.key), [first, second])
        self.assertTrue(self.view.flip_selected_counter())
        self.assertEqual(self.view.units[first]["active_face"], "front")
        self.assertEqual(self.view.units[first]["image_path"], original["image_path"])

    def test_blank_flip_persists_without_definition(self):
        definition_path = self.write_definition("Blank color")
        before = definition_path.read_bytes()
        uid = self.place()
        self.assertTrue(self.view.flip_selected_counter())
        pixmap = self.view.unit_items[uid].pixmap()
        self.assertEqual(pixmap.size().width(), 24)
        self.assertEqual(pixmap.size().height(), 24)
        self.assertEqual(pixmap.toImage().pixelColor(10, 10).name(), "#123456")
        self.assertEqual(definition_path.read_bytes(), before)
        path = self.root / "blank.json"
        self.view.save_campaign(path)
        definition_path.unlink()
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        self.assertEqual(self.view.units[uid]["active_face"], "back")
        self.assertEqual(self.view.unit_items[uid].pixmap().toImage().pixelColor(0, 0).name(), "#123456")
        self.assertTrue(self.view.flip_selected_counter())
        self.assertEqual(self.view.units[uid]["active_face"], "front")

    def test_unresolved_flips_do_not_mutate(self):
        uid = self.place()
        original = copy.deepcopy(self.view.units[uid])
        self.assertFalse(self.view.flip_selected_counter())
        self.assertFalse(self.inspector.flip_button.isEnabled())
        self.write_definition(status="In progress")
        self.assertIn("Verified", self.view.flip_unavailable_reason())
        self.assertFalse(self.view.flip_selected_counter())
        self.write_definition(appearance="Not yet reviewed")
        self.assertIn("not been reviewed", self.view.flip_unavailable_reason())
        self.write_definition()
        (self.root / "alternate.png").unlink()
        self.assertIn("Cannot load", self.view.flip_unavailable_reason())
        self.assertFalse(self.view.flip_selected_counter())
        self.assertEqual(self.view.units[uid], original)

        self.write_definition()
        # A third appearance must not be guessed to be the front or back.
        third = self.root / "third.png"
        image = QPixmap(12, 12)
        image.fill(Qt.GlobalColor.green)
        image.save(str(third))
        self.view.units[uid]["image_path"] = str(third)
        self.assertIn("does not identify", self.view.flip_unavailable_reason())
        self.assertFalse(self.view.flip_selected_counter())

    def test_existing_alternate_and_mode_guard(self):
        self.write_definition()
        uid = self.view.place_counter({"type_id": "same-type", "name": "Alternate",
                                      "image_path": str(self.root / "alternate.png")})
        self.view.set_edge_pick_mode(True)
        self.assertFalse(self.inspector.flip_button.isEnabled())
        self.assertFalse(self.view.flip_selected_counter())
        self.view.set_edge_pick_mode(False)
        self.assertTrue(self.inspector.flip_button.isEnabled())
        self.assertTrue(self.view.flip_selected_counter())
        self.assertEqual(self.view.units[uid]["active_face"], "front")

    def test_browser_review_status_and_reload(self):
        definition = self.write_definition()
        before = definition.read_bytes()
        browser = CounterBrowser(self.root, show_review_controls=True)
        try:
            browser.counter_types = {
                "same-type": {"name": "GE Inf XX 87 @126.FB", "palette": []},
                "unreviewed": {"name": "Other", "palette": []},
            }
            browser.load_review_definitions()
            self.assertIn("Verified", browser.results.item(0).toolTip())
            browser.verified_only.setChecked(True)
            self.assertEqual(browser.results.count(), 1)
            browser.search.setText("87")
            self.assertEqual(browser.results.count(), 1)
            browser.search.setText("Other")
            self.assertEqual(browser.results.count(), 0)
            browser.search.clear()
            self.assertEqual(definition.read_bytes(), before)
            self.write_definition(status="In progress")
            browser.reload_reviews()
            self.assertEqual(browser.results.count(), 0)
            browser.verified_only.setChecked(False)
            self.assertIn("In progress", browser.results.item(0).toolTip())
        finally:
            browser.close()

    def destination(self):
        board, region, col, row = self.key
        key = self.view.canonical_hex_key((board, region, col, row + 1))
        self.view.hexes[key] = {"units": [], "game_reference": "destination"}
        return key

    def test_move_flipped_counter_to_top_and_reload(self):
        self.write_definition("Blank color")
        first, second = self.place(), self.place()
        self.view.select_unit(first)
        self.view.flip_selected_counter()
        original = copy.deepcopy(self.view.units[first])
        destination = self.destination()
        self.view.selected_hex_key = destination
        resident = self.place()
        self.view.selected_hex_key = self.key
        self.view.select_unit(first)
        self.assertTrue(self.view.begin_counter_move())
        self.assertFalse(self.inspector.flip_button.isEnabled())
        self.assertTrue(self.view.finish_counter_move(destination))
        self.assertEqual(stack_ids(self.view.units, self.key), [second])
        self.assertEqual(stack_ids(self.view.units, destination), [resident, first])
        for field in original.keys() - {"hex_key", "stack_order"}:
            self.assertEqual(self.view.units[first][field], original[field])
        self.assertEqual(self.view.selected_unit_id, first)
        self.assertIsNone(self.view.moving_unit_id)
        self.assertEqual(self.inspector.results.count(), 2)
        path = self.root / "moved.json"
        self.view.save_campaign(path)
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        self.assertEqual(self.view.units[first]["hex_key"], destination)
        self.assertEqual(self.view.units[first]["active_face"], "back")
        self.assertEqual(stack_ids(self.view.units, destination), [resident, first])
        self.assertEqual(self.view.unit_items[first].pixmap().toImage().pixelColor(0, 0).name(), "#123456")

    def test_cancel_same_hex_and_mapping_guard(self):
        uid = self.place()
        before = copy.deepcopy(self.view.units)
        self.view.begin_counter_move()
        self.view.cancel_counter_move()
        self.assertEqual(self.view.units, before)
        self.view.begin_counter_move()
        self.view.keyPressEvent(QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Escape,
                                         Qt.KeyboardModifier.NoModifier))
        self.assertIsNone(self.view.moving_unit_id)
        self.view.begin_counter_move()
        self.view.finish_counter_move(self.key)
        self.assertEqual(self.view.units, before)
        self.view.begin_counter_move()
        self.view.set_edge_pick_mode(True)
        self.assertIsNone(self.view.moving_unit_id)
        self.assertFalse(self.view.begin_counter_move())
        self.assertEqual(self.view.units, before)
        self.assertEqual(self.view.selected_unit_id, uid)

    def test_destination_click_and_invalid_click(self):
        uid = self.place()
        destination = self.destination()
        self.view.begin_counter_move()
        event = SimpleNamespace(position=lambda: QPointF(0, 0))
        with patch.object(self.view, "select_campaign_point", return_value=False):
            self.view.select_hex(event)
        self.assertEqual(self.view.moving_unit_id, uid)
        self.assertEqual(self.view.units[uid]["hex_key"], self.key)
        def choose(point):
            self.view.selected_hex_key = destination
            self.view.hex_selected.emit("destination", {})
            return True
        with patch.object(self.view, "select_campaign_point", side_effect=choose):
            self.view.select_hex(event)
        self.assertEqual(self.view.units[uid]["hex_key"], destination)
        self.assertEqual(self.view.selected_unit_id, uid)

    def test_history_undo_redo_entire_sequence(self):
        from game.history_panel import HistoryPanel
        panel = HistoryPanel(self.view)
        try:
            self.write_definition()
            first, second = self.place(), self.place()
            initial = copy.deepcopy(self.view.units)
            self.view.select_unit(first)
            self.assertTrue(self.view.flip_selected_counter())
            destination = self.destination()
            self.view.begin_counter_move()
            self.view.finish_counter_move(destination)
            final = copy.deepcopy(self.view.units)
            self.assertEqual([e["kind"] for e in self.view.action_history["entries"]],
                             ["place", "place", "flip", "move"])
            self.assertEqual(panel.results.count(), 4)
            self.assertTrue(self.view.undo_counter_action())
            self.assertEqual(stack_ids(self.view.units, self.key), [first, second])
            self.assertEqual(self.view.units[first]["active_face"], "back")
            self.assertTrue(self.view.undo_counter_action())
            self.assertEqual(self.view.units, initial)
            self.assertTrue(self.view.undo_counter_action())
            self.assertNotIn(second, self.view.unit_items)
            self.assertTrue(self.view.undo_counter_action())
            self.assertEqual(self.view.units, {})
            self.assertFalse(panel.undo_button.isEnabled())
            self.assertTrue(panel.redo_button.isEnabled())
            self.assertFalse(self.view.undo_counter_action())
            for _ in range(4):
                self.assertTrue(self.view.redo_counter_action())
            self.assertEqual(self.view.units, final)
            self.assertEqual(set(self.view.unit_items), set(final))
            self.assertFalse(self.view.redo_counter_action())
            self.assertEqual(panel.results.count(), 4)
        finally:
            panel.close()

    def test_history_persistence_with_redo_and_branch(self):
        self.write_definition("Blank color")
        uid = self.place()
        self.view.flip_selected_counter()
        flipped = copy.deepcopy(self.view.units)
        self.view.undo_counter_action()
        path = self.root / "history.json"
        self.view.save_campaign(path)
        saved = json.loads(path.read_text(encoding="utf-8"))["action_history"]
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        self.assertEqual(self.view.action_history["cursor"], 1)
        self.assertTrue(self.view.redo_counter_action())
        self.assertEqual(self.view.units, flipped)
        self.view.undo_counter_action()
        self.place()
        self.assertFalse(self.view.can_redo_counter_action())
        self.assertEqual(len(self.view.action_history["entries"]), 2)
        self.assertEqual(self.view.action_history["entries"][-1]["kind"], "place")
        self.assertNotEqual(self.view.action_history["entries"][-1]["action_id"], saved["entries"][-1]["action_id"])
        self.assertIn(uid, self.view.units)

    def test_history_excludes_cancel_and_selection_and_guards_modes(self):
        uid = self.place()
        original = copy.deepcopy(self.view.action_history)
        self.view.select_unit(None)
        self.view.select_unit(uid)
        self.view.begin_counter_move()
        self.assertFalse(self.view.undo_counter_action())
        self.view.cancel_counter_move()
        self.view.begin_counter_move()
        self.view.finish_counter_move(self.key)
        self.assertEqual(self.view.action_history, original)
        self.view.set_edge_pick_mode(True)
        self.assertFalse(self.view.undo_counter_action())
        self.view.set_edge_pick_mode(False)
        self.assertTrue(self.view.undo_counter_action())

    def test_invalid_history_rejected_before_replacing_campaign(self):
        self.place()
        path = self.root / "invalid-history.json"
        self.view.save_campaign(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        before = copy.deepcopy(self.view.units)
        for mutate in (
            lambda h: h.update(cursor=999),
            lambda h: h["entries"][0].update(kind="unknown"),
            lambda h: h["entries"][0]["after"].update(name="inconsistent"),
            lambda h: h["entries"].append(copy.deepcopy(h["entries"][0])),
        ):
            bad = copy.deepcopy(data)
            mutate(bad["action_history"])
            path.write_text(json.dumps(bad), encoding="utf-8")
            with patch.object(self.view, "load_campaign") as loader:
                with self.assertRaises(ValueError):
                    self.view.load_campaign_save(path, self.root)
                loader.assert_not_called()
            self.assertEqual(self.view.units, before)

    def test_failed_redo_leaves_state_and_cursor_unchanged(self):
        self.place()
        self.view.undo_counter_action()
        before = copy.deepcopy(self.view.action_history)
        self.image.unlink()
        self.assertFalse(self.view.redo_counter_action())
        self.assertEqual(self.view.units, {})
        self.assertEqual(self.view.action_history, before)

    def test_legacy_counter_save_starts_new_history(self):
        uid = self.place()
        path = self.root / "legacy-counters.json"
        self.view.save_campaign(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        data.pop("action_history")
        path.write_text(json.dumps(data), encoding="utf-8")
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        self.assertFalse(self.view.can_undo_counter_action())
        destination = self.destination()
        self.view.begin_counter_move()
        self.view.finish_counter_move(destination)
        self.view.undo_counter_action()
        self.assertEqual(self.view.units[uid]["hex_key"], self.key)
        self.assertFalse(self.view.can_undo_counter_action())
        self.assertIn(uid, self.view.units)

    def test_dice_attack_events_persist_and_redo_without_reroll(self):
        from rules import attack_result_record
        from game.history_panel import HistoryPanel
        uid = self.place()
        before = copy.deepcopy(self.view.units)
        roll = self.view.record_dice_roll("percentile", manual_faces=[0, 0], purpose="test")
        self.assertEqual(roll["value"], 100)
        result = attack_result_record(attacker_ids=[uid], defender_ids=["defender-instance"],
                                      target_hex=list(self.key), result="DR", rolls=[roll], notes="Manual example")
        self.view.record_attack_result(result)
        self.assertEqual(self.view.units, before)
        panel = HistoryPanel(self.view)
        self.assertEqual(panel.results.count(), 3)
        self.assertIn("Manual example", panel.results.item(2).toolTip())
        panel.close()
        self.view.undo_counter_action()  # attack result
        self.view.undo_counter_action()  # dice record
        path = self.root / "recorded-results.json"
        self.view.save_campaign(path)
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        with patch.object(self.view.dice_service, "roll") as roller:
            self.assertTrue(self.view.redo_counter_action())
            self.assertTrue(self.view.redo_counter_action())
            roller.assert_not_called()
        self.assertEqual(self.view.action_history["entries"][1]["payload"], roll)
        self.assertEqual(self.view.action_history["entries"][2]["payload"], result)
        self.assertEqual(self.view.units, before)
        # Counter replay still works with result-only entries interleaved.
        for _ in range(3):
            self.assertTrue(self.view.undo_counter_action())
        self.assertEqual(self.view.units, {})
        for _ in range(3):
            self.assertTrue(self.view.redo_counter_action())
        self.assertEqual(self.view.units, before)

    def test_dice_dialog_manual_and_ai_modes(self):
        from game.dice_dialog import DiceDialog
        dialog = DiceDialog(self.view)
        try:
            self.assertEqual(len(self.view.action_history["entries"]), 0)
            dialog.roll_type.setCurrentIndex(2)
            dialog.method.setCurrentIndex(1)
            dialog.first.setValue(0)
            dialog.second.setValue(0)
            dialog.record_roll()
            self.assertIn("100", dialog.result.text())
            self.assertEqual(self.view.action_history["entries"][-1]["payload"]["method"], "manual")
        finally:
            dialog.close()
        ai = DiceDialog(self.view, controller="ai")
        try:
            self.assertEqual(ai.method.count(), 1)
            self.assertFalse(ai.method.isEnabled())
            ai.record_roll()
            self.assertEqual(self.view.action_history["entries"][-1]["payload"]["controller"], "ai")
            self.assertEqual(self.view.action_history["entries"][-1]["payload"]["method"], "automatic")
        finally:
            ai.close()

    def test_tampered_dice_save_rejected(self):
        self.view.record_dice_roll("1D10", manual_faces=[0])
        path = self.root / "bad-dice.json"
        self.view.save_campaign(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        data["action_history"]["entries"][0]["payload"]["value"] = 0
        path.write_text(json.dumps(data), encoding="utf-8")
        before = copy.deepcopy(self.view.action_history)
        with patch.object(self.view, "load_campaign") as loader:
            with self.assertRaises(ValueError):
                self.view.load_campaign_save(path, self.root)
            loader.assert_not_called()
        self.assertEqual(self.view.action_history, before)

    def test_player_setup_persistence_and_invalid_load(self):
        from tests.test_sides import team_setup
        from rules.sides import default_setup
        from game.nation_roster import initial_roster
        self.view.player_setup = team_setup(2, 1)
        self.view.player_setup["future"] = {"keep": True}
        path = self.root / "players.json"
        self.view.save_campaign(path)
        expected = copy.deepcopy(self.view.player_setup)
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        self.assertEqual(self.view.player_setup, expected)
        data = json.loads(path.read_text(encoding="utf-8"))
        data["player_setup"]["assignments"]["axis-0"] = "allied-1"
        path.write_text(json.dumps(data), encoding="utf-8")
        with patch.object(self.view, "load_campaign") as loader:
            with self.assertRaises(ValueError):
                self.view.load_campaign_save(path, self.root)
            loader.assert_not_called()
        self.assertEqual(self.view.player_setup, expected)
        data.pop("player_setup")
        path.write_text(json.dumps(data), encoding="utf-8")
        with patch.object(self.view, "load_campaign", side_effect=self.load_maps):
            self.view.load_campaign_save(path, self.root)
        self.assertEqual(self.view.player_setup, default_setup(initial_roster()))


if __name__ == "__main__":
    unittest.main()
