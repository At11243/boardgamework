from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QGroupBox,
)

terrain_types = [
    "Clear",
    "Steppe",
    "Hills",
    "Desert Hills",
    "Stony Hills",
    "Mountain",
    "Desert Mountain",
    "Woods",
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

port_types = [
    "Unknown",
    "None",
    "Great Port",
    "Large Port",
    "General Port",
    "Small Port"
]

presence_types = [
    "Unknown",
    "Absent",
    "Present"
]

waterway_types = [
    "Unknown",
    "None",
    "Major River",
    "Minor River", 
    "Wadi",
    "Canal"
]

border_types = [
    "Unknown",
    "None",
    "Internal Border",
    "International Border",
    "Future Border"
]

navigation_types = [
    "Unknown",
    "Not navigable",
    "Navigable",
]

class TerrainEditor(QWidget):
    applied = Signal(dict)
    edge_mode_changed = Signal(bool)

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

        self.edge_button = QPushButton("Pick Hex Edge")
        self.edge_button.setCheckable(True)
        self.edge_button.toggled.connect(
            self.edge_mode_changed.emit
        )
        fields_layout.addWidget(self.edge_button)

        fields_layout.addWidget(QLabel("Hex surface"))

        self.surface_type = QComboBox()
        self.surface_type.addItems([
            "Unknown",
            "Land",
            "Water",
            "Mixed land/water"
        ])
        fields_layout.addWidget(self.surface_type)
        

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
        fields_layout.addWidget(self.settlement_type)
        
        self.settlement_name = QLineEdit()
        self.settlement_name.setPlaceholderText("Settlement name")
        fields_layout.addWidget(self.settlement_name)

        port_group = QGroupBox("Port")
        port_layout = QVBoxLayout(port_group)

        port_layout.addWidget(QLabel("Port class"))
        self.port_type = QComboBox()
        self.port_type.addItems(port_types)
        port_layout.addWidget(self.port_type)

        self.port_name = QLineEdit()
        self.port_name.setPlaceholderText("Port name")
        port_layout.addWidget(self.port_name)

        port_layout.addWidget(QLabel("Port facilities"))
        self.port_facilities = QComboBox()
        self.port_facilities.addItems(presence_types)
        port_layout.addWidget(self.port_facilities)

        port_layout.addWidget(QLabel("Anchorage"))
        self.port_anchorage = QComboBox()
        self.port_anchorage.addItems(presence_types)
        port_layout.addWidget(self.port_anchorage)

        port_layout.addWidget(QLabel("Naval Base Type"))
        self.port_naval_base_type = QLineEdit()
        self.port_naval_base_type.setPlaceholderText(
            "Printed type; blank = unknown"
        )
        port_layout.addWidget(self.port_naval_base_type)

        port_layout.addWidget(QLabel("Shipbuilding capacity"))
        self.port_shipbuilding_capacity = QLineEdit()
        self.port_shipbuilding_capacity.setPlaceholderText(
            "Printed capacity; blank = unknown"
        )
        port_layout.addWidget(self.port_shipbuilding_capacity)

        fields_layout.addWidget(port_group)


        self.side_help = QLabel()
        self.side_help.setWordWrap(True)
        fields_layout.addWidget(self.side_help)

        self.hexside_controls = {} 

        for side in range(6):
            group = QGroupBox(f"Side {side}")
            side_layout = QVBoxLayout(group)

            side_layout.addWidget(QLabel("River / Waterway"))
            waterway = QComboBox()
            waterway.addItems(waterway_types)
            side_layout.addWidget(waterway)

            side_layout.addWidget(QLabel("Navigation"))
            navigation = QComboBox()
            navigation.addItems(navigation_types)
            side_layout.addWidget(navigation)

            side_layout.addWidget(QLabel("Border"))
            border = QComboBox()
            border.addItems(border_types)
            side_layout.addWidget(border)

            side_layout.addWidget(QLabel("Escarpment"))
            escarpment = QComboBox()
            escarpment.addItems(presence_types)
            side_layout.addWidget(escarpment)

            side_layout.addWidget(QLabel("Coastal cliff"))
            coastal_cliff = QComboBox()
            coastal_cliff.addItems(presence_types)
            side_layout.addWidget(coastal_cliff)

            side_layout.addWidget(QLabel("Printed fortifications"))
            fortification = QComboBox()
            fortification.addItems([
                "Unknown",
                "None",
                "Fortifications",
                "Major Fortifications"
            ])

            side_layout.addWidget(fortification)

            side_layout.addWidget(QLabel("High Mountain"))
            high_mountain = QComboBox()
            high_mountain.addItems(presence_types)
            side_layout.addWidget(high_mountain)

            self.hexside_controls[str(side)] = {
                "group" : group,
                "waterway" : waterway,
                "navigation" : navigation,
                "border" : border,
                "escarpment" : escarpment,
                "coastal_cliff" : coastal_cliff,
                "fortification" : fortification,
                "high_mountain" : high_mountain, 
            }

            fields_layout.addWidget(group)

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
        self.scroll_area = scroll

        self.developer_mode.toggled.connect(self.update_enabled)
        self.apply_button.clicked.connect(self.apply_values)

        self.show_hex(None, {})

    def update_enabled(self):
        self.fields.setEnabled(
            self.has_selection and self.developer_mode.isChecked()
        )

        if not self.fields.isEnabled():
            self.edge_button.setChecked(False)

    def show_hex(self, reference, properties):
        self.has_selection = bool(reference)
        self.reference_label.setText(reference or "Select a hex")


        self.surface_type.setCurrentText(
            properties.get("surface", "Unknown")
        )

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
        port = properties.get("port") or {}

        self.port_type.setCurrentText(
            port.get("type", "Unknown")
        )
        self.port_name.setText(port.get("name", ""))
        self.port_facilities.setCurrentText(
            port.get("facilities", "Unknown")
        )
        self.port_anchorage.setCurrentText(
            port.get("anchorage", "Unknown")
        )

        self.port_naval_base_type.setText(
            port.get("naval_base_type") or ""
        )
        self.port_shipbuilding_capacity.setText(
            port.get("shipbuilding_capacity") or ""
        )

        #Side numbers run clockwise in image coordinates.
        if properties.get("_grid_sideways", True):
            directions = [
                "Upper right",
                "Right",
                "Lower right",
                "Lower left",
                "Left",
                "Upper Left"
            ]
        else:
            directions = [
                "Top",
                "Upper right",
                "Lower right",
                "Bottom",
                "Lower left",
                "Upper left"
            ]

        self.side_help.setText(
            "Sides are numbered clockwise."
            "Directions refer to the map as displayed."
        )

        hexsides = properties.get("hexsides") or {}

        for side, controls in self.hexside_controls.items():
            values = hexsides.get(side, {})

            controls["group"].setTitle(
                f"Side {side} - {directions[int(side)]}"
            )
            controls["waterway"].setCurrentText(
                values.get("waterway", "Unknown")
            )
            controls["navigation"].setCurrentText(
                values.get("navigation", "Unknown")
            )
            controls["border"].setCurrentText(
                values.get("border", "Unknown")
            )
            controls["escarpment"].setCurrentText(
                values.get("escarpment", "Unknown")
            )
            controls["coastal_cliff"].setCurrentText(
                values.get("coastal_cliff", "Unknown")
            )
            controls["fortification"].setCurrentText(
                values.get("fortification", "Unknown")
            )
            controls["high_mountain"].setCurrentText(
                values.get("high_mountain", "Unknown")
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


        port = {
            "type" : self.port_type.currentText(),
            "name" : self.port_name.text().strip(),
            "facilities" : self.port_facilities.currentText(),
            "anchorage" : self.port_anchorage.currentText(),
            "naval_base_type" : (
                self.port_naval_base_type.text().strip() or None
            ),
            "shipbuilding_capacity" : (
                self.port_shipbuilding_capacity.text().strip() or None
            ),
        }

        hexsides = {
            side: {
                "waterway" : controls["waterway"].currentText(),
                "navigation" : controls["navigation"].currentText(),
                "border" : controls["border"].currentText(),
                "escarpment" : controls["escarpment"].currentText(),
                "coastal_cliff" : controls["coastal_cliff"].currentText(),
                "fortification" : controls["fortification"].currentText(),
                "high_mountain" : controls["high_mountain"].currentText(),
            }
            for side, controls in self.hexside_controls.items()
        }

        self.applied.emit({
            "surface" : self.surface_type.currentText(),
            "terrain" : terrain or None,
            "settlement" : settlement, 
            "port" : port,
            "hexsides" : hexsides,
            "review_status" : self.review_status.currentText(),
        })

    def focus_hexside(self, side):
        widget = self.hexside_controls[str(side)]["waterway"]
        widget.setFocus()
        self.scroll_area.ensureWidgetVisible(widget, 20, 40)
