"""Simple chronological counter history; entries after the cursor are redoable."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem


class HistoryPanel(QWidget):
    def __init__(self, view, parent=None):
        super().__init__(parent)
        self.view = view
        layout = QVBoxLayout(self)
        buttons = QHBoxLayout()
        self.undo_button = QPushButton("Undo Action")
        self.redo_button = QPushButton("Redo Action")
        buttons.addWidget(self.undo_button)
        buttons.addWidget(self.redo_button)
        layout.addLayout(buttons)
        self.summary = QLabel()
        self.summary.setWordWrap(True)
        layout.addWidget(self.summary)
        self.results = QListWidget()
        layout.addWidget(self.results)
        self.undo_button.clicked.connect(view.undo_counter_action)
        self.redo_button.clicked.connect(view.redo_counter_action)
        view.history_changed.connect(self.refresh)
        view.stack_changed.connect(self.refresh_controls)
        self.refresh()

    def refresh_controls(self):
        self.undo_button.setEnabled(self.view.can_undo_counter_action())
        self.redo_button.setEnabled(self.view.can_redo_counter_action())

    def refresh(self):
        history = self.view.action_history
        cursor = history["cursor"]
        self.results.clear()
        for index, entry in enumerate(history["entries"]):
            state = "Applied" if index < cursor else "Undone"
            item = QListWidgetItem(f"{index + 1}. [{state}] {entry['description']}")
            detail = (f"Instance: {entry['unit_id']}" if "unit_id" in entry
                      else self.event_details(entry))
            item.setToolTip(f"{entry['timestamp']}\n{detail}\nAction: {entry['action_id']}")
            self.results.addItem(item)
        self.results.scrollToBottom()
        self.summary.setText(
            f"{cursor} applied | {len(history['entries']) - cursor} available to redo.\n"
            "Counter actions and recorded results. Mapping edits are separate."
        )
        self.refresh_controls()

    @staticmethod
    def event_details(entry):
        payload = entry["payload"]
        if entry["kind"] == "dice_roll":
            return (f"Dice: {payload['faces']} | Result: {payload['value']}\n"
                    f"Controller: {payload['controller']} | {payload['method']}\n"
                    "v1.6a Rule 2.C.1, printed p8 / PDF p10")
        return (f"Attack: {payload['attack_id']}\nAttackers: {', '.join(payload['attacker_ids'])}\n"
                f"Defenders: {', '.join(payload['defender_ids'])}\n"
                f"Rolls: {', '.join(str(roll['value']) for roll in payload['rolls'])}\n"
                f"Notes: {payload['notes']}\nManually recorded; no combat effects applied.")
