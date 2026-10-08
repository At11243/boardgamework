import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from map_view import MapView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWidnowTitle("TSWW Barbarossa")
        self.resize(1200,800)