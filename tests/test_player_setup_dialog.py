import copy
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication
from game.player_setup_dialog import PlayerSetupDialog
from rules.sides import default_setup, validate_setup
from tests.test_sides import roster


class PlayerSetupDialogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.view = SimpleNamespace(player_setup=default_setup(roster()), units={},
                                    counter_project_dir=Path(self.temp.name))
        self.dialog = PlayerSetupDialog(self.view)

    def tearDown(self):
        self.dialog.close()
        self.temp.cleanup()

    def test_mode_limits_balancing_and_manual_edit(self):
        self.assertFalse(self.dialog.counts["axis"].isEnabled())
        self.dialog.mode.setCurrentIndex(1)
        self.dialog.counts["axis"].setValue(2)
        self.dialog.suggest()
        self.dialog.players_table.item(0, 1).setText("Alice")
        self.dialog.save_setup()
        setup = self.view.player_setup
        self.assertEqual(len(setup["players"]["axis"]), 2)
        self.assertEqual(setup["players"]["axis"][0]["name"], "Alice")
        self.assertEqual(validate_setup(setup), setup)
        again = PlayerSetupDialog(self.view)
        try:
            again.mode.setCurrentIndex(4)
            self.assertEqual(again.counts["axis"].value(), 1)
            self.assertEqual(again.counts["allied"].value(), 1)
            again.save_setup()
            self.assertEqual(self.view.player_setup["players"]["allied"][0]["controller"], "ai")
        finally:
            again.close()

    def test_cancel_does_not_change_roster_or_assignments(self):
        before = copy.deepcopy(self.view.player_setup)
        self.dialog.table.cellWidget(0, 1).setCurrentText("Neutral")
        self.dialog.add_nation()
        self.dialog.reject()
        self.assertEqual(self.view.player_setup, before)

    def test_saved_player_ids_and_unknown_fields_survive_editing(self):
        self.dialog.close()
        self.view.player_setup["players"]["axis"][0].update(player_id="custom-player", future=42)
        self.view.player_setup["assignments"].update({f"axis-{i}": "custom-player" for i in range(3)})
        self.dialog = PlayerSetupDialog(self.view)
        self.dialog.save_setup()
        self.assertEqual(self.view.player_setup["players"]["axis"][0]["player_id"], "custom-player")
        self.assertEqual(self.view.player_setup["players"]["axis"][0]["future"], 42)
