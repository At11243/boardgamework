"""Basic dice presentation; a future animation must display the recorded faces."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox, QSpinBox,
    QLabel, QLineEdit, QPushButton, QDialogButtonBox, QMessageBox,
)


class DiceDialog(QDialog):
    def __init__(self, view, parent=None, *, controller="human"):
        super().__init__(parent)
        if controller not in ("human", "ai"):
            raise ValueError("Controller must be human or ai.")
        self.view = view
        self.controller = controller
        self.setWindowTitle("Dice")
        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)
        self.roll_type = QComboBox()
        for label, key in (("1D10", "1D10"), ("2D10 - sum", "2D10"),
                           ("Percentile - tens then ones", "percentile")):
            self.roll_type.addItem(label, key)
        form.addRow("Roll", self.roll_type)
        self.method = QComboBox()
        self.method.addItem("Roll automatically", "automatic")
        if controller == "human":
            self.method.addItem("Enter physical dice", "manual")
        self.method.setEnabled(controller == "human")
        form.addRow("Method", self.method)
        self.first_label = QLabel("Die 1 digit")
        self.second_label = QLabel("Die 2 digit")
        self.first = QSpinBox()
        self.second = QSpinBox()
        for spin in (self.first, self.second):
            spin.setRange(0, 9)
        form.addRow(self.first_label, self.first)
        form.addRow(self.second_label, self.second)
        self.purpose = QLineEdit()
        self.purpose.setPlaceholderText("Optional: what is this roll for?")
        form.addRow("Purpose", self.purpose)
        self.explanation = QLabel("D10: 0 means 10. Percentile: 00 means 100.\n"
                                  "v1.6a Rule 2.C.1, printed p8 / PDF p10.\n"
                                  "Rolls are saved with the campaign history; no rules effects are applied.")
        self.explanation.setWordWrap(True)
        layout.addWidget(self.explanation)
        self.roll_button = QPushButton()
        self.roll_button.clicked.connect(self.record_roll)
        layout.addWidget(self.roll_button)
        self.result = QLabel("No roll recorded.")
        self.result.setWordWrap(True)
        self.result.setTextFormat(Qt.TextFormat.PlainText)
        layout.addWidget(self.result)
        close = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close.rejected.connect(self.reject)
        layout.addWidget(close)
        self.roll_type.currentIndexChanged.connect(self.update_inputs)
        self.method.currentIndexChanged.connect(self.update_inputs)
        self.update_inputs()

    def update_inputs(self, *_):
        kind = self.roll_type.currentData()
        manual = self.method.currentData() == "manual"
        self.first.setVisible(manual)
        self.first_label.setVisible(manual)
        self.second.setVisible(manual and kind != "1D10")
        self.second_label.setVisible(manual and kind != "1D10")
        self.first_label.setText("Tens digit" if kind == "percentile" else "Die 1 digit (0 = 10)")
        self.second_label.setText("Ones digit" if kind == "percentile" else "Die 2 digit (0 = 10)")
        self.roll_button.setText("Record Entered Roll" if manual else "Roll and Record")

    def record_roll(self, *_):
        faces = None
        kind = self.roll_type.currentData()
        if self.method.currentData() == "manual":
            faces = [self.first.value()]
            if kind != "1D10":
                faces.append(self.second.value())
        try:
            record = self.view.record_dice_roll(kind, controller=self.controller,
                                                manual_faces=faces, purpose=self.purpose.text())
        except ValueError as error:
            QMessageBox.warning(self, "Cannot Record Roll", str(error))
            return
        digits = ", ".join(str(value) for value in record["faces"])
        self.result.setText(f"{kind}: [{digits}] = {record['value']} ({record['method']})\n"
                            "Recorded in campaign history. Save the campaign to keep it.")
