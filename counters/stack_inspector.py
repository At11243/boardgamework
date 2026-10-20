"""Stack membership, instance selection, and reviewed face flipping."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton
from counters.counter_state import stack_ids


class StackInspector(QWidget):
    def __init__(self, view, parent=None):
        super().__init__(parent)
        self.view = view
        layout = QVBoxLayout(self)
        self.heading = QLabel("Select a campaign hex")
        self.results = QListWidget()
        self.details = QLabel("Click a counter or choose an instance here.")
        self.details.setWordWrap(True)
        layout.addWidget(self.heading)
        layout.addWidget(self.results)
        layout.addWidget(self.details)
        self.flip_button = QPushButton("Flip Selected Counter")
        self.flip_reason = QLabel()
        self.flip_reason.setWordWrap(True)
        layout.addWidget(self.flip_button)
        layout.addWidget(self.flip_reason)
        self.flip_button.clicked.connect(view.flip_selected_counter)
        self.move_button = QPushButton("Move Selected Counter")
        self.cancel_move_button = QPushButton("Cancel Move")
        self.move_reason = QLabel()
        self.move_reason.setWordWrap(True)
        layout.addWidget(self.move_button)
        layout.addWidget(self.cancel_move_button)
        layout.addWidget(self.move_reason)
        self.move_button.clicked.connect(view.begin_counter_move)
        self.cancel_move_button.clicked.connect(view.cancel_counter_move)
        self.results.currentItemChanged.connect(self.choose_instance)
        view.stack_changed.connect(self.refresh)

    def refresh(self):
        view = self.view
        key = view.selected_hex_key
        ids = stack_ids(view.units, key)
        reference = view.hexes.get(key, {}).get("game_reference", "Select a campaign hex")
        self.heading.setText(f"{reference} | {len(ids)} counters | top first")
        self.results.blockSignals(True)
        try:
            self.results.clear()
            for uid in reversed(ids):
                unit = view.units[uid]
                item = QListWidgetItem(unit["name"])
                item.setData(Qt.ItemDataRole.UserRole, uid)
                item.setToolTip(f"Instance: {uid}\nType: {unit['type_id']}")
                self.results.addItem(item)
                if uid == view.selected_unit_id:
                    self.results.setCurrentItem(item)
        finally:
            self.results.blockSignals(False)
        unit = view.units.get(view.selected_unit_id)
        self.details.setText(
            f"{unit['name']}\nInstance: {unit['unit_id']}\n"
            f"Face: {unit['active_face']}\nManual placement; no legality checks."
            if unit else "Click a counter or choose an instance here."
        )
        reason = view.flip_unavailable_reason()
        self.flip_button.setEnabled(not reason)
        self.flip_button.setToolTip(reason or "Switch between reviewed faces; no gameplay effects applied.")
        self.flip_reason.setText(reason)
        reason = view.move_unavailable_reason()
        self.move_button.setEnabled(not reason)
        self.cancel_move_button.setEnabled(view.moving_unit_id is not None)
        self.results.setEnabled(view.moving_unit_id is None)
        self.move_reason.setText(reason or "Movement costs and legality are manual.")

    def choose_instance(self, current, previous):
        self.view.select_unit(current.data(Qt.ItemDataRole.UserRole) if current else None)
