import json 

from pathlib import Path

from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QImageReader, QPainter, QPixmap, QTransform, QPen, QBrush, QPolygonF
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QApplication
from campaign_layout import barbarossa_boards

from campaign_grid_definitions import barbarossa_grids
from hex_model import hex_center, nearest_hex, printed_hex_number, nearest_hexside


class MapView(QGraphicsView):
    hex_selected = Signal(str, dict)
    edge_selected = Signal(int)

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
        self.hexes = {} 
        self.selected_hex_key = None 
        self.map_definitions = {}
        self.edge_pick_mode = False
        self.edge_highlight = None

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
        self.edge_highlight = None
        self.hex_selected.emit("", {})
        self.map_scene.clear()
        self.board_records = {}
        self.hexes = {} 
        self.selected_hex_key = None 
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
        self.edge_highlight = None
        self.hex_selected.emit("", {})
        self.map_scene.clear()
        self.map_item = None
        self.map_path = None
        self.original_size = None
        self.board_records = {}
        self.hexes = {} 
        self.selected_hex_key = None 

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
            self.edge_highlight = None
            self.hex_selected.emit("", {})
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
    def save_campaign(self, path):
        if not self.board_records:
            raise ValueError("Load the campaign before saving.")

        #JSON cannot use tuples as dictionary keys.
        #Store the key alongside each hex's properties instead
        hex_records = [
            {
                "key": list(key),
                "properties": properties
            }
            for key, properties in self.hexes.items()
        ]

        data = {
            "format" : "tsww-barbarossa-campaign",
            "version" : 1, 
            "boards" : list(self.board_records),
            "hexes" : hex_records,
            "selected_hex_key" : (
                list(self.selected_hex_key)
                if self.selected_hex_key is not None
                else None
            ),
        }

        path = Path(path)
        temporary_path = path.with_name(path.name + ".tmp")

        try: 
            temporary_path.write_text(
                json.dumps(data, indent = 2, ensure_ascii = False),
                encoding = "utf-8",
            )

            #Replace the destination after writing completes.
            temporary_path.replace(path)
        finally:
            if temporary_path.exists():
                temporary_path.unlink()


    def load_campaign_save(self, path, maps_dir):
        path = Path(path)

        try: 
            data = json.loads(path.read_text(encoding = "utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(
                "The save file contains invalid JSON."
            ) from error

        if not isinstance(data, dict):
            raise ValueError("Invalid campaign save.")

        if data.get("format") != "tsww-barbarossa-campaign":
            raise ValueError("This is not a Barbarossa campaign save.")

        if data.get("version") != 1:
            raise ValueError("This save version is not supported.")
        expected_boards = [
            board[0] for board in barbarossa_boards
        ]

        if data.get("boards") != expected_boards:
            raise ValueError("The save uses a different campaign layout.")

        records = data.get("hexes")

        if not isinstance(records, list):
            raise ValueError("The save is missing its hex records.")

        #Validate the saved data before replacing current campaign
        restored_hexes = {} 

        board_layout = {
            board_id: (x,y) 
            for board_id, filename, x, y, width, height 
            in barbarossa_boards
        }            

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Invalid hex record.")

            saved_key = record.get("key")
            properties = record.get("properties")

            if (
                not isinstance(saved_key, list)
                or len(saved_key) != 4
                or not isinstance(properties, dict)
            ):
                raise ValueError("Invalid hex key or properties.")

            board_id, region_name, column, row = saved_key

            if (
                not isinstance(board_id, str)
                or not isinstance(region_name, str)
                or type(column) is not int
                or type(row) is not int
                or board_id not in board_layout 
            ):
                raise ValueError("Invalid board or grid coordinates.")

            region = next(
                (
                    region 
                    for region in barbarossa_grids[board_id]["regions"]
                    if region["name"] == region_name
                ),
                None,
            )

            if region is None:
                raise ValueError(f"Unknown grid region: {region_name}")

            key = (board_id, region_name, column, row)

            if key in restored_hexes:
                raise ValueError("Duplicate hex record in the save.")

            local_x, local_y = hex_center(
                region["grid"], column, row
            )
            origin_x, origin_y = board_layout[board_id]

            number = printed_hex_number(region, column, row)

            #Preserve properties, but recalculate derived values
            restored = properties.copy()
            restored.update({
                "board_id" : board_id,
                "region" : region_name,
                "column" : column, 
                "row" : row,
                "printed_number" : number,
                "game_reference" : f"{region_name}:{number}",
                "center" : (origin_x + local_x , origin_y + local_y),
            })

            if not isinstance(restored.get("units"), list):
                raise ValueError("Invalid units list in a hex record.")

            restored_hexes[key] = restored

        #All hex records have now been restored.
        saved_selection = data.get("selected_hex_key")
        selected_key = None

        if saved_selection is not None:
            if (
                not isinstance(saved_selection, list)
                or len(saved_selection) != 4
                or not isinstance(saved_selection[0], str)
                or not isinstance(saved_selection[1], str)
                or type(saved_selection[2]) is not int
                or type(saved_selection[3]) is not int
                ):
                    raise ValueError("Invalid selected hex key.")

            selected_key = tuple(saved_selection)

            if selected_key not in restored_hexes:
                raise ValueError(
                    "The selected hex is missing from the save."
                )

            
        self.load_campaign(maps_dir)

        self.hexes = restored_hexes
        self.selected_hex_key = selected_key

        if selected_key is not None:
            board_id, region_name, column, row = selected_key

            selected_region = next(
                region for region in barbarossa_grids[board_id]["regions"]
                if region["name"] == region_name
            )

            display_properties = self.map_definitions.get(
                selected_key, {}
            ).copy()

            display_properties["_grid_sideways"] = (
                selected_region["grid"]["sideways"]
            )

            self.hex_selected.emit(
                self.hexes[selected_key]["game_reference"],
                display_properties,
            )
        else:
            self.hex_selected.emit("", {})

        if selected_key is not None:
            center_x, center_y = self.hexes[selected_key]["center"]
            self.debug_marker.setPos(center_x, center_y)
            self.centerOn(self.debug_marker)

        return len(self.hexes)



    def select_hex(self, event):
        if self.map_item is None:
            return 

        point = self.mapToScene(event.position().toPoint())

        if self.edge_pick_mode:
            if self.selected_hex_key is None:
                self.window().statusBar().showMessage(
                    "Turn off Pick Hex Edge and select a hex first."
                )
                return

            board_id, region_name, column, row = self.selected_hex_key

            region = next(
                region
                for region in barbarossa_grids[board_id]["regions"]
                if region["name"] == region_name
            )

            origin_x, origin_y = self.board_records[board_id]["origin"]

            center_x, center_y = hex_center(
                region["grid"], column, row
            )

            side, start, end = nearest_hexside(
                region["grid"],
                center_x,
                center_y,
                point.x() - origin_x,
                point.y() - origin_y,
            )

            #Ignore clicks far from the selected hex's edge
            start_x = origin_x + start[0]
            start_y = origin_y + start[1]
            end_x = origin_x + end[0]
            end_y = origin_y + end[1]

            vx = end_x - start_x 
            vy = end_y - start_y

            fraction = (
                (point.x() - start_x) * vx 
                + (point.y() - start_y) * vy
            ) / (vx * vx + vy * vy)

            fraction = max(0, min(1, fraction))

            closest_x = start_x + fraction * vx
            closest_y = start_y + fraction * vy

            click_position = event.position().toPoint()
            edge_position = self.mapFromScene(
                QPointF(closest_x, closest_y)
            )

            distance_squared = (
                (click_position.x() - edge_position.x()) ** 2 
                + (click_position.y() - edge_position.y()) ** 2 
            )

            if distance_squared > 20 ** 2: 
                self.window().statusBar().showMessage(
                    "Click near an edge of the selected hex."
                )
                return

            if self.edge_highlight is not None:
                self.map_scene.removeItem(self.edge_highlight)

            pen = QPen(Qt.GlobalColor.yellow)
            pen.setWidth(6) 
            pen.setCosmetic(True)

            self.edge_highlight = self.map_scene.addLine(
                start_x, start_y, end_x, end_y, pen
            )
            self.edge_highlight.setZValue(101)
            self.edge_selected.emit(side)

            self.window().statusBar().showMessage(
                f"{self.hexes[self.selected_hex_key]['game_reference']}"
                f" | Selected side {side}"
            )
            return 
        
        for board_id, record in self.board_records.items():
            origin_x, origin_y = record["origin"]
            width, height = record["size"]

            image_x = point.x() - origin_x 
            image_y = point.y() - origin_y

            if not (0 <= image_x < width and 0 <= image_y < height):
                continue

            board_definition = barbarossa_grids.get(board_id)

            if board_definition is None:
                return

            for region in board_definition["regions"]:
                boundary = QPolygonF([
                    QPointF(x,y)
                    for x,y in region["boundary"]
                ])

                if not boundary.containsPoint(
                    QPointF(image_x, image_y),
                    Qt.FillRule.OddEvenFill,
                ):
                    continue

                column, row, center_x, center_y = nearest_hex(
                    region["grid"], image_x, image_y
                )

                campaign_x = origin_x + center_x
                campaign_y = origin_y + center_y

                number = printed_hex_number(region, column, row)
                key = (board_id, region["name"], column, row)

                #Preserve existing properties when selecting again.
                if key not in self.hexes:
                    self.hexes[key] = {
                        "board_id" : board_id,
                        "region" : region["name"],
                        "column" : column,
                        "row" : row, 
                        "printed_number" : number,
                        "game_reference" : f"{region['name']}:{number}",
                        "center" : (campaign_x, campaign_y),
                        "terrain" : None,
                        "units" : [],
                    }

                self.selected_hex_key = key
                display_properties = self.map_definitions.get(
                    key, {}
                ).copy()

                display_properties["_grid_sideways"] = (
                    region["grid"]["sideways"]
                )

                self.hex_selected.emit(
                    self.hexes[key]["game_reference"],
                    display_properties,
                )

                self.debug_marker.setPos(campaign_x, campaign_y)

                self.centerOn(self.debug_marker)

                self.window().statusBar().showMessage(
                    f"{board_id} | {region['name']}:{number}"
                    f" | Grid ({column}, {row})"
                )
            
                return 

            self.window().statusBar().showMessage(
                f"{board_id} | No grid region at this position"
            )
            return 


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
            
    def load_map_definitions(self, path):
        path = Path(path)

        if not path.is_file():
            return

        data = json.loads(path.read_text(encoding="utf-8"))

        if (
            not isinstance(data, dict)
            or data.get("format") != "tsww-barbarossa-map-terrain"
            or data.get("version") != 1
            or not isinstance(data.get("hexes"), list)
        ):
            raise ValueError("Invalid map terrain file.")

        definitions = {}

        for record in data["hexes"]:
            if not isinstance(record, dict):
                raise ValueError("Invalid terrain record.")

            key = record.get("key")
            properties = record.get("properties")

            if (
                not isinstance(key, list)
                or len(key) != 4 
                or not isinstance(key[0], str)
                or not isinstance(key[1], str)
                or type(key[2]) is not int 
                or type(key[3]) is not int
                or not isinstance(properties, dict)
            ):
                raise ValueError("Invalid terrain key or properties.")

            terrain = properties.get("terrain")
            settlement = properties.get("settlement")

            if terrain is not None and (
                not isinstance(terrain, list)
                or not all(isinstance(value, str) for value in terrain)
            ):
                raise ValueError("Invalid terrain list.")

            if settlement is not None and (
                not isinstance(settlement, dict)
                or not isinstance(settlement.get("type"), str)
                or not isinstance(settlement.get("name"), str)
            ):
                raise ValueError("Invalid settlement information.")

            if properties.get("review_status", "Unknown") not in (
                "Unknown", "Suggested", "Verified"
            ):
                raise ValueError("Invalid reveiw status.")

            if properties.get("surface", "Unknown") not in (
                "Unknown",
                "Land",
                "Water",
                "Mixed land/water"
            ):
                raise ValueError("Invalid hex surface classification.")

            port = properties.get("port")

            if port is not None:
                if not isinstance(port, dict):
                    raise ValueError("Invalid port information.")

                if port.get("type") not in (
                    "Unknown", "None", "Great Port",
                    "Large Port", "General Port", "Small Port"
                ):
                    raise ValueError("Invalid port class.")

                if not isinstance(port.get("name"), str):
                    raise ValueError("Invalid port name.")

                for field in ("facilities", "anchorage"):
                    if port.get(field) not in (
                        "Unknown", "Absent", "Present"
                    ):
                        raise ValueError(f"Invalid port {field}.")

                for field in (
                    "naval_base_type",
                    "shipbuilding_capacity",
                ):
                    value = port.get(field)

                    if value is not None and not isinstance(value, str):
                        raise ValueError(f"Invalid port {field}.")

            hexsides = properties.get("hexsides", {})

            if not isinstance(hexsides, dict):
                raise ValueError("Invalid hexside information.")

            for side, values in hexsides.items():
                if side not in ("0", "1", "2", "3", "4", "5"):
                    raise ValueError("Invalid hexside number.")

                if not isinstance(values, dict):
                    raise ValueError("Invalid hexside record.")

                if values.get("waterway") not in (
                    "Unknown", "None", "Major River",
                    "Minor River", "Wadi", "Canal",
                ):
                    raise ValueError("Invalid waterway type.")

                if values.get("navigation") not in(
                    "Unknown", "Not navigable", "Navigable",
                ):
                    raise ValueError("Invalid navigation value.")

                if values.get("border") not in(
                    "Unknown", "None", "Internal Border",
                    "International Border", "Future Border"
                ):
                    raise ValueError("Invalid border type.")

                for field in (
                    "escarpment", 
                    "coastal_cliff",
                    "high_mountain",
                    ):
                    if values.get(field, "Unknown") not in (
                        "Unknown", "Absent", "Present"
                    ):
                        raise ValueError(f"Invalid hexside {field}.")

                if values.get("fortification", "Unknown") not in(
                    "Unknown",
                    "None",
                    "Fortifications",
                    "Major Fortifications"
                ):
                    raise ValueError("Invalid hexside fortification.")
            definitions[tuple(key)] = properties 

        self.map_definitions = definitions

    def save_map_definition(self, path, properties):
        key = self.selected_hex_key
        if key is None:
            raise ValueError("Select a hex first.")

        #Keep the existing definitions if writing fails.
        definitions = self.map_definitions.copy()
        updated = definitions.get(key, {}).copy()
        updated.update(properties)
        definitions[key] = updated

        data = {
            "format" : "tsww-barbarossa-map-terrain",
            "version" : 1,
            "hexes" : [
                {
                    "key" : list(hex_key),
                    "properties" : values,
                }
                for hex_key, values in definitions.items()
            ],
        }

        path = Path(path)
        temporary_path = path.with_name(path.name + ".tmp")

        try:
            temporary_path.write_text(
                json.dumps(data, indent = 2, ensure_ascii = False),
                encoding = "utf-8"
            )
            temporary_path.replace(path)
        finally:
            if temporary_path.exists():
                temporary_path.unlink()

        self.map_definitions = definitions

    def set_edge_pick_mode(self, enabled):
        self.edge_pick_mode = enabled

        if not enabled and self.edge_highlight is not None:
            self.map_scene.removeItem(self.edge_highlight)
            self.edge_highlight = None
    
                