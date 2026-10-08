from pathlib import Path

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QImageReader, QPainter, QPixmap, QTransform, QPen, QBrush
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QApplication
from campaign_layout import barbarossa_boards

from grid_definitions import barbarossa_grids
from hex_model import hex_center, nearest_hex


class MapView(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.map_scene = QGraphicsScene(self)
        self.setScene(self.map_scene)

        self.map_item = None
        self.map_path = None
        self.original_size = None
        self.board_records = {}
        self.debug_marker = None
        self.press_position = None
        self.drag_started = False

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

        
        image = reader.read()

        if image.isNull():
            raise ValueError(
                f"Cannot load the map:\n{reader.errorString()}"
            )

        pixmap = QPixmap.fromImage(image)

        if pixmap.isNull():
            raise ValueError("Could not create the map display image.")

        #Replace the previous map only after loading succeeds.
        self.debug_marker = None
        self.map_scene.clear()
        self.board_records = {}
        self.map_item = self.map_scene.addPixmap(pixmap)

        #Preserve original-image coordinates even with a preview. 
        scale_x = original_size.width() / image.width()
        scale_y = original_size.height() / image.height()

        self.map_item.setTransform(
            QTransform.fromScale(scale_x, scale_y)
        )

        self.map_scene.setSceneRect(
            QRectF(
                0,
                0,
                original_size.width(),
                original_size.height(),
            )
        )

        self.map_path = path
        self.original_size = original_size

        self.fit_map()

    def fit_map(self):
        if self.map_item is not None:
            self.fitInView(
                self.map_scene.sceneRect(),
                Qt.AspectRatioMode.KeepAspectRatio,
            )

    def jump_to_counter(self):
            marker = getattr(self, "debug_marker", None)
    
            if marker is None or marker.scene() is not self.map_scene:
                self.window().statusBar().showMessage(
                    "load the campaign to create the marker."
                )
                return 
    
            self.centerOn(marker)

    def wheelEvent(self, event):
        if self.map_item is None:
            super().wheelEvent(event)
            return

        delta = event.angleDelta().y()

        if delta == 0:
            event.ignore()
            return

        factor = 1.2 if delta > 0 else (1 / 1.2)
        proposed_scale = self.transform().m11() * factor

        #prevent zooming indefinitely in either direction.
        if 0.005 <= proposed_scale <= 8:
            self.scale(factor,factor)

        event.accept()

    def load_campaign(self, maps_dir):
        maps_dir = Path(maps_dir)

        #Check every file and its dimensions before loading. 
        for board_id, filename, x, y, width, height in barbarossa_boards:
            path = maps_dir / filename

            if not path.is_file():
                raise FileNotFoundError(
                    f"Missing campaign image:\n{path}"
                )

            reader = QImageReader(str(path))
            size = reader.size()

            if size.width() != width or size.height() != height:
                raise ValueError(
                    f"Unexpected dimensions for {filename}.\n"
                    f"Expected: {width} x {height}\n"
                    f"Found: {size.width()} x {size.height()}\n"
                    "Use the original Barbarossa image without resizing."
                )

        #Release the previous map before loading the campaign.
        self.debug_marker = None
        self.map_scene.clear()
        self.map_item = None
        self.map_path = None
        self.original_size = None
        self.board_records = {}

        QImageReader.setAllocationLimit(1024)

        try:
            for board_id, filename, x, y, width, height in barbarossa_boards:
                path = maps_dir / filename

                #Read at original resolution: no setScaledSize
                reader = QImageReader(str(path))
                print(f"Loading {filename}...", flush = True)
                image = reader.read()

                if image.isNull():
                    raise ValueError(
                        f"Cannot load {filename}:\n"
                        f"{reader.errorString()}"
                    )

                pixmap = QPixmap.fromImage(image)

                if pixmap.isNull():
                    raise ValueError(
                        f"Cannot create the display image for {filename}."
                    )

                item = self.map_scene.addPixmap(pixmap)
                item.setPos(x,y)
                print(f"Displayed {filename}", flush = True)

                self.board_records[board_id] = {
                    "filename" : filename,
                    "origin" : (x,y),
                    "size" : (width, height),
                    "item" : item,
                }

                # our existing fit_map method checks map_item
                if self.map_item is None:
                    self.map_item = item

                #The scene owns the pixmap item
                del image, pixmap

        except Exception:
            self.debug_marker = None
            self.map_scene.clear()
            self.map_item = None
            self.board_records = {}
            raise

        self.map_scene.setSceneRect(
            self.map_scene.itemsBoundingRect()
        )
        #Show one calculated hex center for alignment checking. 

        region = barbarossa_grids["Map 2"]["regions"][0]
        local_x, local_y = hex_center(region["grid"], 8, 45)

        origin_x, origin_y = self.board_records["Map 2"]["origin"]

        campaign_x = origin_x + local_x
        campaign_y = origin_y + local_y

        print(
            f"Marker : image = ({local_x:.1f}, {local_y:.1f}),"
            f"campaign=({campaign_x:.1f}, {campaign_y:.1f})",
            flush = True,
        )

        radius = 35

        marker = self.map_scene.addEllipse(
            -radius,
            -radius,
            radius * 2,
            radius * 2,
            QPen(Qt.GlobalColor.black),
            QBrush(Qt.GlobalColor.magenta),
        )
        marker.setPos(campaign_x, campaign_y)
        marker.setZValue(100)
        self.debug_marker = marker

        self.fit_map()

        #Temporarily zoom to the marker for this check. REMOVE LATER
        self.resetTransform()
        self.scale(1.5,1.5)
        self.centerOn(self.debug_marker)

        return len(self.board_records)

    def select_hex(self, event):
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.map_item is not None
        ):
            point = self.mapToScene(event.position().toPoint())

            message = (
                f"Campaign coordinates:"
                f"x = {point.x():.1f}, y = {point.y():.1f}"
            )

            #Identify the image containing this position
            for board_id, record in self.board_records.items():
                origin_x, origin_y = record["origin"]
                width, height = record["size"]

                if (
                    origin_x <= point.x() < origin_x + width
                    and origin_y <= point.y() < origin_y + height
                ):
                    message += (
                        f" | {board_id}"
                        f" | Image coordinates:"
                        f"x = {point.x() - origin_x:.1f}, "
                        f"y = {point.y() - origin_y:.1f}"
                    )

                    if board_id == "Map 2":
                        region = barbarossa_grids["Map 2"]["regions"][0]

                        image_x = point.x() - origin_x 
                        image_y = point.y() - origin_y

                        #Only use this grid inside its region
                        from PySide6.QtCore import QPointF
                        from PySide6.QtGui import QPolygonF

                        boundary = QPolygonF([
                            QPointF(x,y)
                            for x,y in region["boundary"]
                        ])

                        print(
                            f"Click: image=({image_x:.1f}, {image_y:.1f})"
                        )
                        if boundary.containsPoint(
                            QPointF(image_x, image_y),
                            Qt.FillRule.OddEvenFill,
                        ):
                            column, row, center_x, center_y = nearest_hex(
                                region["grid"], image_x, image_y
                            )
                            
                            self.debug_marker.setPos(
                                origin_x + center_x, 
                                origin_y + center_y
                            )

                            self.centerOn(self.debug_marker)

                            message += (
                                f" |{region['name']}"
                                f" | Grid ({column}, {row})"
                            )
                    break
            
            self.window().statusBar().showMessage(message)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.press_position = event.position().toPoint()
            self.drag_started = False

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.press_position is not None:
            position = event.position().toPoint()
            distance = (
                position - self.press_position
            ).manhattanLength()

            if distance >= QApplication.startDragDistance():
                self.drag_started = True

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        should_select = (
            event.button() == Qt.MouseButton.LeftButton
            and self.press_position is not None
            and not self.drag_started
            and (
                event.position().toPoint() - self.press_position
            ).manhattanLength() < QApplication.startDragDistance()
        )

        #Finish panning before selecting and centering a hex.
        super().mouseReleaseEvent(event)

        self.press_position = None
        self.drag_started = False 

        if should_select:
            self.select_hex(event)
            

    
                