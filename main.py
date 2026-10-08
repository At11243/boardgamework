import sys
from pathlib import Path

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow,
    QFileDialog,
    QMessageBox,
)

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
        self.board_records = {}

        self.create_menus()
        self.statusBar().showMessage("Choose File -> Open Map")

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




def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())