from pathlib import Path

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QImageReader, QPainter, QPixmap, QTransform
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView


class MapView(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.map_scene = QGraphicsScene(self)
        self.setScene(self.map_scene)

        self.map_item = None
        self.map_path = None
        self.original_size = None

        #Drag the map by holding the left mouse button.
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        #Keep the point under the cursor steady when zooming.
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setBackgroundBrush(Qt.GlobalColor.darkGray)

    def load_map(self, path):
        path = Path(path)

        if not path.is_file():
            raise FileNotFoundError(f"Map file not found:\n{path}")

        #The supplied maps are large, so allow their decoding.
        QImageReader.setAllocationLimit(1024)

        reader = QImageReader(str(path))
        original_size = reader.size()

        if not original_size.isValid():
            raise ValueError(
                f"Cannot read the map dimensions:\n{reader.errorString()}"
            )

        #Start with a managable preview.
        #We will add detailed map tiles later.
        if max(original_size.width(), original_size.height()) > 4096:
            preview_size = original_size.scaled(
                4096,
                4096,
                Qt.AspectRatioMode.KeepAspectRatio,
            )
            reader.setScaledSize(preview_size)

        image = reader.read()

        if image.isNull():
            raise ValueError(
                f"Cannot load the map:\n{reader.errorString()}"
            )

        pixmap = QPixmap.fromImage(image)

        if pixmap.isNull():
            raise ValueError("Could not create the map display image.")

        #Replace the previous map only after loading succeeds.
        self.map_scene.clear()
        self.map_item = self.map_scene.addPixmap(pixmap)

        #Preserve original-image coordinates even with a preview. 
        scale_x = original_size.width() / image.width()
        scale_y = original_size.height() / image.height()

        self.map_item.setTransform(
            QTransofrm.fromScale(scale_x, scale_y)
        )

        self.map_scene.setSceneRect(
            QRectF(
                0,
                0,
                original_size.width(),
                original_size.height(),
            )
        )