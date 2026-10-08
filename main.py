import sys
from pathlib import Path

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

        self.create_menus()
        self.statusBar().setVisible(True)
        self.statusBar().showMessage("Status bar ready- click the map")

    def create_menus(self):
        file_menu = self.menuBar().addMenu("File")

        open_action = QAction("Open Map...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_map)
        file_menu.addAction(open_action)

        campaign_action = QAction("Open Barbarossa Campaign", self)
        campaign_action.setShortcut("Ctrl + Shift + O")
        campaign_action.triggered.connect(self.open_campaign)
        file_menu.addAction(campaign_action)


        view_menu = self.menuBar().addMenu("View")

        fit_action = QAction("Fit Map to Window", self)
        fit_action.setShortcut("F")
        fit_action.triggered.connect(self.map_view.fit_map)
        view_menu.addAction(fit_action)

        jump_action = QAction("Jump to Counter", self)
        jump_action.setShortcut("J")
        jump_action.triggered.connect(self.map_view.jump_to_counter)
        view_menu.addAction(jump_action)

        save_action = QAction("Save Campaign...", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_campaign)
        file_menu.addAction(save_action)

        load_save_action = QAction("Load Campaign Save...", self)
        load_save_action.triggered.connect(self.load_campaign_save)
        file_menu.addAction(load_save_action)

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

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()




if __name__ == "__main__":
    sys.exit(main())

