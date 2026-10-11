import sys
from pathlib import Path
from datetime import datetime
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QDockWidget
)

from terrain_editor import TerrainEditor
from map_view import MapView
from campaign_layout import barbarossa_boards
from counter_browser import CounterBrowser

project_dir = Path(__file__).resolve().parent
maps_dir = project_dir / "assets" / "maps"



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TSWW Barbarossa")
        self.resize(1200,800)

        self.map_view = MapView(self)
        self.setCentralWidget(self.map_view)

        self.terrain_path = project_dir / "map_terrain.json"

        self.terrain_editor = TerrainEditor(self)

        terrain_dock = QDockWidget("Hex Information", self)
        terrain_dock.setWidget(self.terrain_editor)
        terrain_dock.setMinimumWidth(200)

        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            terrain_dock
        )

        self.map_view.hex_selected.connect(
            self.terrain_editor.show_hex
        )

        self.terrain_editor.applied.connect(self.apply_terrain)

        self.terrain_editor.transport_branch_requested.connect(
            self.map_view.start_transport_branch
        )

        self.terrain_editor.transport_mode_changed.connect(
            self.map_view.set_transport_draw_mode
        )

        self.terrain_editor.edge_mode_changed.connect(
            self.map_view.set_edge_pick_mode
        )

        self.map_view.edge_selected.connect(
            self.terrain_editor.focus_hexside
        )

        self.map_view.transport_summary_changed.connect(
            self.terrain_editor.show_transport_connections
        )

        self.map_view.hex_selected.connect(
            self.map_view.refresh_transport_summary
        )

        self.terrain_editor.transport_erase_changed.connect(
            self.map_view.set_transport_erase_mode
        )

        self.terrain_storage_ready = True

        try: 
            self.map_view.load_map_definitions(self.terrain_path)
        except (OSError, ValueError) as error:
            self.terrain_storage_ready = False
            QMessageBox.critical(
                self,
                "Terrain loading failed", 
                str(error)
            )
        self.board_records = {}

        self.map_view.terrain_brush_path = self.terrain_path 

        self.terrain_editor.terrain_brush_changed.connect(
            self.change_terrain_brush
        )
        self.terrain_editor.terrain_brush_undo_requested.connect(
            self.map_view.undo_terrain_brush
        )

        self.counter_browser = CounterBrowser(project_dir, self)

        self.counter_dock = QDockWidget("Counters", self)
        self.counter_dock.setWidget(self.counter_browser)

        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            self.counter_dock
        )

        self.counter_browser.place_requested.connect(
            self.place_counter
        )

        try:
            self.counter_browser.load_catalog(
                project_dir
                / "assets"
                / "counters"
                / "counter_catalog.json"
            )
        except (OSError, ValueError, KeyError, TypeError) as error:
            QMessageBox.warning(
                self,
                "Counter Catalog Loading Failed",
                str(error),
            )

        self.create_menus()
        self.statusBar().setVisible(True)
        self.statusBar().showMessage("Status bar ready- click the map")

    def change_terrain_brush(self, enabled, properties): 
        if enabled and not self.terrain_storage_ready:
            self.terrain_editor.brush_button.setChecked(False)
            QMessageBox.warning(
                self,
                "Terrain brush unavailable",
                "Resolve the terrain loading error before painting."
            )
            return 

        self.map_view.set_terrain_brush(enabled, properties)

    def place_counter(self, counter):
        try:
            self.map_view.place_counter(counter)
        except (OSError, ValueError, KeyError) as error:
            QMessageBox.warning(
                self,
                "Counter Placement Failed",
                str(error)
            )

    def create_menus(self):
        file_menu = self.menuBar().addMenu("File")
        backup_action = QAction("Export Mapping Backup...", self)
        backup_action.triggered.connect(self.export_mapping_backup)
        file_menu.addAction(backup_action)
        file_menu.addSeparator()

        open_action = QAction("Open Map...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_map)
        file_menu.addAction(open_action)

        campaign_action = QAction("Open Barbarossa Campaign", self)
        campaign_action.setShortcut("Ctrl + Shift + O")
        campaign_action.triggered.connect(self.open_campaign)
        file_menu.addAction(campaign_action)


        view_menu = self.menuBar().addMenu("View")

        audit_action = QAction("Audit Shared Hexsides...", self)
        audit_action.triggered.connect(
            self.map_view.audit_mapping_edges
        )

        view_menu.addAction(audit_action)
        view_menu.addSeparator()

        fit_action = QAction("Fit Map to Window", self)
        fit_action.setShortcut("F")
        fit_action.triggered.connect(self.map_view.fit_map)
        view_menu.addAction(fit_action)

        jump_action = QAction("Jump to Counter", self)
        jump_action.setShortcut("J")
        jump_action.triggered.connect(self.map_view.jump_to_counter)
        view_menu.addAction(jump_action)

        review_action = QAction(
            "Review Overlay -- Green / Amber/ Red", self
        )
        review_action.setCheckable(True)
        review_action.toggled.connect(
            self.map_view.set_review_overlay
        )
        view_menu.addAction(review_action)

        save_action = QAction("Save Campaign...", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_campaign)
        file_menu.addAction(save_action)

        load_save_action = QAction("Load Campaign Save...", self)
        load_save_action.triggered.connect(self.load_campaign_save)
        file_menu.addAction(load_save_action)

        transport_overlay_action = QAction(
            "Transport Review Overlay", self
        )
        transport_overlay_action.setCheckable(True)
        transport_overlay_action.toggled.connect(
            self.map_view.set_transport_review_overlay
        )
        view_menu.addAction(transport_overlay_action)

    def open_map(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open a Barbarossa map",
            str(maps_dir),
            "Map images (*.png *.jpg *.jpeg)",
        )

        if not filename:
            return
        
        self.statusBar().showMessage("Loading map...")

        try:
            self.map_view.load_map(filename)
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, "Map loading failed", str(error))
            self.statusBar().showMessage("Map loading failed")
            return
        
        size = self.map_view.original_size
        name = Path(filename).name

        self.setWindowTitle(f"TSWW Barbaross - {name}")
        self.statusBar().showMessage(
            f"{name} | Original: {size.width()} x {size.height()} pixels"
            " | Scroll to zoom | Drag to pan | f to fit"
        )

    def open_campaign(self):
        self.statusBar().showMessage("loading Campaign Maps...")


        try:
            count = self.map_view.load_campaign(maps_dir)
        except (OSError, ValueError, MemoryError) as error:
            QMessageBox.critical(
                self,
                "Campaign loading failed",
                str(error),
            )
            self.statusBar().showMessage("Campaign loading failed")
            return

        self.setWindowTitle("TSWW Barbarossa -- Campaign")
        self.statusBar().showMessage(
            f"{count} campaign boards loaded"
            " | Scroll to zoom | Drag to pan | f to fit |"
        )

    def save_campaign(self):
        if not self.map_view.board_records:
            QMessageBox.information(
                self,
                "Save Campaign",
                "Load the campaign before saving.",
            )
            return 

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Barbarossa campaign",
            str(project_dir / "barbarossa_campaign.json"), 
            "Campaign saves (*.json)",
        )

        if not filename:
            return 

        path = Path(filename)

        if path.suffix.lower() != ".json":
            path = Path(str(path) + ".json")

        try: 
            self.map_view.save_campaign(path)

        except (OSError, ValueError, TypeError) as error:
            QMessageBox.critical(
                self,
                "Campaign saving failed",
                str(error)
            )
            return

        self.statusBar().showMessage(
            f"Saved {len(self.map_view.hexes)} hex records"
            f"to {path.name}"
        )

    def load_campaign_save(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Load barbarossa campaign save",
            str(project_dir),
            "Campaign saves (*.json)",
        )

        if not filename:
            return 

        self.statusBar().showMessage("Loading campaign save...")

        try:
            count = self.map_view.load_campaign_save(
                filename, maps_dir
            )
        except (OSError, ValueError, MemoryError) as error:
            QMessageBox.critical(
                self,
                "Campaign loading failed",
                str(error),
            )
            self.statusBar().showMessage("Campaign loading failed")
            return 

        self.setWindowTitle(
            f"TSWW Barbarossa - {Path(filename).name}"
        )
        self.statusBar().showMessage(
            f"Loaded {count} hex records"
            " | J to jump to marker | F to fit map"
        )

    def apply_terrain(self, properties):
        if not self.terrain_storage_ready:
            QMessageBox.warning(
                self,
                "Terrain editing unavailable",
                "The existing terrain file could not be loaded."
                "Resolve that error and restart before saving edits.",
            )
            return 

        try:
            self.map_view.save_map_definition(
                self.terrain_path, properties 
            )
        except (OSError, ValueError, TypeError) as error:
            QMessageBox.critical(
                self,
                "Terrain saving failed",
                str(error)
            )
            return 

        key = self.map_view.selected_hex_key
        reference = self.map_view.hexes[key]["game_reference"]

        self.statusBar().showMessage(
            f"Saved map information for {reference}"
        )

    def export_mapping_backup(self):
        print("Backup export clicked", flush = True)
        if self.map_view.brush_before is not None:
            QMessageBox.information(
                self,
                "Finish Painting",
                "Release the mouse to save the brush stroke "
                "before exporting.",
            )
            return 

        source_paths = [
            self.terrain_path,
            self.map_view.transport_path,
            project_dir / "campaign_grid_definitions.py",
            project_dir / "campaign_layout.py",
        ]

        if not self.terrain_path.is_file():
            QMessageBox.information(
                self, 
                "No saved terrain",
                "Save some terrain information before exporting.",
            )
            return 

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-S")

        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Export saved mapping information",
            str(project_dir / f"barbarossa_mapping_{timestamp}.zip"),
            "Mapping backups (*.zip)",
        )

        if not filename:
            return

        destination = Path(filename)

        if destination.suffix.lower() != ".zip":
            destionation = Path(str(destionation) + ".zip")

        temporary_path = None

        try:
            #Read saved files without changing the working data. 
            contents = {
                path.name : path.read_bytes()
                for path in source_paths 
                if path.is_file()
            }

            missing = [
                path.name
                for path in source_paths 
                if not path.is_file() 
            ]

            notes = (
                "TSWW Barbarossa mapping backup\n"
                f"Created {datetime.now().astimezone().isoformat()}\n\n"
                "Contains saved mapping data and grid definitions.\n"
                "Map images and campaign game saves are separate.\n\n"
                "Included:\n"
                + "\n".join(contents)
                + "\n\nMissing files:\n"
                + ("\n".join(missing) if missing else "None")
                + "\n"
            )

            #Create the complete archive before replacing the destionation.
            with NamedTemporaryFile(
                dir = destination.parent,
                prefix = "barbarossa_backup_",
                suffix = ".tmp",
                delete = False ,
            ) as temporary:
                temporary_path = Path(temporary.name)

            with ZipFile(
                temporary_path, "w", compression = ZIP_DEFLATED
            ) as archive:
                for name, content in contents.items():
                    archive.writestr(name, content)

                archive.writestr("BACKUP_README.txt", notes)

            with ZipFile(temporary_path, "r") as archive:
                bad_file = archive.testzip()

                if bad_file is not None:
                    raise ValueError(
                        f"Backup verification failed: {bad_file}"
                    )

            temporary_path.replace(destination)

        except (OSError, ValueError) as error:
            QMessageBox.critical(
                self, 
                "Backup Export Failed",
                str(error)
            )
            return

        finally:
            if temporary_path is not None:
                if temporary_path.exists():
                    temporary_path.unlink()

        self.statusBar().showMessage(
            f"Mapping backup exported: {destination.name}"
        )


        
def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()




if __name__ == "__main__":
    sys.exit(main())

