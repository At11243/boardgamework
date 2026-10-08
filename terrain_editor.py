from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QPushButton,
    QScrollArea
)

terrain_types = [
    "Clear",
    "Steppe",
    "Hills",
    "Desert Hills",
    "Stony Hills",
    "Mountain",
    "High Mountain",
    "Desert Mountain",
    "Woods"
    "Paddy Fields", 
    "Jungle",
    "Waterways",
    "Lakes",
    "Salt Marsh",
    "Swamp",
    "Desert",
    "Sandy Desert",
    "Stony Desert",
    "Irrigation Intensive",
    "Bocage",
    "Glacier",
    "Lava Flow",
    "Salt Lake",
    "Lake/Sea",
]

settlement_types = [
    "None",
    "Major City",
    "Small City",
    "Large Town",
    "Town",
    "Point of Interest",
]

class TerrainEditor(QWidget):
    applied = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.has_selection = False

        layout = QVBoxLayout(self)

        self.reference_label = QLabel("Select a hex")
        layout.addWidget(self.reference_label)

        self.developer_mode = QCheckBox("Developer Mode")
        layout.addWidget(self.developer_mode)

        self.fields = QWidget()
        fields_layout = QVBoxLayout(self.fields)

        fields_layout.addWidget(QLabel("Terrain -- Select all that apply"))

        self.terrain_checks = {} 

        for terrain in terrain_types:
            checkbox = QCheckBox(terrain)
            self.terrain_checks[terrain] = checkbox
            fields_layout.addWidget(checkbox)


        fields_layout.addWidget(QLabel("Settlement classification"))

        self.settlement_known = QCheckBox(
            "Settlement information checked"
        )

        fields_layout.addWidget(self.settlement_known)

        self.settlement_type = QComboBox()
        self.settlement_type.addItems(settlement_types)

        self.settlement_name = QLineEdit()
        self.settlement_name.setPlaceholderText("Settlement name")
        fields_layout.addWidget(self.settlement_name)

        fields_layout.addWidget(QLabel("Review Status"))

        self.review_status = QComboBox()
        self.review_status.addItems([
            "Unknown",
            "Suggested",
            "Verified"
        ])

        fields_layout.addWidget(self.review_status)

        self.apply_button = QPushButton("Apply and Save")
        fields_layout.addWidget(self.apply_button)

        fields_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.fields)
        layout.addWidget(scroll)

        self.developer_mode.toggled.connect(self.update_enabled)
        self.apply_button.clicked.connect(self.apply_values)

        self.show_hex(None, {})

    def update_enabled(self):
        self.fields.setEnabled(
            self.has_selection and self.developer_mode.isChecked()
        )

    def show_hex(self, reference, properties):
        self.has_selection = reference is not None
        self.reference_label.setText(reference or "Select a hex")

        terrain = properties.get("terrain") or []

        for name, checkbox in self.terrain_checks.items():
            checkbox.setChecked(name in terrain)

        settlement = properties.get("settlement")

        self.settlement_known.setChecked(settlement is not None)
        self.settlement_type.setCurrentText(
            settlement.get("type", "None")
            if settlement is not None
            else "None"
        )
        self.settlement_name.setText(
            settlement.get("name", "")
            if settlement is not None
            else ""
        )

        self.review_status.setCurrentText(
            properties.get("review_status", "Unknown")
        )

        self.update_enabled()

    def apply_values(self):
        terrain = [
            name
            for name, checkbox in self.terrain_checks.items()
            if checkbox.isChecked()
        ]

        settlement = None

        if self.settlement_known.isChecked():
            settlement_type = self.settlement_type.currentText()

            settlement = {
                "type" : settlement_type,
                "name" : (
                    self.settlement_name.text().strip()
                    if settlement_type != "None"
                    else ""
                ),
            }

        self.applied.emit({
            "terrain" : terrain or None,
            "settlement" : settlement, 
            "review_status" : self.review_status.currentText(),
        })
