import json 
from copy import deepcopy

from pathlib import Path

from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import (
    QImageReader, 
    QPainter, 
    QPixmap, 
    QTransform, 
    QPen, 
    QBrush, 
    QPolygonF, 
    QColor,
    QShortcut,
    QPainterPath,
)
from PySide6.QtWidgets import (
    QGraphicsScene, 
    QGraphicsView, 
    QApplication,
    QMessageBox 
)
from maps.campaign_layout import barbarossa_boards

from maps.campaign_grid_definitions import barbarossa_grids
from maps.hex_model import (
    hex_center, 
    nearest_hex, 
    printed_hex_number, 
    nearest_hexside,
    hex_vertices,
    is_playable_hex,
)

from maps.mapping_support import(
    merge_records,
    normalize_campaign,
    synchronize_sides,
    audit_sides,
)
from maps.mapping_fields import validate_extra_fields
from uuid import uuid4
from counters.counter_state import restore_units, stack_ids
from counters.counter_faces import face_pixmap, flipped_instance
from game.action_history import empty_history, append_action, append_event, restore_history, EVENT_ACTIONS
from rules import DiceService, validate_attack_result
from rules.sides import default_setup, validate_setup
from game.nation_roster import initial_roster

class MapView(QGraphicsView):
    hex_selected = Signal(str, dict)
    edge_selected = Signal(int)
    transport_summary_changed = Signal(str)
    stack_changed = Signal()
    history_changed = Signal()

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
        self.hexes = {} # Store hex information
        self.units = {} #Store unit information
        self.unit_items = {} #Store graphic objects separately from units
        self.selected_unit_id = None
        self.moving_unit_id = None
        self.cancel_move_shortcut = QShortcut("Escape", self)
        self.cancel_move_shortcut.setEnabled(False)
        self.cancel_move_shortcut.activated.connect(self.cancel_counter_move)
        self.unit_highlight = None
        self.campaign_metadata = {}
        self.action_history = empty_history()
        self.player_setup = default_setup(initial_roster())
        self.dice_service = DiceService()
        self.counter_project_dir = Path(__file__).resolve().parents[1]
        self.hex_selected.connect(self.refresh_counter_selection)
        self.selected_hex_key = None 
        self.map_definitions = {}
        self.excluded_map_definitions = {}
        self.terrain_brush_enabled = False 
        self.terrain_brush_properties = {}
        self.terrain_brush_path = None 
        self.brush_before = None 
        self.brush_touched = set()
        self.brush_undo = None 
        self.edge_pick_mode = False
        self.edge_highlight = None
        self.review_overlay_enabled = False
        self.transport_review_overlay_enabled = False
        self.transport_review_overlay_enabled = False
        self.join_markers = []
        self.transport_draw_mode = False 
        self.transport_draw_type = "Tarmac Road"
        self.transport_anchor = None 
        self.transport_segments = {} 
        self.excluded_transport_connections = []
        self.transport_erase_mode = False 

        self.transport_path = Path(__file__).resolve().parents[1] / "map_transport.json"

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

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
        self.join_markers = []
        self.transport_anchor = None 
        self.transport_segments = {}
        self.hex_selected.emit("", {})
        self.reset_counter_selection()
        self.map_scene.clear()
        self.board_records = {}
        self.hexes = {} 
        self.units = {} 
        self.unit_items = {}
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
        self.join_markers = []
        self.transport_anchor = None 
        self.transport_segments = {} 
        self.hex_selected.emit("", {})
        self.reset_counter_selection()
        self.map_scene.clear()
        self.map_item = None
        self.map_path = None
        self.original_size = None
        self.board_records = {}
        self.hexes = {} 
        self.units = {}
        self.unit_items = {}
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
            self.join_markers = []
            self.transport_anchor = None 
            self.transport_segments = {} 
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
        self.load_transport_connections()

        return len(self.board_records)

    def place_counter(self, counter):
        if self.moving_unit_id is not None:
            raise ValueError("Finish or cancel the move before placing another counter.")
        if (
            not self.board_records
            or self.selected_hex_key is None
        ):
            raise ValueError(
                "Load the campaign and select a hex first."
            )

        if self.terrain_brush_enabled or self.transport_draw_mode:
            raise ValueError(
                "Turn off terrain painting and transport drawing "
                "before placing counters."
            )

        key = self.canonical_hex_key(self.selected_hex_key)

        project_dir = Path(__file__).resolve().parents[1]
        image_path = project_dir / counter["image_path"]

        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():
            raise ValueError(
                f"Cannot load counter image:\n{image_path}"
            )

        grid, center_x, center_y = self.hex_key_geometry(key)

        unit_id = uuid4().hex

        #Store ordinary data separately from the graphics item.
        self.units[unit_id] = {
            "unit_id": unit_id,
            "type_id": counter["type_id"],
            "name": counter["name"],
            "image_path": counter["image_path"],
            "hex_key": key,
            # Placement currently chooses an imported image, not a reviewed face.
            "active_face": "unassigned",
            "stack_order": max((u["stack_order"] for u in self.units.values()
                                if u["hex_key"] == key), default=-1) + 1,
        }

        self.render_counter(unit_id, pixmap)
        self.layout_stack(key)
        self.select_unit(unit_id)
        self.record_counter_action("place", None, self.units[unit_id],
                                   f"Placed {counter['name']} at {self.hex_reference(key)}")
        self.window().statusBar().showMessage(
            f"Placed {counter['name']} on "
            f"{self.hexes[self.selected_hex_key]['game_reference']}"
        )
        return unit_id

    def render_counter(self, unit_id, pixmap):
        unit = self.units[unit_id]
        grid, center_x, center_y = self.hex_key_geometry(unit["hex_key"])

        item = self.map_scene.addPixmap(pixmap)

        item.setOffset(
            -pixmap.width() / 2,
            -pixmap.height() / 2,
        )

        #Display width in original campaign-image pixels.
        item.setScale(80 / pixmap.width())
        item.setPos(center_x, center_y)
        item.setZValue(200)

        item.setTransformationMode(
            Qt.TransformationMode.SmoothTransformation
        )

        #Keep ordinary map selection working beneath the counter.
        item.setAcceptedMouseButtons(Qt.MouseButton.NoButton)

        self.unit_items[unit_id] = item
        item.setData(0, unit_id)
        item.setToolTip(unit["name"])

    def layout_stack(self, key):
        ids = stack_ids(self.units, key)
        _, x, y = self.hex_key_geometry(key)
        for index, uid in enumerate(ids):
            # A small fan exposes the stack without spreading across the hex.
            offset = min(index, 5) * 6
            self.unit_items[uid].setPos(x + offset, y - offset)
            self.unit_items[uid].setZValue(200 + index * 0.001)

    def reset_counter_selection(self):
        self.moving_unit_id = None
        self.cancel_move_shortcut.setEnabled(False)
        if self.unit_highlight is not None:
            self.map_scene.removeItem(self.unit_highlight)
            self.unit_highlight = None
        self.selected_unit_id = None
        self.campaign_metadata = {}
        self.units = {}
        self.unit_items = {}
        self.action_history = empty_history()
        self.player_setup = default_setup(initial_roster())
        self.history_changed.emit()
        self.stack_changed.emit()

    def refresh_counter_selection(self, *_):
        if (self.selected_unit_id in self.units
                and self.units[self.selected_unit_id]["hex_key"] != self.selected_hex_key):
            self.select_unit(None)
        self.stack_changed.emit()

    def select_unit(self, unit_id):
        if unit_id is not None and unit_id not in self.units:
            return
        if self.unit_highlight is not None:
            self.map_scene.removeItem(self.unit_highlight)
            self.unit_highlight = None
        self.selected_unit_id = unit_id
        if unit_id is not None:
            item = self.unit_items[unit_id]
            # Draw the outline above the stack without changing stack order.
            rect = item.sceneBoundingRect()
            self.unit_highlight = self.map_scene.addRect(rect, QPen(QColor("yellow"), 3))
            self.unit_highlight.setZValue(201)
            self.unit_highlight.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        self.stack_changed.emit()

    def flip_unavailable_reason(self):
        if self.moving_unit_id is not None:
            return "Finish or cancel the counter move before flipping."
        if self.selected_unit_id not in self.units:
            return "Select a counter to flip."
        if self.terrain_brush_enabled or self.transport_draw_mode or self.edge_pick_mode:
            return "Turn off terrain painting, transport drawing, and edge picking before flipping."
        try:
            flipped_instance(self.units[self.selected_unit_id], self.counter_project_dir)
        except ValueError as error:
            return str(error)
        return ""

    def flip_selected_counter(self, *_):
        reason = self.flip_unavailable_reason()
        if reason:
            self.window().statusBar().showMessage(reason)
            return False
        uid = self.selected_unit_id
        # Resolve and render completely before changing the current instance.
        try:
            updated, pixmap = flipped_instance(self.units[uid], self.counter_project_dir)
        except ValueError as error:
            self.window().statusBar().showMessage(str(error))
            return False
        before = deepcopy(self.units[uid])
        self.units[uid] = updated
        item = self.unit_items[uid]
        item.setPixmap(pixmap)
        item.setOffset(-pixmap.width() / 2, -pixmap.height() / 2)
        item.setScale(80 / pixmap.width())
        self.select_unit(uid)
        self.record_counter_action("flip", before, updated,
                                   f"Flipped {updated['name']} to {updated['active_face']}")
        self.window().statusBar().showMessage(
            f"Flipped {updated['name']} to {updated['active_face']} | No gameplay effects applied"
        )
        return True

    def move_unavailable_reason(self):
        if self.moving_unit_id is not None:
            return "Click a destination hex. Cancel Move or press Escape to cancel."
        if self.selected_unit_id not in self.units:
            return "Select a counter to move."
        if self.terrain_brush_enabled or self.transport_draw_mode or self.edge_pick_mode:
            return "Turn off mapping modes before moving counters."
        return ""

    def begin_counter_move(self, *_):
        reason = self.move_unavailable_reason()
        if reason:
            self.window().statusBar().showMessage(reason)
            return False
        self.moving_unit_id = self.selected_unit_id
        self.cancel_move_shortcut.setEnabled(True)
        self.setFocus()
        self.stack_changed.emit()
        self.window().statusBar().showMessage(
            "Click a destination hex | Escape to cancel | Movement costs and legality are manual"
        )
        return True

    def cancel_counter_move(self, *_):
        if self.moving_unit_id is None:
            return
        self.moving_unit_id = None
        self.cancel_move_shortcut.setEnabled(False)
        self.stack_changed.emit()
        self.window().statusBar().showMessage("Counter move cancelled.")

    def finish_counter_move(self, destination):
        uid = self.moving_unit_id
        if uid not in self.units:
            return False
        if self.terrain_brush_enabled or self.transport_draw_mode or self.edge_pick_mode:
            self.cancel_counter_move()
            return False
        destination = self.canonical_hex_key(destination)
        if destination not in self.hexes:
            raise ValueError("Select a campaign hex before moving.")
        unit = self.units[uid]
        before = deepcopy(unit)
        source = unit["hex_key"]
        if source != destination:
            unit["stack_order"] = max(
                (u["stack_order"] for u in self.units.values() if u["hex_key"] == destination),
                default=-1,
            ) + 1
            unit["hex_key"] = destination
            self.layout_stack(source)
            self.layout_stack(destination)
        self.moving_unit_id = None
        self.cancel_move_shortcut.setEnabled(False)
        self.selected_hex_key = destination
        self.select_unit(uid)
        self.record_counter_action(
            "move", before, unit,
            f"Moved {unit['name']} from {self.hex_reference(source)} to {self.hex_reference(destination)}"
        )
        self.window().statusBar().showMessage(
            f"Moved {unit['name']} to {self.hexes[destination]['game_reference']}"
            " | Movement costs and legality are manual"
        )
        return True

    def hex_reference(self, key):
        return self.hexes.get(key, {}).get("game_reference", str(key))

    def record_counter_action(self, kind, before, after, description):
        append_action(self.action_history, kind, before, after, description)
        self.history_changed.emit()

    def history_blocked(self):
        return bool(self.moving_unit_id is not None or self.terrain_brush_enabled
                    or self.transport_draw_mode or self.edge_pick_mode)

    def record_dice_roll(self, roll_type, *, controller="human", manual_faces=None, purpose="", rng=None):
        if not self.board_records or self.history_blocked():
            raise ValueError("Load a campaign and finish movement/mapping before recording dice.")
        service = self.dice_service if rng is None else DiceService(rng=rng)
        record = service.roll(roll_type, controller=controller, manual_faces=manual_faces,
                              purpose=purpose)
        append_event(self.action_history, "dice_roll", record,
                     f"{roll_type}: {record['value']} ({record['method']})"
                     + (f" - {record['purpose']}" if record["purpose"] else ""))
        self.history_changed.emit()
        return record

    def record_attack_result(self, record):
        """Future combat/AAR entry point; records results without changing units."""
        if not self.board_records or self.history_blocked():
            raise ValueError("Load a campaign and finish movement/mapping before recording results.")
        record = validate_attack_result(record)
        # Historical participants can later be eliminated; snapshots are not fabricated.
        key = self.canonical_hex_key(record["target_hex"])
        if key not in self.hexes:
            raise ValueError("Attack target is not recorded in the campaign.")
        record["target_hex"] = list(key)
        append_event(self.action_history, "attack_result", record,
                     f"Attack at {self.hex_reference(key)}: {record['result']} (manual)")
        self.history_changed.emit()
        return record

    def can_undo_counter_action(self):
        return not self.history_blocked() and self.action_history["cursor"] > 0

    def can_redo_counter_action(self):
        return (not self.history_blocked()
                and self.action_history["cursor"] < len(self.action_history["entries"]))

    def undo_counter_action(self, *_):
        return self.apply_history_action(False)

    def redo_counter_action(self, *_):
        return self.apply_history_action(True)

    def apply_history_action(self, redo):
        available = self.can_redo_counter_action() if redo else self.can_undo_counter_action()
        if not available:
            return False
        cursor = self.action_history["cursor"]
        entry = self.action_history["entries"][cursor if redo else cursor - 1]
        if entry["kind"] in EVENT_ACTIONS:
            # Results are stored facts: redo reactivates the record, never rerolls.
            self.action_history["cursor"] += 1 if redo else -1
            self.history_changed.emit()
            self.window().statusBar().showMessage(
                f"{'Redid' if redo else 'Undid'} record: {entry['description']}"
            )
            return True
        uid = entry["unit_id"]
        expected = entry["before"] if redo else entry["after"]
        target = deepcopy(entry["after"] if redo else entry["before"])
        if self.units.get(uid) != expected:
            self.window().statusBar().showMessage("Cannot apply history: counter state has changed.")
            return False
        # Missing artwork must not partially apply an Undo/Redo.
        try:
            pixmap = face_pixmap(target, self.counter_project_dir) if target else None
        except ValueError as error:
            self.window().statusBar().showMessage(str(error))
            return False
        affected = {snapshot["hex_key"] for snapshot in (expected, target) if snapshot}
        self.select_unit(None)
        if uid in self.unit_items:
            self.map_scene.removeItem(self.unit_items.pop(uid))
        self.units.pop(uid, None)
        if target is not None:
            self.units[uid] = target
            self.render_counter(uid, pixmap)
        for key in affected:
            self.layout_stack(key)
        key = (target or expected)["hex_key"]
        self.selected_hex_key = key
        properties = self.map_definitions.get(key, {}).copy()
        properties["_grid_sideways"] = self.hex_key_geometry(key)[0]["sideways"]
        self.hex_selected.emit(self.hex_reference(key), properties)
        _, x, y = self.hex_key_geometry(key)
        if self.debug_marker is not None:
            self.debug_marker.setPos(x, y)
        self.select_unit(uid if target else None)
        self.action_history["cursor"] += 1 if redo else -1
        self.history_changed.emit()
        self.window().statusBar().showMessage(
            f"{'Redid' if redo else 'Undid'}: {entry['description']}"
        )
        return True
    
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
            **self.campaign_metadata,
            "format" : "tsww-barbarossa-campaign",
            "version" : 1, 
            "units": list(self.units.values()),
            "action_history": self.action_history,
            "player_setup": validate_setup(self.player_setup),
            "selected_unit_id": self.selected_unit_id,
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

        restored_hexes = normalize_campaign(
            self, restored_hexes
        )
        
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

            selected_key = self.canonical_hex_key(
                saved_selection
            )

            if selected_key not in restored_hexes:
                raise ValueError(
                    "The selected hex is missing from the save."
                )

            
        try:
            restored_units = restore_units(
                data.get("units", []), self.canonical_hex_key, restored_hexes
            )
        except (KeyError, TypeError, StopIteration) as error:
            raise ValueError("Invalid counter board or grid region.") from error
        restored_pixmaps = {}
        for uid, unit in restored_units.items():
            pixmap = face_pixmap(unit, self.counter_project_dir)
            restored_pixmaps[uid] = pixmap
        selected_unit = data.get("selected_unit_id")
        if (selected_unit is not None
                and (not isinstance(selected_unit, str) or selected_unit not in restored_units)):
            raise ValueError("Invalid selected counter instance.")
        if selected_unit is not None and restored_units[selected_unit]["hex_key"] != selected_key:
            raise ValueError("Selected counter does not belong to the selected hex.")

        restored_history = restore_history(data.get("action_history"), restored_units,
                                           self.canonical_hex_key, restored_hexes)
        # Validate every stored face assignment before replacing the campaign.
        for entry in restored_history["entries"]:
            for snapshot in (entry["before"], entry["after"]):
                if snapshot is not None:
                    face_pixmap(snapshot, self.counter_project_dir)

        restored_setup = (validate_setup(data["player_setup"]) if "player_setup" in data
                          else default_setup(initial_roster()))
        self.load_campaign(maps_dir)

        self.hexes = restored_hexes
        self.selected_hex_key = selected_key
        self.campaign_metadata = {key: value for key, value in data.items()
                                  if key not in ("format", "version", "boards", "hexes",
                                                 "units", "selected_hex_key", "selected_unit_id",
                                                 "action_history", "player_setup")}
        self.units = restored_units
        self.player_setup = restored_setup
        self.action_history = restored_history
        self.history_changed.emit()
        for uid, pixmap in restored_pixmaps.items():
            self.render_counter(uid, pixmap)
        for key in {unit["hex_key"] for unit in self.units.values()}:
            self.layout_stack(key)
        self.select_unit(selected_unit)

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

        if self.moving_unit_id is not None:
            # Normal hex picking handles canonical joins and creates an unrecorded hex.
            if self.select_campaign_point(point):
                self.finish_counter_move(self.selected_hex_key)
            else:
                self.window().statusBar().showMessage(
                    "Choose a playable destination hex, or press Escape to cancel."
                )
            return

        if self.transport_draw_mode:
            self.draw_transport_to(point)
            return 
        
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
         
        # Preserve mapping modes and drag-to-pan; only plain clicks pick counters.
        for item in self.map_scene.items(point):
            uid = item.data(0)
            if isinstance(uid, str) and uid in self.units:
                _, x, y = self.hex_key_geometry(self.units[uid]["hex_key"])
                self.select_campaign_point(QPointF(x, y))
                self.select_unit(uid)
                return
        self.select_unit(None)
        self.select_campaign_point(point)

    def set_terrain_brush(self, enabled, properties):
        if enabled:
            self.cancel_counter_move()
        self.terrain_brush_enabled = enabled
        self.stack_changed.emit()
        self.terrain_brush_properties = {
            "terrain" : list(properties["terrain"]),
            "surface" : properties["surface"],
            "review_status" : "Verified",
        }

        self.setDragMode(
            QGraphicsView.DragMode.NoDrag 
            if enabled 
            else QGraphicsView.DragMode.ScrollHandDrag 
        )

        self.window().statusBar().showMessage(
            "Terrain brush : drag to paint; release to save."
            if enabled
            else "Terrain brush off."
        )

    def paint_terrain_point(self, point):
        record = self.find_hex_at(point)

        if record is None:
            return 

        key = self.canonical_hex_key(record["key"])

        if key in self.brush_touched: 
            return 

        self.brush_touched.add(key)

        updated = self.map_definitions.get(key, {}).copy()
        updated.update(self.terrain_brush_properties)
        self.map_definitions[key] = updated

        self.viewport().update()

    def write_terrain_records(self, definitions):
        if self.terrain_brush_path is None:
            raise ValueError("The terrain save path is not configured.")

        path = Path(self.terrain_brush_path)
        temporary = path.with_name(path.name + ".tmp")

        records_to_save = self.excluded_map_definitions.copy()
        records_to_save.update(definitions)
        
        data = {
            "format" : "tsww-barbarossa-map-terrain",
            "version" : 1,
            "hexes" : [
                {
                    "key" : list(key),
                    "properties" : properties 
                }
                for key, properties in records_to_save.items()
            ],
        }

        try:
            temporary.write_text(
                json.dumps(data, indent = 2, ensure_ascii = False),
                encoding = "utf-8",
            )
            temporary.replace(path)
        finally:
            if temporary.exists():
                temporary.unlink()

    def refresh_selected_terrain(self): 
        key = self.selected_hex_key

        if key is None or key not in self.hexes:
            return 

        properties = self.map_definitions.get(key, {}).copy()
        grid, _, _ = self.hex_key_geometry(key)
        properties["_grid_sideways"] = grid["sideways"]

        self.hex_selected.emit(
            self.hexes[key]["game_reference"],
            properties,
        )

    def finish_terrain_stroke(self):
        before = self.brush_before
        count = len(self.brush_touched)
        self.brush_before = None
        self.brush_touched = set()

        if before is None or count == 0:
            return 

        try: 
            self.write_terrain_records(self.map_definitions)
        except (OSError, ValueError, TypeError) as error:
            self.map_definitions = before
            QMessageBox.critical(
                self,
                "Brush saving failed",
                str(error),
            )
        else:
            self.brush_undo = before
            self.window().statusBar().showMessage(
                f"Painted, verified, and saved {count} hexes."
            )

        self.refresh_selected_terrain()
        self.viewport().update()

    def undo_terrain_brush(self):
        if self.brush_before is not None:
            return 

        if self.brush_undo is None:
            self.window().statusBar().showMessage(
                "No brush stroke to undo."
            )
            return 

        try: 
            self.write_terrain_records(self.brush_undo)
        except (OSError, ValueError, TypeError) as error:
            QMessageBox.critical(
                self,
                "Brush undo failed",
                str(error),
            )
            return 

        self.map_definitions = self.brush_undo
        self.brush_undo = None 
        self.refresh_selected_terrain()
        self.viewport().update()

        self.window().statusBar().showMessage(
            "Last brush stroke undone and saved."
        )

    def mousePressEvent(self, event):
        if (
            self.terrain_brush_enabled
            and event.button() == Qt.MouseButton.LeftButton
        ):
            if not self.board_records:
                self.window().statusBar().showMessage(
                    "Load the campaign before painting."
                )
                event.accept()
                return 

            self.setFocus()
            self.brush_before = self.map_definitions.copy()
            self.brush_touched = set()

            self.paint_terrain_point(
                self.mapToScene(event.position().toPoint())
            )
            event.accept()
            return 
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.setFocus()
            self.press_position = event.position().toPoint()
            self.drag_started = False

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.brush_before is not None:
            self.paint_terrain_point(
                self.mapToScene(event.position().toPoint())
            )
            event.accept()
            return 

        if self.press_position is not None:
            position = event.position().toPoint()
            distance = (
                position - self.press_position
            ).manhattanLength()

            if distance >= QApplication.startDragDistance():
                self.drag_started = True

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if (
            self.brush_before is not None
            and event.button() == Qt.MouseButton.LeftButton
        ):
            self.paint_terrain_point(
                self.mapToScene(event.position().toPoint())
            )
            self.finish_terrain_stroke()
            event.accept()
            return 

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
        excluded_definitions = {}

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
                "Unknown", "Suggested", "In progress", "Verified"
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

            validate_extra_fields(properties)

            if not is_playable_hex(
                key[0], key[1], key[2], key[3]
            ):
                excluded_key = tuple(key)
                excluded_definitions[excluded_key] = merge_records(
                    excluded_definitions.get(excluded_key, {}),
                    properties, 
                    str(excluded_key),
                )
                continue 

            shared_key = self.canonical_hex_key(key)

            definitions[shared_key] = merge_records(
                definitions.get(shared_key, {}),
                properties,
                str(shared_key),
            )

        self.map_definitions = definitions
        self.excluded_map_definitions = excluded_definitions

    def save_map_definition(self, path, properties):
        key = self.selected_hex_key

        if key is None:
            raise ValueError("Select a hex first.")

        key = self.canonical_hex_key(key)
        validate_extra_fields(properties)

        previous = self.map_definitions.get(key, {})

        definitions = self.map_definitions.copy()
        updated = previous.copy()
        updated.update(properties)
        definitions[key] = updated

        definitions = synchronize_sides(
            self, 
            definitions,
            key,
            previous,
        )

        #Use the same atomic writer as the brush.
        self.terrain_brush_path = Path(path)
        self.write_terrain_records(definitions)

        #Update memory only after the file is saved.
        self.map_definitions = definitions
        self.brush_undo = None
        self.refresh_selected_terrain()
        self.viewport().update()

    def transport_pen(self, transport_type):
        styles = {
            "Tarmac Road" : ('#FFD54F', 7, Qt.PenStyle.SolidLine),
            "Gravel Road" : ("#FF9800", 5, Qt.PenStyle.DashLine),
            "Track" : ("#FF9800", 3, Qt.PenStyle.DotLine),
            "High Capacity Railway": (
                "#00E5FF", 3 , Qt.PenStyle.SolidLine
            ),
            "Low Capacity Railway" : (
                "#00E5FF", 3, Qt.PenStyle.DashLine
            ),
            "Broad Gauge High Cap RR" : (
                "#E040FB", 3, Qt.PenStyle.SolidLine
            ),
            "Broad Gauge Low Cap RR" : (
                "#E040FB", 3, Qt.PenStyle.DashLine
            ),
            "High Capacity Ferry" : (
                "#76FF03", 5, Qt.PenStyle.DashLine
            ),
            "Ferry" : ("#76FF03", 3, Qt.PenStyle.DotLine),
        }

        color, width, style = styles[transport_type]
        pen = QPen(QColor(color))
        pen.setWidthF(width)
        pen.setStyle(style)
        pen.setCosmetic(True)
        return pen

    def refresh_transport_summary(self, *_):
        key = self.selected_hex_key

        if key is None:
            self.transport_summary_changed.emit("Select a hex.")
            return

        key = self.canonical_transport_key(key)

        connections = [] 

        for segment in self.transport_segments.values(): 
            if segment["source_key"] == key:
                side = segment["source_side"]
                other_key = segment["target_key"]
            elif segment["target_key"] == key:
                side = segment["target_side"]
                other_key = segment["source_key"]
            else:
                continue

            board_id, region_name, column, row = other_key

            region = next(
                entry
                for entry in barbarossa_grids[board_id]["regions"]
                if entry["name"] == region_name
            )

            number = printed_hex_number(region, column, row)

            connections.append(
                f"Side {side} : {segment['type']}"
                f" -> {board_id} : {region_name}:{number}"
            )

        self.transport_summary_changed.emit(
            "\n".join(sorted(connections))
            if connections
            else "No transport connections recorded."
        )

    def set_transport_erase_mode(self, enabled):
        self.transport_erase_mode = enabled
        self.transport_anchor = None

        self.window().statusBar().showMessage(
            "Erase mode: click both ends of a connection."
            if enabled
            else "Draw mode: click a starting hex."
        )

    def save_transport_connections(self):
        data = {
            "format" : "tsww-barbarossa-transport",
            "version" : 1,
            "connections" : [
                {
                    "source_key" : list(segment["source_key"]),
                    "source_side" : segment["source_side"],
                    "target_key" : list(segment["target_key"]),
                    "target_side" : segment["target_side"],
                    "type" : segment["type"],
                }
                for segment in self.transport_segments.values()
            ],
        }

        data["connections"].extend(
            self.excluded_transport_connections
        )

        temporary_path = self.transport_path.with_name(
            self.transport_path.name + ".tmp"
        )

        try: 
            temporary_path.write_text(
                json.dumps(data, indent = 2, ensure_ascii = False),
                encoding = "utf-8",
            )
            temporary_path.replace(self.transport_path)
        finally: 
            if temporary_path.exists():
                temporary_path.unlink()

    def canonical_hex_key(self, key):
        """Give matching physical hexes one shared key."""


        grid, campaign_x, campaign_y = self.hex_key_geometry(key)
        key = tuple(key)


        candidates = [key]

        for (
            board_id, filename, origin_x, origin_y, width, height
        ) in barbarossa_boards:

            image_x = campaign_x - origin_x 
            image_y = campaign_y - origin_y

            if not (
                0 <= image_x < width
                and 0 <= image_y < height
            ):
                continue
            for region in barbarossa_grids[board_id]["regions"]:
                column, row, center_x, center_y = nearest_hex(
                    region["grid"], image_x, image_y  
                )

                tolerance = min(
                    grid["dx"],
                    grid["dy"],
                    region["grid"]["dx"],
                    region["grid"]["dy"], 
                ) * 0.05

                distance = (
                    (center_x - image_x ) ** 2 
                    + (center_y - image_y) ** 2
                ) ** 0.5

                if distance > tolerance:
                    continue

                if not is_playable_hex(
                    board_id, region["name"], column, row
                ):
                    continue

                boundary = QPolygonF([
                    QPointF(x,y)
                    for x,y in region["boundary"]
                ])

                if not boundary.containsPoint(
                    QPointF(center_x, center_y),
                    Qt.FillRule.OddEvenFill,
                ):
                    continue 

                candidates.append((
                    board_id,
                    region["name"],
                    column,
                    row
                ))

        #Deterministic choice, regardless of click position.
        return min(candidates)

    def canonical_transport_key(self, key):
        return self.canonical_hex_key(key)

    def normalize_transport_hex(self, record):
        key = self.canonical_transport_key(record["key"])

        grid, center_x, center_y = (
            self.transport_key_geometry(list(key))
        )

        board_id, region_name, column, row = key

        region = next(
            entry
            for entry in barbarossa_grids[board_id]["regions"]
            if entry["name"] == region_name
        )

        number = printed_hex_number(region, column, row)

        return {
            "key" : key,
            "grid" : grid,
            "center" : (center_x, center_y),
            "reference" : f"{region_name}:{number}",
        }

    def hex_key_geometry(self, key):
        "Get a hex's grid and center in campaign coordinates."

        if (
            not isinstance(key, (list, tuple))
            or len(key) != 4 
            or not isinstance(key[0], str)
            or not isinstance(key[1], str)
            or type(key[2]) is not int
            or type(key[3]) is not int
        ):
            raise ValueError("Invalid hex key.")

        board_id, region_name, column, row = key

        board = next(
            (
                entry for entry in barbarossa_boards 
                if entry[0] == board_id
            ),
            None,
        )

        if board is None or board_id not in barbarossa_grids:
            raise ValueError(f"Unknown campaign board: {board_id}")

        region = next(
            (
                entry for entry in barbarossa_grids[board_id]["regions"]
                if entry["name"] == region_name
            ),
            None,
        )

        if region is None:
            raise ValueError(
                f"Unknown region on {board_id} : {region_name}"
            )

        if not is_playable_hex(
            board_id, region_name, column, row
        ):
            raise ValueError("The key references an excluded hex.")

        local_x, local_y = hex_center(
            region["grid"], column, row
        )

        origin_x, origin_y = board[2], board[3]

        return (
            region["grid"],
            origin_x + local_x, 
            origin_y + local_y
        )

    def transport_key_geometry(self, key):
        return self.hex_key_geometry(key)
    
    def load_transport_connections(self):
        if not self.transport_path.is_file():
            return 

        data = json.loads(
            self.transport_path.read_text(encoding = "utf-8")
        )

        if (
            not isinstance(data, dict)
            or data.get("format") != "tsww-barbarossa-transport"
            or data.get("version") != 1
            or not isinstance(data.get("connections"), list)
        ):
            raise ValueError("Invalid transport file.")

        #Validate everything before adding display items.
        prepared = [] 
        seen = set()
        excluded_connections = []

        for record in data["connections"]:
            if not isinstance(record, dict):
                raise ValueError("Invalid transport connection.")

            source_key = record.get("source_key")
            target_key = record.get("target_key")
            transport_type = record.get("type")
            source_side = record.get("source_side")
            target_side = record.get("target_side")

            if (
                type(source_side) is not int
                or not 0 <= source_side < 6
                or type(target_side) is not int
                or not 0 <= target_side < 6 
                or not isinstance(transport_type, str)
            ):
                raise ValueError("Invalid transport type or side.")

            for endpoint in (source_key, target_key):
                if (
                    not isinstance(endpoint, list)
                    or len(endpoint) != 4 
                    or not isinstance(endpoint[0], str)
                    or not isinstance(endpoint[1], str)
                    or type(endpoint[2]) is not int 
                    or type(endpoint[3]) is not int
                ):
                    raise ValueError("Invalid transport hex key,")

            if any(
                not is_playable_hex(*endpoint)
                for endpoint in (source_key, target_key)
            ):
                excluded_connections.append(record.copy())
                continue 

            source_key = list(
                self.canonical_transport_key(source_key)
            )
            target_key = list(
                self.canonical_transport_key(target_key)
            )


            source_grid, sx, sy = self.transport_key_geometry(
                source_key
            )
            target_grid, tx, ty = self.transport_key_geometry(
                target_key
            )

            source_key = tuple(source_key)
            target_key = tuple(target_key)

            if source_key == target_key:
                raise ValueError("Transport connects a hex to itself.")

            #Recaculate sides using the normalized grids.
            source_side, _, _ = nearest_hexside(
                source_grid, sx, sy, tx, ty
            )
            target_side, _, _ = nearest_hexside(
                target_grid, tx, ty, sx, sy
            )



            source_vertices = hex_vertices(source_grid, sx, sy)
            target_vertices = hex_vertices(target_grid, tx, ty)

            start = source_vertices[source_side]
            end = source_vertices[(source_side + 1) % 6]
            other_start = target_vertices[target_side]
            other_end = target_vertices[(target_side + 1) % 6]

            mx = (start[0] + end[0]) / 2
            my = (start[1] + end[1]) / 2
            other_mx = (other_start[0] + other_end[0]) / 2
            other_my = (other_start[1] + other_end[1]) / 2 

            tolerance = min(
                source_grid["dx"], source_grid["dy"],
                target_grid["dx"], target_grid["dy"],
            ) * 0.05

            if (
                ((tx - (2 * mx - sx)) ** 2
                 + (ty - (2 * my - sy)) ** 2) ** 0.5 > tolerance 
                or ((mx - other_mx) ** 2 
                    + (my - other_my) ** 2) ** 0.5 > tolerance  
            ):
                raise ValueError(
                    "Saved transport hexes do not share an edge."
                )

            try:
                pen = self.transport_pen(transport_type)
            except KeyError:
                raise ValueError(
                    f"Unknown transport type: {transport_type}"
                ) from None 

            segment_key = (
                transport_type,
                tuple(sorted([source_key, target_key])),
            )

            if segment_key in seen:
                # Alternate region keys can describe
                # an already-loaded physical connection.
                continue

            seen.add(segment_key)

            path = QPainterPath()
            path.moveTo(sx, sy)
            path.lineTo(
                (mx + other_mx) / 2,
                (my + other_my) / 2,
            )
            path.lineTo(tx, ty)

            prepared.append((
                segment_key,
                {
                    "source_key" : source_key,
                    "source_side" : source_side,
                    "target_key" : target_key,
                    "target_side" : target_side,
                    "type" : transport_type,
                },
                path,
                pen,
            ))

        self.excluded_transport_connections = excluded_connections

        for segment_key, segment, path, pen in prepared:
            item = self.map_scene.addPath(path, pen)
            is_railway = (
                "Railway" in segment["type"]
                or "RR" in segment["type"]
            )
            item.setZValue(92 if is_railway else 90)
            item.setAcceptedMouseButtons(Qt.MouseButton.NoButton)

            segment["item"] = item
            self.transport_segments[segment_key] = segment

    def draw_transport_to(self, point):
        target = self.find_hex_at(point)

        if target is None:
            self.window().statusBar().showMessage(
                "Choose a playable hex."
            )
            return 

        target = self.normalize_transport_hex(target)

        #First click: choose starting hex.
        if self.transport_anchor is None:
            self.transport_anchor = target
            self.window().statusBar().showMessage(
                f"Route starts at {target['reference']}"
                " | Click a neighboring hex"
            )
            return 

        source = self.transport_anchor 

        if source["key"] == target["key"]:
            return 

        source_x, source_y = source["center"]
        target_x, target_y = target["center"]

        #Find the source edge facing the target. 
        side, start, end = nearest_hexside(
            source["grid"],
            source_x,
            source_y,
            target_x, 
            target_y
        )

        midpoint_x = (start[0] + end[0]) / 2
        midpoint_y = (start[1] + end[1]) / 2

        #Expected neighbor center across this edge.
        expected_x = 2 * midpoint_x - source_x
        expected_y = 2 * midpoint_y - source_y

        tolerance = min(
            source["grid"]["dx"],
            source["grid"]["dy"],
            target["grid"]["dx"],
            target["grid"]["dy"],
        ) * 0.05

        center_error = (
            (target_x - expected_x) ** 2 
            + (target_y - expected_y) ** 2
        ) ** 0.5

        #Find the target edge facing the source 
        opposite, other_start, other_end = nearest_hexside(
            target["grid"],
            target_x, 
            target_y, 
            source_x,
            source_y
        )

        other_midpoint_x = (
            other_start[0] + other_end[0]
        ) / 2 
        other_midpoint_y = (
            other_start[1] + other_end[1]
        ) / 2 

        edge_error = (
            (midpoint_x - other_midpoint_x) ** 2 
            + (midpoint_y - other_midpoint_y) ** 2 
        ) ** 0.5

        if center_error > tolerance or edge_error > tolerance :
            self.window().statusBar().showMessage(
                "Choose an adjoining hex."
                " | Toggle Draw Transport off and on"
                " to start a separate route"
            )
            return 

        #Same connection in either direction has the same key.
        connection = tuple(sorted([
            source["key"],
            target["key"],
        ]))

        segment_key = (
            self.transport_draw_type,
            connection,
        )

        if self.transport_erase_mode:
            segment = self.transport_segments.pop(
                segment_key, None
            )

            if segment is None:
                self.window().statusBar().showMessage(
                    "No connection of the selected type"
                    " between these hexes."
                )
                self.transport_anchor = None
                return 

            try:
                self.save_transport_connections()
            except (OSError, ValueError, TypeError) as error:
                #Restore the record if saving failed.
                self.transport_segments[segment_key] = segment
                self.window().statusBar().showMessage(
                    f"Connection was not erased: {error}"
                )
                return 

            self.map_scene.removeItem(segment["item"])
            self.transport_anchor = None 
            self.refresh_transport_summary()

            self.window().statusBar().showMessage(
                f"Erased {self.transport_draw_type} connection"
                " | Saved"
            )
            return 

        if segment_key not in self.transport_segments:
            crossing_x = (
                midpoint_x + other_midpoint_x
            ) / 2 
            crossing_y = (
                midpoint_y + other_midpoint_y
            ) / 2 

            path = QPainterPath()
            path.moveTo(source_x, source_y)
            path.lineTo(crossing_x, crossing_y)
            path.lineTo(target_x, target_y)

            pen = self.transport_pen(self.transport_draw_type)

            item = self.map_scene.addPath(path, pen)

            #Railways appear above the wider road lines.
            is_railway = (
                "Railway" in self.transport_draw_type
                or "RR" in self.transport_draw_type
            )
            item.setZValue(92 if is_railway else 90)
            item.setAcceptedMouseButtons(
                Qt.MouseButton.NoButton
            )

            self.transport_segments[segment_key] = {
                "source_key" : source["key"],
                "source_side" : side,
                "target_key" : target["key"],
                "target_side" : opposite,
                "type" : self.transport_draw_type,
                "item" : item
            }

            try: 
                self.save_transport_connections()
            except (OSError, ValueError,  TypeError) as error:
                self.transport_segments.pop(segment_key)
                self.map_scene.removeItem(item)

                self.window().statusBar().showMessage(
                    f"Connection was not added: {error}"
                )
                return

        #Next click extends the route from this hex.
        self.transport_anchor = target

        self.window().statusBar().showMessage(
            f"{self.transport_draw_type}: "
            f"{source['reference']} -> {target['reference']}"
            " | Saved"
        )

        self.refresh_transport_summary()

    def start_transport_branch(self):
        if not self.transport_draw_mode:
            return 

        self.transport_anchor = None 

        self.window().statusBar().showMessage(
            "New branch | Click its starting hex,"
            " then neighboring hexes"
        )

    def set_transport_draw_mode(self, enabled, transport_type):
        if enabled:
            self.cancel_counter_move()
        self.transport_draw_mode = enabled
        self.stack_changed.emit()
        self.transport_draw_type = transport_type
        self.transport_anchor = None 

        if enabled:
            self.set_edge_pick_mode(False)
            message = (
                f"{transport_type} drawing enabled"
                " | Click a starting hex"
            )
        else:
            message = "Transport drawing disabled"

        self.window().statusBar().showMessage(message)

    def set_edge_pick_mode(self, enabled):
        if enabled:
            self.cancel_counter_move()
        self.edge_pick_mode = enabled
        self.stack_changed.emit()

        if not enabled and self.edge_highlight is not None:
            self.map_scene.removeItem(self.edge_highlight)
            self.edge_highlight = None
    
    def select_campaign_point(self, point):
        """Select the hex at a campaign position."""

        for board_id, record in self.board_records.items():
            origin_x, origin_y = record["origin"]
            width, height = record["size"]

            image_x = point.x() - origin_x
            image_y = point.y() - origin_y

            if not (0 <= image_x < width and 0 <= image_y < height):
                continue

            for region in barbarossa_grids[board_id]["regions"]:
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

                if not is_playable_hex(
                    board_id, region["name"], column, row
                ): 
                    self.window().statusBar().showMessage(
                        "That position is outside the playable map."
                    )
                    return False

                key = self.canonical_hex_key(
                    (board_id, region["name"], column, row)
                )

                board_id, region_name, column, row = key

                region = next(
                    entry 
                    for entry in barbarossa_grids[board_id]["regions"]
                    if entry["name"] == region_name
                )

                number= printed_hex_number(region, column, row)

                grid, campaign_x, campaign_y = ( 
                    self.hex_key_geometry(key)
                )

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
                self.refresh_transport_summary()

                if self.edge_highlight is not None:
                    self.map_scene.removeItem(self.edge_highlight)
                    self.edge_highlight = None

                properties = self.map_definitions.get(key, {}).copy()
                properties["_grid_sideways"] = region["grid"]["sideways"]

                self.hex_selected.emit(
                    self.hexes[key]["game_reference"],
                    properties,
                )

                self.debug_marker.setPos(campaign_x, campaign_y)
                self.centerOn(self.debug_marker)

                self.window().statusBar().showMessage(
                    f"{board_id} | {region['name']}:{number}"
                    f" | Grid ({column}, {row})"
                )
                return True

            self.window().statusBar().showMessage(
                f"{board_id} | No grid region at this position"
            )
            return False

        return False 

    def keyPressEvent(self, event):
        if self.moving_unit_id is not None:
            if event.key() == Qt.Key.Key_Escape:
                self.cancel_counter_move()
            elif event.key() not in (Qt.Key.Key_Up, Qt.Key.Key_Down,
                                     Qt.Key.Key_Left, Qt.Key.Key_Right):
                super().keyPressEvent(event)
                return
            event.accept()
            return
        if event.key() == Qt.Key.Key_F8:
            self.check_selected_hex_joins()
            event.accept()
            return
        
        arrows = {
            Qt.Key.Key_Up,
            Qt.Key.Key_Down,
            Qt.Key.Key_Left,
            Qt.Key.Key_Right,
        }

        if event.key() not in arrows:
            super().keyPressEvent(event)
            return

        if self.selected_hex_key is None:
            self.window().statusBar().showMessage(
                "Select a hex before using the arrow keys."
            )
            event.accept()
            return

        if self.edge_pick_mode:
            self.window().statusBar().showMessage(
                "Turn off Pick Hex Edge before moving between hexes."
            )
            event.accept()
            return

        board_id, region_name, column, row = self.selected_hex_key

        region = next(
            region
            for region in barbarossa_grids[board_id]["regions"]
            if region["name"] == region_name
        )

        grid = region["grid"]
        origin_x, origin_y = self.board_records[board_id]["origin"]

        local_x, local_y = hex_center(grid, column, row)
        center_x = origin_x + local_x
        center_y = origin_y + local_y

        vertices = hex_vertices(grid, center_x, center_y)

        if grid["sideways"]:
            directions = {
                Qt.Key.Key_Up: 5, 
                Qt.Key.Key_Down : 2,
                Qt.Key.Key_Left : 4,
                Qt.Key.Key_Right : 1,
            }
        else:
            directions = {
                Qt.Key.Key_Up : 0,
                Qt.Key.Key_Down : 3, 
                Qt.Key.Key_Left : 4, 
                Qt.Key.Key_Right : 1,
            }

        side = directions[event.key()]
        start = vertices[side]
        end = vertices[(side + 1) % 6]

        #Reflect the center through the shared edge's midpoint.
        target = QPointF(
            start[0] + end[0] - center_x,
            start[1] + end[1] - center_y,
        )

        if not self.select_campaign_point(target):
            self.window().statusBar().showMessage(
                "No mapped neighboring hex in that direction."
            )

        event.accept()

    def set_review_overlay(self, enabled):
        self.review_overlay_enabled = enabled
        self.viewport().update()

    def set_transport_review_overlay(self, enabled):
        self.transport_review_overlay_enabled = enabled
        self.viewport().update()

    def draw_transport_review(self, painter, rect):
        if not self.transport_review_overlay_enabled:
            return 

        colors = {
            "Unknown" : QColor(240, 70, 70, 65),
            "In progress" : QColor(255, 185, 0, 85),
            "Verified" : QColor(40, 210, 90, 85),
        }

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        #Unreviewed regions begin with a red background. 
        painter.setBrush(colors["Unknown"])

        for board_id, record in self.board_records.items():
            origin_x, origin_y = record["origin"]

            for region in barbarossa_grids[board_id]["regions"]:
                polygon = QPolygonF([
                    QPointF(origin_x + x, origin_y + y)
                    for x,y in region["boundary"]
                ])

                if polygon.boundingRect().intersects(rect):
                    painter.drawPolygon(polygon)
        

        for key, properties in self.map_definitions.items():
            status = properties.get(
                "transport_review_status", "Unknown"
            )

            if status not in ("In progress", "Verified"):
                continue

            board_id, region_name, column, row = key

            if board_id not in self.board_records:
                continue

            if not is_playable_hex(
                board_id, region_name, column, row
            ):
                continue 

            region = next(
                (
                    entry
                    for entry in barbarossa_grids[board_id]["regions"]
                    if entry["name"] == region_name
                ),
                None,
            )

            if region is None:
                continue 

            local_x, local_y = hex_center(
                region["grid"], column, row
            )
            origin_x, origin_y = (
                self.board_records[board_id]["origin"]
            )

            polygon = QPolygonF([
                QPointF(x,y)
                for x,y in hex_vertices(
                    region["grid"],
                    origin_x + local_x,
                    origin_y + local_y
                )
            ])

            if polygon.boundingRect().intersects(rect):
                painter.setBrush(colors[status])
                painter.drawPolygon(polygon)

        painter.restore()

    def drawForeground(self, painter, rect):


        super().drawForeground(painter, rect)


        if self.transport_review_overlay_enabled:
            self.draw_transport_review(painter, rect)
            return 
        
        if not self.review_overlay_enabled:
            return

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        #Wash every defined region red: unedited means unknown.
        painter.setBrush(QColor(220, 65, 65, 45))

        for board_id, record in self.board_records.items():
            definition = barbarossa_grids.get(board_id)

            if definition is None:
                continue

            origin_x, origin_y = record["origin"]

            for region in definition["regions"]:
                polygon = QPolygonF([
                    QPointF(origin_x + x, origin_y + y)
                    for x,y in region["boundary"]
                ])

                if polygon.boundingRect().intersects(rect):
                    painter.drawPolygon(polygon)


        colors = {
            "Verified" : QColor(30, 200, 90, 110),
            "Suggested" : QColor(255, 185, 25, 110),
            "In progress" : QColor(255, 185, 25, 110),
        }

        for key, properties in self.map_definitions.items():
            color = colors.get(properties.get("review_status"))

            if color is None:
                continue

            board_id, region_name, column, row = key
            record = self.board_records.get(board_id)

            if record is None:
                continue

            region = next(
                ( 
                    region 
                    for region in barbarossa_grids[board_id]["regions"]
                    if region["name"] == region_name
                ),
                None,
            )

            if region is None:
                continue

            local_x, local_y = hex_center(
                region["grid"], column, row
            )
            origin_x, origin_y = record["origin"]

            polygon = QPolygonF([
                QPointF(x,y)
                for x, y in hex_vertices(
                    region["grid"],
                    origin_x + local_x, 
                    origin_y + local_y
                )
            ])

            if polygon.boundingRect().intersects(rect):
                painter.setBrush(color)
                painter.drawPolygon(polygon)

        painter.restore()

    def find_hex_at(self, point): 
        """Look up a hex without selecting or modifying it."""


        for board_id, record in self.board_records.items():
            origin_x, origin_y = record["origin"]
            width, height = record["size"]

            image_x = point.x() - origin_x 
            image_y = point.y() - origin_y

            if not (0 <= image_x < width and 0 <= image_y < height):
                continue

            for region in barbarossa_grids[board_id]["regions"]:
                boundary = QPolygonF([
                    QPointF(x,y)
                    for x,y in region["boundary"]
                ])

                if not boundary.containsPoint(
                    QPointF(image_x, image_y),
                    Qt.FillRule.OddEvenFill,
                ):
                    continue

                column, row, local_x, local_y = nearest_hex(
                    region["grid"], image_x, image_y
                )

                if not is_playable_hex(
                    board_id, region["name"], column, row
                ):
                    continue

                return {
                    "key" : (board_id, region["name"], column, row),
                    "reference" : (
                        f"{region['name']}:"
                        f"{printed_hex_number(region, column, row)}"
                    ),
                    "grid" : region["grid"],
                    "center" : (
                        origin_x + local_x, 
                        origin_y + local_y
                    ),
                }
        return None 

    def audit_mapping_edges(self):
        if not self.board_records:
            QMessageBox.information(
                self,
                "Mapping Audit",
                "Load the campaign first."
            )
            return 

        messages = audit_sides(self)

        if not messages:
            QMessageBox.information(
                self,
                "Mapping Audit",
                "No disagreements found on recorded shared "
                "features with mapped neighbors.\n\n"
                "This does not verify the printed map or"
                "unrecorded features.",
            )
            return 

        dialog = QMessageBox(self)
        dialog.setWindowTitle("Mapping Audit")
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setText(
            f"Found {len(messages)} shared-feature differences."
        )
        dialog.setInformativeText(
            "Open Show Details to see the affected hexes. \n"
            "Unknown on one side means it has not been recorded there. \n"
            "The audit does not change your data."
        )
        dialog.setDetailedText("\n".join(messages))
        dialog.exec()


    def check_selected_hex_joins(self):
        if self.selected_hex_key is None:
            self.window().statusBar().showMessage(
                "Select a hex first."
            )
            return 

        for item in self.join_markers:
            self.map_scene.removeItem(item)

        self.join_markers = [] 

        board_id, region_name, column, row = self.selected_hex_key

        region = next(
            region 
            for region in barbarossa_grids[board_id]["regions"]
            if region["name"] == region_name
        )

        grid = region["grid"]
        origin_x, origin_y = self.board_records[board_id]["origin"]

        local_x, local_y = hex_center(grid, column, row)
        center_x = origin_x + local_x 
        center_y = origin_y + local_y

        vertices = hex_vertices(grid, center_x, center_y)

        #Allow small differences in the original grid calibrations.
        tolerance = min(grid["dx"], grid["dy"]) * 0.05


        reference = printed_hex_number(region, column, row)
        print(
            f"\n Join check: {board_id} {region_name} : {reference}",
            flush = True
        )

        warnings = 0

        for side in range(6):
            start = vertices[side]
            end = vertices[(side + 1) % 6]

            expected_x = start[0] + end[0] - center_x
            expected_y = start[1] + end[1] - center_y

            neighbor = self.find_hex_at(
                QPointF(expected_x, expected_y)
            )

            if neighbor is None:
                print(f"Side {side}: no mapped neighbor", flush = True)
                continue

            neighbor_x, neighbor_y = neighbor["center"]

            center_error = (
                (neighbor_x - expected_x) ** 2 
                + (neighbor_y - expected_y) ** 2
            ) ** 0.5

            #Find the neighbor edge facing the selected hex.
            opposite, other_start, other_end = nearest_hexside(
                neighbor["grid"],
                neighbor_x,
                neighbor_y,
                center_x,
                center_y,
            )

            edge_error = (
                (
                    (start[0] + end[0]) / 2
                    - (other_start[0] + other_end[0]) / 2
                ) ** 2
                + (
                    (start[1] + end[1]) / 2 
                    - (other_start[1] + other_end[1]) / 2
                ) ** 2
            ) ** 0.5

            okay = (
                neighbor["key"] != self.selected_hex_key
                and center_error <= tolerance
                and edge_error <= tolerance
            )

            if not okay:
                warnings += 1

            color = (
                Qt.GlobalColor.green
                if okay 
                else Qt.GlobalColor.red
            )

            marker = self.map_scene.addEllipse(
                neighbor_x - 10,
                neighbor_y - 10,
                20,
                20,
                QPen(color),
                QBrush(color),
            )
            marker.setZValue(102)
            marker.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
            self.join_markers.append(marker)

            crossing = (
                " [board/region join]"
                if neighbor["key"][:2] != self.selected_hex_key[:2]
                else ""
            )

            print(
                f"Side {side} -> {neighbor['key'][0]} "
                f"{neighbor['reference']} / side {opposite}"
                f" | center error {center_error:.2f}px"
                f" | edge error {edge_error:.2f}px"
                f" | {'OK' if okay else 'CHECK'}{crossing}",
                flush = True,
            )

            self.window().statusBar().showMessage(
                f"Join check: {warnings} alignment warnigns"
                " | Details in terminal"
            )
