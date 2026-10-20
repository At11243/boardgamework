"""Resource paths and backup contents after relocating Python modules."""
import importlib
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch
from zipfile import ZipFile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication
from maps.map_view import MapView
from counters import unit_editor
import main


class ProjectLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_root_resources_and_imports(self):
        root = Path(__file__).resolve().parents[1]
        view = MapView()
        try:
            self.assertEqual(view.transport_path, root / "map_transport.json")
            self.assertEqual(view.counter_project_dir, root)
            self.assertEqual(unit_editor.project_dir, root)
            self.assertEqual(main.project_dir, root)
            for name in ("maps.import_grids", "counters.import_counters", "game.action_history",
                         "game.dice_dialog", "game.history_panel", "rules.dice", "rules.combat_records"):
                importlib.import_module(name)
        finally:
            view.close()

    def test_unit_editor_direct_file_import_from_another_directory(self):
        root = Path(__file__).resolve().parents[1]
        script = root / "counters" / "unit_editor.py"
        # Isolated subprocess reproduces an IDE's script-only import path.
        # A non-main run name checks startup imports without opening the editor
        # or reading/writing the real unit-definition files.
        code = (
            "import runpy,sys; from pathlib import Path; "
            "script=Path(sys.argv[1]); sys.path.insert(0,str(script.parent)); "
            "state=runpy.run_path(str(script),run_name='direct_launch_smoke'); "
            "assert state['project_dir']==script.parent.parent; "
            "assert state['CounterBrowser'].__module__=='counters.counter_browser'"
        )
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, "-I", "-B", "-c", code, str(script)],
                                    cwd=folder, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_mapping_backup_uses_relocated_definitions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "maps").mkdir()
            files = {
                "map_terrain.json": "temporary terrain",
                "map_transport.json": "temporary transport",
                "maps/campaign_grid_definitions.py": "temporary grids",
                "maps/campaign_layout.py": "temporary layout",
            }
            for name, text in files.items():
                (root / name).write_text(text, encoding="utf-8")
            destination = root / "backup.zip"
            fake = SimpleNamespace(
                map_view=SimpleNamespace(brush_before=None, transport_path=root / "map_transport.json"),
                terrain_path=root / "map_terrain.json", statusBar=Mock(return_value=Mock()),
            )
            with patch.object(main, "project_dir", root), \
                    patch.object(main.QFileDialog, "getSaveFileName", return_value=(str(destination), "")):
                main.MainWindow.export_mapping_backup(fake)
            with ZipFile(destination) as archive:
                for name, text in files.items():
                    self.assertEqual(archive.read(Path(name).name).decode("utf-8"), text)
                self.assertIsNone(archive.testzip())
