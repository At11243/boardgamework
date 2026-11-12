import sys
import re

from pathlib import Path
import json 

# IDE Run File launches from counters/, without the project package root.
# Module launching already supplies that root and needs no path adjustment.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QFormLayout,
    QComboBox,
    QTextEdit,
    QLineEdit,
    QTabWidget,
    QScrollArea,
    QColorDialog,
    QCheckBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QAction, 
    QKeySequence,
    QColor,
    QPixmap,
)

from counters.counter_browser import CounterBrowser
from counters.unit_storage import write_definitions


project_dir = Path(__file__).resolve().parents[1]

glider_fields = (
    ("tug_attack_modifier", "Tug air attack modifier"),
    ("tug_defense_modifier", "Tug air defense modifier"),
    ("tug_bombing_restriction", "Tug bombing restriction"),
    ("tug_range_modifier", "Tug range modifier"),
)

aircraft_fields = (
    ("attack_factor", "Attack factor"),
    ("aircraft_type_code", "Aircraft type / code"),
    ("air_defense", "Air defense rating"),
    ("close_air_support", "Close air support rating"),
    ("strategic_bombing", "Strategic bombing rating"),
    ("capacity_code", "Capacity / code"),
    ("range", "Range"),
) + glider_fields

ground_fields = (
    ("attack", "Attack rating"),
    ("defense", "Defense rating"),
    ("combat_strength", "Combined combat strength"),
    ("movement", "Movement rating"),
    ("antiaircraft", "Antiaircraft rating"),
    ("capacity", "Capacity, including printed code"),
    ("radius", "Radius"),
    ("cd_level", "Coastal-defense level"),
    ("cd_short", "CD printed short-range component"),
    ("cd_long", "CD printed long-range component"),
    ("fortification_level", "Fortification level"),
    ("printed_rating", "Printed rating / operational code"),
    ("printed_code", "Additional printed code"),
    ("printed_symbol_rating", "Additional value inside symbol"),
)

ground_formats = {
    "Unknown": (),
    "Separate attack / defense / movement": (
        "attack", "defense", "movement", "antiaircraft",
    ),
    "Combined combat strength / movement": (
        "combat_strength", "movement", "antiaircraft",
    ),
    "Antiaircraft": (
        "antiaircraft", "movement",
    ),
    "Transport / capacity": (
        "capacity", "movement",
    ),
    "Headquarters / capacity / radius": (
        "capacity", "movement", "radius",
    ),
    "Coastal defense": (
        "cd_level", "cd_short", "cd_long", "antiaircraft", "printed_code",
    ),
    "Movement only": ("movement", "capacity", "radius"),
    "Operational / code": ("printed_rating", "capacity", "radius"),
    "Fortification level": ("fortification_level",),
}

# Required printed core values, not every field available for a layout.
# UICFB p2; R16a 4.A.3/5 pp19-20 (PDF21-22), 14.B.8 p102 (PDF104).
# Unprinted CD short/long values and optional HQ capacities stay unknown.
ground_required_fields = {
    "Coastal defense": ("cd_level",),
    "Movement only": ("movement",),
    "Operational / code": ("printed_rating",),
    "Fortification level": ("fortification_level",),
}

ground_format_sources = {
    "Movement only": "UICFB p2: HQ and other single movement-value layouts. No combat strength is invented.",
    "Operational / code": "Literal printed OP/ST code; no movement or combat rating implied. R16a 14.B.8, printed p102 / PDF104; 15, printed pp113-116 / PDF115-118.",
    "Fortification level": "R16a 4.A.5, printed p20 / PDF22. Store the printed UR level; no gameplay effects calculated.",
    "Coastal defense": "UICFB p2; R16a 4.A.3.a.i-ii, printed p19 / PDF21. In 3/2, level=3, printed short component=3, long component=2. This editor does not calculate effective short-range gunnery; store printed components only. Unprinted components are optional.",
}


def naval_required_fields(ship_type):
    """Printed metadata layout; never infer a tactical speed from patrol range.

    R16a 5.C.2.e.ii-iii, p32 / PDF34; 5.C.4, p33 / PDF35.
    SSF's rule-defined combat speed is not a printed counter rating.
    """
    core = ("ship_type", "gunnery", "protection")
    code = ship_type.strip().upper()
    if code == "SSF":
        return core + ("patrol_range",)
    if code == "FAS":
        return core + ("printed_bottom_right",)
    return core + ("tactical_speed",)

face_statuses = (
    "Unknown",
    "Not applicable",
    "Full strength",
    "Reduced",
    "Damaged", 
    "Emplaced",
    "Fanatic remnants",
    "Other",
)

back_appearances = (
    "Not yet reviewed",
    "Printed image",
    "Blank color"
)

naval_fields = (
    ("ship_type", "Ship type / code"),
    ("gunnery", "Naval gunnery rating"),
    ("protection", "Protection rating"),
    ("antiaircraft", "Antiaircraft rating"),
    ("torpedo", "Torpedo rating"),
    ("tactical_speed", "Tactical speed"),
    ("patrol_range", "Submarine patrol range (sea zones)"),
    ("printed_bottom_right", "Printed bottom-right value (literal)"),
    ("capacity_code", "Capacity / code"),
    ("ship_name", "Printed ship name"),
)

commander_fields = (
    ("rank", "Rank / printed stars"),
    ("movement_bonus", "Movement bonus"),
    ("attack_bonus", "Combat bonus — attack"),
    ("success_drm", "Success-table DRM"),
    ("attack_cev", "CEV modifier — attack"),
    ("defense_bonus", "Defense bonus"),
    ("defense_cev", "CEV modifier — defense"),
    ("retreat_modifier", "Retreat modifier"),
    ("movement", "Movement rating"),
    ("stacking_modifier", "Stacking modifier"),
    ("name_vehicle", "Printed name / vehicle"),
    ("printed_header", "Printed header / modifier codes"),
    ("printed_lower_line", "Printed lower line (literal)"),
)

unit_type_choices = (
    "Unknown",
    "Armour",
    "Light Armour",
    "Mechanised",
    "Flamethrower Tanks",
    "Assault Gun",
    "Tank Destroyer",
    "Engineer Tanks",
    "Motorcycle",
    "Transport",
    "Static",
    "Quarter Master",
    "Air Quarter Master",
    "River Quarter Master",
    "Supply Terminal",
    "Air Group HQ",
    "Penal",
    "Infantry",
    "Cavalry",
    "Naval Infantry",
    "Bicycle Infantry",
    "Light Infantry",
    "Fortress",
    "Machine Gun",
    "Political Police",
    "Security",
    "Border",
    "Airborne",
    "Air Landing",
    "Glider",
    "Commando/Special Forces",
    "Training",
    "Cavalry/Mechanised",
    "Combat Engineer",
    "Construction Engineer",
    "Railway Engineer",
    "Assault Engineer",
    "Beach Engineer",
    "Port Engineer",
    "Artillery",
    "Mortar",
    "Rocket Artillery",
    "Siege Artillery",
    "Railway Siege Artillery",
    "Coastal Defense",
    "Anti Tank",
    "Light Antiaircraft",
    "Reserve",
    "Fortified Region (UR)",
)

unit_size_choices = (
    "Unknown",
    "Not applicable",
    "Wing",
    "Squadron",
    "Battalion",
    "Regiment",
    "Brigade",
    "Division",
    "Corps",
    "Army / Front",
    "Army Group / Direction",
)

unit_descriptors = (
    "Motorized",
    "Air Droppable",
    "Ski",
    "Railway",
    "Mountain",
    "Semi Motorized",
    "Amphibious",
    "Heavy",
)

class UnitEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TSWW Barbarossa — Unit Catalog Editor")
        self.resize(1100, 750)

        self.selected_type_id = None

        self.definitions_path = (
            project_dir
            / "assets"
            / "counters"
            / "unit_definitions.json"
        )

        self.unit_definitions = {}
        self.definitions_metadata = {}
        self.loading_fields = False
        self.dirty = False
        self.storage_ready = False

        try:
            self.load_definitions()
        except (OSError, ValueError, TypeError) as error:
            QMessageBox.critical(
                self,
                "Unit information loading failed",
                str(error),
            )
        else:
            self.storage_ready = True

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        # Reuse the existing searchable counter browser.
        self.browser = CounterBrowser(project_dir, self)
        self.browser.place_button.hide()

        browser_column = QWidget()
        browser_layout = QVBoxLayout(browser_column)

        self.review_filter = QComboBox()
        self.review_filter.addItems([
            "All review statuses",
            "Unreviewed",
            "In progress",
            "Verified",
        ])

        browser_layout.addWidget(QLabel("Review filter"))
        browser_layout.addWidget(self.review_filter)

        browser_layout.addWidget(self.browser)

        navigation = QHBoxLayout()

        self.previous_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")

        navigation.addWidget(self.previous_button)
        navigation.addWidget(self.next_button)
        browser_layout.addLayout(navigation)

        self.next_unreviewed_button = QPushButton(
            "Next unreviewed"
            )
        browser_layout.addWidget(self.next_unreviewed_button)

        self.review_progress= QLabel()
        self.review_progress.setWordWrap(True)
        browser_layout.addWidget(self.review_progress)

        main_layout.addWidget(browser_column, 1)

        # Editable fields will go in this column next.
        fields_column = QWidget()
        self.fields_layout = QVBoxLayout(fields_column)

        self.name_label = QLabel("Select a counter")
        self.name_label.setWordWrap(True)
        self.fields_layout.addWidget(self.name_label)

        self.id_label = QLabel()
        self.fields_layout.addWidget(self.id_label)

        self.fields_widget = QWidget()
        form = QFormLayout(self.fields_widget)

        self.designation = QLineEdit()
        form.addRow("Unit designation", self.designation)

        self.counter_category = QComboBox()
        self.counter_category.addItems([
            "Unknown",
            "Ground unit",
            "Air unit",
            "Naval unit",
            "Commander",
            "Marker",
            "Other",
        ])
        form.addRow("Counter category", self.counter_category)

        self.nationality = QLineEdit()
        form.addRow("Nationality", self.nationality)

        self.service = QLineEdit()
        form.addRow("Service / branch", self.service)

        # Editable so we can enter every chart designation.
        self.unit_type = QComboBox()
        self.unit_type.setEditable(True)
        self.unit_type.setInsertPolicy(
            QComboBox.InsertPolicy.NoInsert
        )
        self.unit_type.addItems(unit_type_choices)
        form.addRow("Unit type", self.unit_type)

        self.unit_size = QComboBox()
        self.unit_size.setEditable(True)
        self.unit_size.setInsertPolicy(
            QComboBox.InsertPolicy.NoInsert
        )
        self.unit_size.addItems(unit_size_choices)
        form.addRow("Unit size", self.unit_size)

        self.front_image = QComboBox()
        form.addRow("Front image", self.front_image)

        self.back_image = QComboBox()
        form.addRow("Back image", self.back_image)

        self.back_appearance = QComboBox()
        self.back_appearance.addItems(back_appearances)
        form.addRow("Back appearance", self.back_appearance)

        self.blank_back_color = "#808080"

        self.back_color_button = QPushButton("Choose blank-back color")
        self.back_color_button.clicked.connect(
            self.choose_blank_back_color
        )
        form.addRow("Blank-back color", self.back_color_button)

        preview_buttons = QWidget()
        preview_layout = QHBoxLayout(preview_buttons)
        preview_layout.setContentsMargins(0, 0, 0, 0)

        preview_front_button = QPushButton("Preview Front")
        preview_back_button = QPushButton("Preview Back")

        preview_front_button.clicked.connect(
            lambda: self.preview_assigned_face("front")
        )
        preview_back_button.clicked.connect(
            lambda: self.preview_assigned_face("back")
        )

        preview_layout.addWidget(preview_front_button)
        preview_layout.addWidget(preview_back_button)
        form.addRow("Assigned faces", preview_buttons)

        self.face_details_tabs = QTabWidget()
        self.face_details_controls = {}

        for face, title in (
            ("front", "Front face identity"),
            ("back", "Back face identity"),
        ):
            page = QWidget()
            face_layout = QFormLayout(page)

            status = QComboBox()
            status.addItems(face_statuses)
            status.currentTextChanged.connect(self.mark_dirty)

            size_override = QComboBox()
            size_override.setEditable(True)
            size_override.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
            size_override.addItems(["Use shared unit size", *unit_size_choices])
            size_override.currentTextChanged.connect(self.mark_dirty)
            size_override.setToolTip("Override the shared Unit size for this face only. This is not printed text.")

            printed_text = QLineEdit()
            printed_text.setPlaceholderText(
                "Only text actually printed, e.g. XX, [XX], Reduced; otherwise blank"
            )
            printed_text.textChanged.connect(self.mark_dirty)

            face_layout.addRow("Face status", status)
            face_layout.addRow("Face unit size", size_override)
            face_layout.addRow(
                "Printed size / status text", printed_text
            )

            descriptors_widget = QWidget()
            descriptors_layout = QVBoxLayout(descriptors_widget)
            descriptors_layout.setContentsMargins(0, 0, 0, 0)

            descriptor_checks = {}

            for name in unit_descriptors:
                checkbox = QCheckBox(name)
                checkbox.toggled.connect(self.mark_dirty)

                descriptors_layout.addWidget(checkbox)
                descriptor_checks[name] = checkbox

            face_layout.addRow(
                "Additional descriptors", descriptors_widget
            )

            self.face_details_controls[face] = {
                "status": status,
                "unit_size_override": size_override,
                "printed_size_status": printed_text,
                "descriptors": descriptor_checks,
            }

            self.face_details_tabs.addTab(page, title)

        form.addRow(self.face_details_tabs)

        self.back_appearance.currentTextChanged.connect(
            self.update_back_controls
        )
        self.back_appearance.currentTextChanged.connect(
            self.mark_dirty
        )

        self.update_back_controls()

        self.review_status = QComboBox()
        self.review_status.addItems([
            "Unreviewed",
            "In progress",
            "Verified",
        ])
        form.addRow("Identification review", self.review_status)

        self.notes = QTextEdit()
        self.notes.setMaximumHeight(100)
        form.addRow("Notes", self.notes)

        self.aircraft_tabs = QTabWidget()
        self.aircraft_controls = {}
        self.aircraft_rows = {}

        for face, title in (
            ("front", "Front aircraft ratings"),
            ("back", "Back aircraft ratings"),
        ):
            page = QWidget()
            face_layout = QFormLayout(page)

            self.aircraft_controls[face] = {}
            self.aircraft_rows[face] = {}

            for field_name, label in aircraft_fields:
                control = QLineEdit()
                control.setPlaceholderText(
                    "Blank = unknown; N/A = not applicable"
                )
                control.textChanged.connect(self.mark_dirty)

                face_layout.addRow(label, control)
                self.aircraft_controls[face][field_name] = control
                self.aircraft_rows[face][field_name] = (face_layout.labelForField(control), control)
                if field_name in dict(glider_fields):
                    control.setToolTip(
                        "Printed effect on the towing aircraft, not an independent glider rating. "
                        "The interpretation of the two -1 markings remains provisional; "
                        "these fields record metadata and do not apply gameplay effects."
                    )
                if field_name == "aircraft_type_code":
                    control.textChanged.connect(self.update_aircraft_fields)

            self.aircraft_tabs.addTab(page, title)

        form.addRow(self.aircraft_tabs)

        self.ground_section = QWidget()
        ground_layout = QVBoxLayout(self.ground_section)

        self.ground_tabs = QTabWidget()
        self.ground_controls = {}
        self.ground_rows = {}
        self.ground_torpedoes = {}
        self.ground_formats = {} 
        self.ground_type_overrides = {} 

        for face, title in (
            ("front", "Front ground ratings"),
            ("back", "Back ground ratings"),
        ):
            page = QWidget()
            face_layout = QFormLayout(page)

            self.ground_controls[face] = {}
            self.ground_rows[face] = {}

            format_choice = QComboBox()
            format_choice.addItems(list(ground_formats.keys()))

            format_choice.currentTextChanged.connect(
                self.update_ground_fields
            )
            format_choice.currentTextChanged.connect(
                self.mark_dirty
            )

            face_layout.addRow("Rating format", format_choice)
            self.ground_formats[face] = format_choice

            type_override = QComboBox()
            type_override.setEditable(True)
            type_override.setInsertPolicy(
                QComboBox.InsertPolicy.NoInsert
            )

            type_override.addItem("Use shared unit type", None)

            for name in unit_type_choices:
                if name != "Unknown":
                    type_override.addItem(name, name)

            type_override.currentTextChanged.connect(
                self.mark_dirty
            )

            face_layout.addRow(
                "Face unit type", type_override
            )
            self.ground_type_overrides[face] = type_override

            for field_name, label in ground_fields:
                control = QLineEdit()
                control.setPlaceholderText(
                    "Blank = unknown; N/A = not applicable"
                )
                control.textChanged.connect(self.mark_dirty)

                label_widget = QLabel(label)
                if field_name == "combat_strength":
                    control.setToolTip("Keep parentheses literally, e.g. (1). R16a 5.A.2, printed p25 / PDF27; this is not automatically a defense-only rating.")
                elif field_name in ("cd_level", "cd_short", "cd_long"):
                    control.setToolTip(ground_format_sources["Coastal defense"])
                face_layout.addRow(label_widget, control)

                self.ground_controls[face][field_name] = control
                self.ground_rows[face][field_name] = (
                    label_widget, control
                )

            torpedoes = QComboBox()
            torpedoes.addItems([
                "Unknown",
                "Absent",
                "Present",
            ])
            torpedoes.currentTextChanged.connect(self.mark_dirty)

            torpedoes_label = QLabel("Torpedoes present")
            face_layout.addRow(torpedoes_label, torpedoes)

            self.ground_torpedoes[face] = torpedoes
            self.ground_rows[face]["torpedoes"] = (
                torpedoes_label, torpedoes
            )

            self.ground_tabs.addTab(page, title)

        ground_layout.addWidget(self.ground_tabs)
        form.addRow(self.ground_section)

        self.special_rating_controls = {}
        self.special_rating_tabs = {}
        self.naval_rows = {}

        for category, section_name, fields in (
            ("Naval unit", "naval", naval_fields),
            ("Commander", "commander", commander_fields),
        ):
            tabs = QTabWidget()

            self.special_rating_tabs[category] = tabs
            self.special_rating_controls[section_name] = {}

            for face, title in (
                ("front", "Front ratings"),
                ("back", "Back ratings"),
            ):
                page = QWidget()
                face_layout = QFormLayout(page)

                controls = {}
                if section_name == "naval":
                    self.naval_rows[face] = {}
                self.special_rating_controls[section_name][face] = (
                    controls
                )

                for field_name, label in fields:
                    control = QLineEdit()
                    control.setPlaceholderText(
                        "Blank = unknown; N/A = not applicable"
                    )
                    control.textChanged.connect(self.mark_dirty)

                    label_widget = QLabel(label)
                    face_layout.addRow(label_widget, control)
                    controls[field_name] = control
                    if section_name == "naval":
                        self.naval_rows[face][field_name] = (label_widget, control)
                        if field_name == "ship_type":
                            control.textChanged.connect(self.update_naval_fields)
                        if field_name in ("tactical_speed", "patrol_range", "printed_bottom_right"):
                            control.setToolTip("R16a 5.C.2.e, printed p32 / PDF34; 5.C.4, p33 / PDF35. SSF uses patrol range; SSF/FAS do not print tactical speed. Keep an unexplained bottom-right value literally without assigning it a gameplay meaning.")
                    elif field_name not in ("rank", "movement", "name_vehicle"):
                        control.setToolTip("UICFB p2: unprinted commander modifiers have no effect. Leave unprinted values blank; do not invent zero or N/A. Codes M/C/D/R may be recorded literally; effects are not implemented.")

                tabs.addTab(page, title)

            form.addRow(tabs)

        self.update_ground_fields()
        self.update_naval_fields()

        # Scroll the fields while keeping Save visible below.
        fields_scroll = QScrollArea()
        fields_scroll.setWidgetResizable(True)
        fields_scroll.setWidget(self.fields_widget)

        self.fields_layout.addWidget(fields_scroll, 1)

        self.counter_category.currentTextChanged.connect(
            self.update_category_fields
        )
        self.unit_type.currentTextChanged.connect(self.update_aircraft_fields)
        self.update_category_fields()

        self.check_button = QPushButton("Check Definition")
        self.check_button.clicked.connect(self.check_definition)
        self.fields_layout.addWidget(self.check_button)
        self.save_button = QPushButton("Save Unit Information")
        self.fields_layout.addWidget(self.save_button)
        self.fields_layout.addStretch()

        self.fields_widget.setEnabled(False)
        self.save_button.setEnabled(False)
        self.check_button.setEnabled(False)

        self.save_button.clicked.connect(self.save_definition)

        save_action = QAction("Save Unit Information", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_definition)
        self.addAction(save_action)

        for field in (
            self.designation,
            self.nationality,
            self.service,
        ):
            field.textChanged.connect(self.mark_dirty)

        for field in (
            self.counter_category,
            self.unit_type,
            self.unit_size,
            self.front_image,
            self.back_image,
            self.review_status,
        ):
            field.currentTextChanged.connect(self.mark_dirty)

        self.notes.textChanged.connect(self.mark_dirty)

        main_layout.addWidget(fields_column, 2)

        self.previous_button.clicked.connect(
            lambda: self.move_selection(-1)
        )
        self.next_button.clicked.connect(
            lambda: self.move_selection(1)
        )

        self.browser.results.currentItemChanged.connect(
            self.show_definition
        )

        # Resolve unsaved edits before rebuilding the search list.
        self.browser.search.textChanged.disconnect(
            self.browser.filter_counters
        )
        self.browser.search.textChanged.connect(
            self.apply_review_filter
        )

        self.review_filter.currentTextChanged.connect(
            self.apply_review_filter
        )
        self.next_unreviewed_button.clicked.connect(
            self.jump_to_unreviewed
        )

        self.accepted_search = self.browser.search.text()
        self.accepted_review_filter = (
            self.review_filter.currentText()
        )

        catalog_path = (
            project_dir
            / "assets"
            / "counters"
            / "counter_catalog.json"
        )

        try:
            self.browser.load_catalog(catalog_path)
        except (OSError, ValueError, TypeError, AttributeError) as error:
            QMessageBox.critical(
                self,
                "Catalog loading failed",
                str(error),
            )
            self.statusBar().showMessage("Catalog loading failed")
            return

        self.refresh_review_progress()
        self.jump_to_unreviewed(first=True)

    def saved_review_status(self, type_id):
        return self.unit_definitions.get(type_id, {}).get(
            "review_status", "Unreviewed"
        )

    def refresh_review_progress(self):
        self.browser.update_review_indicators(
            self.unit_definitions
        )

        counts = {
            "Unreviewed": 0,
            "In progress": 0,
            "Verified": 0,
        }

        for type_id in self.browser.counter_types:
            status = self.saved_review_status(type_id)
            counts[status] = counts.get(status, 0) + 1

        total = len(self.browser.counter_types)

        self.review_progress.setText(
            f"{counts['Verified']} of {total} verified\n"
            f"{counts['In progress']} in progress"
            f" | {counts['Unreviewed']} unreviewed"
        )

    def refresh_review_visibility(self):
        """Update saved-status filtering without deleting live selection items."""
        visible_count = 0
        wanted = self.review_filter.currentText()
        for row in range(self.browser.results.count()):
            item = self.browser.results.item(row)
            status = self.saved_review_status(item.data(Qt.ItemDataRole.UserRole))
            visible = wanted == "All review statuses" or status == wanted
            item.setHidden(not visible)
            visible_count += int(visible)
        self.browser.count_label.setText(f"{visible_count} matching counter definitions")

    def apply_review_filter(self, *_):
        if not self.finish_pending_edits():
            self.browser.search.blockSignals(True)
            self.browser.search.setText(self.accepted_search)
            self.browser.search.blockSignals(False)

            self.review_filter.blockSignals(True)
            self.review_filter.setCurrentText(
                self.accepted_review_filter
            )
            self.review_filter.blockSignals(False)
            return

        self.accepted_search = self.browser.search.text()
        self.accepted_review_filter = (
            self.review_filter.currentText()
        )

        selected_id = self.selected_type_id
        results = self.browser.results

        # Rebuild without intermediate selection-change events.
        results.blockSignals(True)

        try:
            self.browser.filter_counters()

            selected_row = None
            first_visible = None
            visible_count = 0

            for row in range(results.count()):
                item = results.item(row)
                type_id = item.data(Qt.ItemDataRole.UserRole)
                status = self.saved_review_status(type_id)

                visible = (
                    self.accepted_review_filter
                    == "All review statuses"
                    or status == self.accepted_review_filter
                )

                item.setHidden(not visible)

                if visible:
                    visible_count += 1

                    if first_visible is None:
                        first_visible = row

                    if type_id == selected_id:
                        selected_row = row

            target = (
                selected_row
                if selected_row is not None
                else first_visible
            )

            results.setCurrentRow(
                target if target is not None else -1
            )

        finally:
            results.blockSignals(False)

        current = results.currentItem()
        self.browser.show_counter(current, None)
        self.show_definition(current, None)

        self.browser.count_label.setText(
            f"{visible_count} matching counter definitions"
        )
        self.refresh_review_progress()

    def jump_to_unreviewed(self, *_args, first=False):
        if not self.finish_pending_edits():
            return

        # Search across the catalog rather than the current filter.
        self.browser.search.blockSignals(True)
        self.browser.search.clear()
        self.browser.search.blockSignals(False)

        self.review_filter.blockSignals(True)
        self.review_filter.setCurrentText("All review statuses")
        self.review_filter.blockSignals(False)

        self.apply_review_filter()

        results = self.browser.results
        current_row = results.currentRow()
        count = results.count()

        if first:
            order = list(range(count))
        else:
            order = (
                list(range(current_row + 1, count))
                + list(range(0, current_row + 1))
            )

        for wanted_status in ("Unreviewed", "In progress"):
            for row in order:
                item = results.item(row)
                type_id = item.data(Qt.ItemDataRole.UserRole)

                if self.saved_review_status(type_id) == wanted_status:
                    results.setCurrentRow(row)
                    results.scrollToItem(item)
                    return

        if count and first:
            results.setCurrentRow(0)

        self.statusBar().showMessage(
            "No unreviewed or in-progress counters remain."
        )

    def move_selection(self, direction):
        results = self.browser.results
        current = results.currentRow()

        if current < 0:
            row = 0 if direction > 0 else results.count() - 1
        else:
            row = current + direction

        while 0 <= row < results.count():
            item = results.item(row)

            if not item.isHidden():
                results.setCurrentRow(row)
                results.scrollToItem(item)
                return

            row += direction

    def suggested_counter_faces(self, record):
        fronts = []
        backs = []

        for name, path in zip(
            record.get("image_names", []),
            record.get("image_paths", []),
        ):
            filename = Path(name).stem

            is_back = re.search(
                r"(?:^|[\s._-])back(?:$|[\s._-])",
                filename,
                flags=re.IGNORECASE,
            )

            if is_back:
                backs.append(path)
            else:
                fronts.append(path)

        # Only assign automatically when the choice is clear.
        front = fronts[0] if len(fronts) == 1 else None
        back = backs[0] if len(backs) == 1 else None

        return {
            "front_image": front,
            "back_image": back,
        }

    def update_category_fields(self, *_):
        category = self.counter_category.currentText()

        self.aircraft_tabs.setVisible(category == "Air unit")
        self.update_aircraft_fields()
        self.ground_section.setVisible(category == "Ground unit")

        for section_category, tabs in self.special_rating_tabs.items():
            tabs.setVisible(category == section_category)

    def is_glider_face(self, face):
        return (self.unit_type.currentText().strip().casefold() == "glider"
                or self.aircraft_controls[face]["aircraft_type_code"].text().strip().upper() == "G")

    def update_aircraft_fields(self, *_):
        for face, rows in self.aircraft_rows.items():
            glider = self.is_glider_face(face)
            for field, widgets in rows.items():
                if field in ("aircraft_type_code", "capacity_code"):
                    visible = True
                else:
                    visible = (field in dict(glider_fields)) == glider
                for widget in widgets:
                    widget.setVisible(visible)

    def update_ground_fields(self, *_):
        for face, rows in self.ground_rows.items():
            selected_format = (
                self.ground_formats[face].currentText()
            )
            visible_fields = ground_formats.get(
                selected_format, ()
            )
            self.ground_formats[face].setToolTip(ground_format_sources.get(selected_format, "UICFB p2. Printed counter metadata only; gameplay remains manual."))

            for field_name, widgets in rows.items():
                if field_name == "torpedoes":
                    visible = selected_format == "Coastal defense"
                else:
                    visible = (field_name in visible_fields
                               or field_name in ("printed_symbol_rating", "printed_rating"))

                for widget in widgets:
                    widget.setVisible(visible)

    def update_naval_fields(self, *_):
        for face, rows in self.naval_rows.items():
            code = self.special_rating_controls["naval"][face]["ship_type"].text().strip().upper()
            for field, widgets in rows.items():
                visible = (code == "SSF" if field == "patrol_range" else
                           code not in ("SSF", "FAS") if field == "tactical_speed" else True)
                for widget in widgets:
                    widget.setVisible(visible)

    def update_back_controls(self, *_):
        appearance = self.back_appearance.currentText()

        self.back_image.setEnabled(
            appearance == "Printed image"
        )
        self.back_color_button.setEnabled(
            appearance == "Blank color"
        )
        self.back_color_button.setText(
            f"Choose color ({self.blank_back_color})"
        )

    def choose_blank_back_color(self):
        color = QColorDialog.getColor(
            QColor(self.blank_back_color),
            self,
            "Choose blank reverse color",
        )

        if not color.isValid():
            return

        self.blank_back_color = color.name()
        self.update_back_controls()
        self.mark_dirty()
        self.preview_assigned_face("back")

    def suggested_blank_back_color(self):
        relative_path = self.front_image.currentData()

        if not relative_path:
            return "#808080"

        pixmap = QPixmap(str(project_dir / relative_path))

        if pixmap.isNull():
            return "#808080"

        image = pixmap.toImage()

        # A suggested background color from near the top-left.
        # Use the color picker if this hits text or a border.
        x = min(3, image.width() - 1)
        y = min(3, image.height() - 1)

        color = image.pixelColor(x, y)

        if color.alpha() == 0:
            return "#808080"

        return color.name()

    def preview_assigned_face(self, face):
        if self.selected_type_id is None:
            return

        if face == "front":
            relative_path = self.front_image.currentData()

            if not relative_path:
                self.browser.preview.clear()
                self.browser.preview.setText(
                    "No front image assigned."
                )
                return

            pixmap = QPixmap(str(project_dir / relative_path))

        else:
            appearance = self.back_appearance.currentText()

            if appearance == "Blank color":
                front_path = self.front_image.currentData()

                if not front_path:
                    self.browser.preview.clear()
                    self.browser.preview.setText(
                        "Assign a front image first."
                    )
                    return

                front_pixmap = QPixmap(
                    str(project_dir / front_path)
                )

                if front_pixmap.isNull():
                    self.browser.preview.clear()
                    self.browser.preview.setText(
                        "Cannot load the front image."
                    )
                    return

                # Generate a reverse at the front's dimensions.
                pixmap = QPixmap(front_pixmap.size())
                pixmap.fill(QColor(self.blank_back_color))

            elif appearance == "Printed image":
                relative_path = self.back_image.currentData()

                if not relative_path:
                    self.browser.preview.clear()
                    self.browser.preview.setText(
                        "No printed back image assigned."
                    )
                    return

                pixmap = QPixmap(
                    str(project_dir / relative_path)
                )

            else:
                self.browser.preview.clear()
                self.browser.preview.setText(
                    "Back appearance has not been reviewed."
                )
                return

        if pixmap.isNull():
            self.browser.preview.clear()
            self.browser.preview.setText(
                "Cannot load the assigned image."
            )
            return

        self.browser.preview.setPixmap(
            pixmap.scaled(
                160,
                160,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def show_definition(self, current, previous):
        if not self.finish_pending_edits():
            # Restore the previous selection without triggering
            # another selection-change event.
            results = self.browser.results
            results.blockSignals(True)
            results.setCurrentItem(previous)
            results.blockSignals(False)

            self.browser.show_counter(previous, current)
            return

        self.loading_fields = True

        try:
            self.selected_type_id = None
            self.fields_widget.setEnabled(False)
            self.save_button.setEnabled(False)
            self.check_button.setEnabled(False)

            if current is None:
                self.name_label.setText("Select a counter")
                self.id_label.clear()
                self.statusBar().showMessage("No counter selected")
                return

            self.selected_type_id = current.data(
                Qt.ItemDataRole.UserRole
            )

            record = self.browser.counter_types[
                self.selected_type_id
            ]

            values = self.unit_definitions.get(
                self.selected_type_id, {}
            )

            self.name_label.setText(record["name"])
            self.id_label.setText(
                f"Definition ID: {self.selected_type_id}"
            )

            self.designation.setText(
                values.get("designation", record["name"])
            )
            self.counter_category.setCurrentText(
                values.get("counter_category", "Unknown")
            )
            self.nationality.setText(
                values.get("nationality", "")
            )
            self.service.setText(
                values.get("service", "")
            )
            self.unit_type.setCurrentText(
                values.get("unit_type", "Unknown")
            )
            self.unit_size.setCurrentText(
                values.get("unit_size", "Unknown")
            )
            self.review_status.setCurrentText(
                values.get("review_status", "Unreviewed")
            )
            self.notes.setPlainText(values.get("notes", ""))

            aircraft = values.get("aircraft", {})

            for face, controls in self.aircraft_controls.items():
                face_values = aircraft.get(face, {})

                for field_name, control in controls.items():
                    value = face_values.get(field_name)
                    control.setText(
                        "" if value is None else value
                    )

            self.aircraft_tabs.setCurrentIndex(0)

            ground = values.get("ground", {})

            # Older saves stored one format for both faces.
            legacy_format = ground.get("format", "Unknown")

            for face, controls in self.ground_controls.items():
                face_values = ground.get(face, {})

                self.ground_formats[face].setCurrentText(
                    face_values.get("format", legacy_format)
                )

                override = face_values.get("unit_type_override")
                type_choice = self.ground_type_overrides[face]

                if override is None:
                    type_choice.setCurrentIndex(0)
                else:
                    type_choice.setCurrentText(override)

                for field_name, control in controls.items():
                    value = face_values.get(field_name)
                    control.setText(
                        "" if value is None else value
                    )

                self.ground_torpedoes[face].setCurrentText(
                    face_values.get("torpedoes", "Unknown")
                )

            self.ground_tabs.setCurrentIndex(0)
            self.update_ground_fields()

            for section_name, faces in (
                self.special_rating_controls.items()
            ):
                section_values = values.get(section_name, {})

                for face, controls in faces.items():
                    face_values = section_values.get(face, {})

                    for field_name, control in controls.items():
                        value = face_values.get(field_name)
                        control.setText(
                            "" if value is None else value
                        )

            for tabs in self.special_rating_tabs.values():
                tabs.setCurrentIndex(0)
            
            self.update_category_fields()

            suggested_faces = self.suggested_counter_faces(record)

            for combo, field_name in (
                (self.front_image, "front_image"),
                (self.back_image, "back_image"),
            ):
                combo.clear()
                combo.addItem("Not assigned", None)

                for image_name, image_path in zip(
                    record.get("image_names", []),
                    record.get("image_paths", []),
                ):
                    combo.addItem(image_name, image_path)

                saved_path = values.get(field_name)

                if field_name not in values:
                    saved_path = suggested_faces[field_name]

                # Keep a saved assignment visible even if a
                # later import no longer lists that image.
                index = combo.findData(saved_path)

                if saved_path is not None and index < 0:
                    combo.addItem(
                        f"Previously assigned: {saved_path}",
                        saved_path,
                    )
                    index = combo.count() - 1

                combo.setCurrentIndex(max(0, index))

            saved_appearance = values.get("back_appearance")

            if saved_appearance is None:
                saved_appearance = (
                    "Printed image"
                    if self.back_image.currentData() is not None
                    else "Not yet reviewed"
                )

            self.back_appearance.setCurrentText(saved_appearance)

            self.blank_back_color = values.get(
                "blank_back_color",
                self.suggested_blank_back_color(),
            )

            faces = values.get("faces", {})

            for face, controls in self.face_details_controls.items():
                face_values = faces.get(face, {})

                controls["status"].setCurrentText(
                    face_values.get("status", "Unknown")
                )
                controls["unit_size_override"].setCurrentText(
                    face_values.get("unit_size_override") or "Use shared unit size"
                )
                controls["printed_size_status"].setText(
                    face_values.get("printed_size_status", "")
                )

                descriptors = face_values.get("descriptors", [])

                for name, checkbox in controls["descriptors"].items():
                    checkbox.setChecked(name in descriptors)

            self.face_details_tabs.setCurrentIndex(0)
            self.update_back_controls()

            self.fields_widget.setEnabled(self.storage_ready)
            self.save_button.setEnabled(self.storage_ready)
            self.check_button.setEnabled(self.storage_ready)

            self.dirty = False
            self.statusBar().showMessage(
                f"Counter {self.browser.results.currentRow() + 1}"
                f" of {self.browser.results.count()}"
            )

        finally:
            self.loading_fields = False

    def load_definitions(self):
        if not self.definitions_path.is_file():
            return

        data = json.loads(
            self.definitions_path.read_text(encoding="utf-8")
        )

        if (
            not isinstance(data, dict)
            or data.get("format")
            != "tsww-barbarossa-unit-definitions"
            or data.get("version") != 1
            or not isinstance(data.get("definitions"), dict)
        ):
            raise ValueError("Invalid unit definitions file.")

        definitions = data["definitions"]

        for type_id, values in definitions.items():
            if (
                not isinstance(type_id, str)
                or not isinstance(values, dict)
            ):
                raise ValueError("Invalid unit definition record.")

            for field in (
                "designation",
                "counter_category",
                "nationality",
                "service",
                "unit_type",
                "unit_size",
                "review_status",
                "notes",
            ):
                if field in values and not isinstance(
                    values[field], str
                ):
                    raise ValueError(
                        f"Invalid {field} for {type_id}."
                    )

            for field in ("front_image", "back_image"):
                value = values.get(field)

                if value is not None and not isinstance(value, str):
                    raise ValueError(
                        f"Invalid {field} for {type_id}."
                    )

            aircraft = values.get("aircraft", {})

            if not isinstance(aircraft, dict):
                raise ValueError(
                    f"Invalid aircraft information for {type_id}."
                )

            for face in ("front", "back"):
                face_values = aircraft.get(face, {})

                if not isinstance(face_values, dict):
                    raise ValueError(
                        f"Invalid {face} aircraft ratings for {type_id}."
                    )

                for field_name, label in aircraft_fields:
                    value = face_values.get(field_name)
                
                    if value is not None and not isinstance(value, str):
                        raise ValueError(
                            f"Invalid {face} {label} for {type_id}."
                        )    

            ground = values.get("ground", {})

            if not isinstance(ground, dict):
                raise ValueError(
                    f"Invalid ground information for {type_id}."
                )

            legacy_format = ground.get("format", "Unknown")

            if legacy_format not in ground_formats:
                raise ValueError(
                    f"Invalid ground counter format for {type_id}."
                )

            for face in ("front", "back"):
                face_values = ground.get(face, {})

                if not isinstance(face_values, dict):
                    raise ValueError(
                        f"Invalid {face} ground ratings for {type_id}."
                    )

                face_format = face_values.get(
                    "format", legacy_format
                )

                if face_format not in ground_formats:
                    raise ValueError(
                        f"Invalid {face} ground format for {type_id}."
                    )

                override = face_values.get("unit_type_override")

                if override is not None and not isinstance(
                    override, str
                ):
                    raise ValueError(
                        f"Invalid {face} unit-type override"
                        f"for {type_id}."
                    )

                for field_name, label in ground_fields:
                    value = face_values.get(field_name)

                    if value is not None and not isinstance(value, str):
                        raise ValueError(
                            f"Invalid {face} {label} for {type_id}."
                        )

                if face_values.get("torpedoes", "Unknown") not in (
                    "Unknown",
                    "Absent", 
                    "Present",
                ):
                    raise ValueError(
                        f"Invalid {face} torpedo indicator for {type_id}."
                    )
                
            if ground.get("format", "Unknown") not in ground_formats:
                raise ValueError(
                    f"Invalid ground counter format for {type_id}."
                )

            for face in ("front", "back"):
                face_values = ground.get(face, {})

                if not isinstance(face_values, dict):
                    raise ValueError(
                        f"Invalid {face} ground ratings for {type_id}."
                    )

                for field_name, label in ground_fields:
                    value = face_values.get(field_name)

                    if value is not None and not isinstance(value, str):
                        raise ValueError(
                            f"Invalid {face} {label} for {type_id}."
                        )

                if face_values.get("torpedoes", "Unknown") not in (
                    "Unknown",
                    "Absent",
                    "Present",
                ):
                    raise ValueError(
                        f"Invalid {face} torpedo indicator for {type_id}."
                    )

            appearance = values.get(
                "back_appearance", "Not yet reviewed"
            )

            if appearance not in back_appearances:
                raise ValueError(
                    f"Invalid back appearance for {type_id}."
                )

            color = values.get("blank_back_color", "#808080")

            if (
                not isinstance(color, str)
                or re.fullmatch(r"#[0-9a-fA-F]{6}", color) is None
            ):
                raise ValueError(
                    f"Invalid blank-back color for {type_id}."
                )

            faces = values.get("faces", {})

            if not isinstance(faces, dict):
                raise ValueError(
                    f"Invalid face information for {type_id}."
                )

            for face in ("front", "back"):
                face_values = faces.get(face, {})

                if not isinstance(face_values, dict):
                    raise ValueError(
                        f"Invalid {face} information for {type_id}."
                    )

                override = face_values.get("unit_size_override")
                if override is not None and not isinstance(override, str):
                    raise ValueError(f"Invalid {face} unit-size override for {type_id}.")

                if face_values.get("status", "Unknown") not in face_statuses:
                    raise ValueError(
                        f"Invalid {face} status for {type_id}."
                    )

                if not isinstance(
                    face_values.get("printed_size_status", ""),
                    str,
                ):
                    raise ValueError(
                        f"Invalid {face} printed text for {type_id}."
                    )

                descriptors = face_values.get("descriptors", [])

                if (
                    not isinstance(descriptors, list)
                    or not all(
                        isinstance(name, str)
                        for name in descriptors
                    )
                ):
                    raise ValueError(
                        f"Invalid {face} descriptors for {type_id}."
                    )                

            for section_name, fields in (
                ("naval", naval_fields),
                ("commander", commander_fields),
            ):
                section_values = values.get(section_name, {})

                if not isinstance(section_values, dict):
                    raise ValueError(
                        f"Invalid {section_name} information "
                        f"for {type_id}."
                    )

                for face in ("front", "back"):
                    face_values = section_values.get(face, {})

                    if not isinstance(face_values, dict):
                        raise ValueError(
                            f"Invalid {face} {section_name} ratings "
                            f"for {type_id}."
                        )

                    for field_name, label in fields:
                        value = face_values.get(field_name)

                        if value is not None and not isinstance(
                            value, str
                        ):
                            raise ValueError(
                                f"Invalid {face} {label} "
                                f"for {type_id}."
                            )

        self.unit_definitions = definitions
        self.definitions_metadata = {
            key: value for key, value in data.items()
            if key not in ("format", "version", "definitions")
        }

    def definition_issues(self):
        """Check current edits for completeness, not TSWW rule correctness."""
        issues = []
        for label, value in (
            ("Unit designation", self.designation.text()),
            ("Counter category", self.counter_category.currentText()),
            ("Nationality", self.nationality.text()),
            ("Service / branch", self.service.text()),
            ("Unit type", self.unit_type.currentText()),
        ):
            if not value.strip() or value.strip().casefold() == "unknown":
                issues.append(f"{label}: missing or unknown (use N/A if not applicable).")

        appearance = self.back_appearance.currentText()
        if appearance == "Not yet reviewed":
            issues.append("Back appearance: not yet reviewed.")
        for face, combo in (("Front", self.front_image), ("Back", self.back_image)):
            path = combo.currentData()
            required = face == "Front" or appearance == "Printed image"
            if face == "Back" and appearance == "Blank color":
                continue
            if not path:
                if required:
                    issues.append(f"{face} image: not assigned.")
            elif QPixmap(str(project_dir / path)).isNull():
                issues.append(f"{face} image: missing or unreadable ({path}).")
        if (appearance == "Printed image" and self.front_image.currentData()
                and self.front_image.currentData() == self.back_image.currentData()):
            issues.append("Front and back use the same image; review assignments.")

        category = self.counter_category.currentText()
        for face in ("front", "back"):
            if face == "back" and appearance == "Blank color":
                continue
            override = self.face_details_controls[face]["unit_size_override"].currentText().strip()
            size = (self.unit_size.currentText().strip()
                    if override in ("", "Use shared unit size") else override)
            if not size or size.casefold() == "unknown":
                issues.append(f"{face.title()} unit size: missing or unknown (use N/A if not applicable).")
            if category == "Ground unit":
                rating_format = self.ground_formats[face].currentText()
                if rating_format == "Unknown":
                    issues.append(f"{face.title()} ground ratings: select a rating format.")
                # AA is optional except on dedicated antiaircraft counters.
                required = tuple(
                    field for field in ground_required_fields.get(
                        rating_format, ground_formats.get(rating_format, ()))
                    if field != "antiaircraft" or rating_format == "Antiaircraft"
                )
                controls = self.ground_controls[face]
                labels = dict(ground_fields)
            elif category == "Air unit":
                required = (("aircraft_type_code", "capacity_code")
                            + tuple(name for name, _ in glider_fields)
                            if self.is_glider_face(face) else
                            ("attack_factor", "aircraft_type_code", "air_defense", "range"))
                controls = self.aircraft_controls[face]
                labels = dict(aircraft_fields)
            elif category in ("Naval unit", "Commander"):
                section = "naval" if category == "Naval unit" else "commander"
                controls = self.special_rating_controls[section][face]
                required = (naval_required_fields(controls["ship_type"].text())
                            if section == "naval" else ("rank", "movement"))
                labels = dict(naval_fields if section == "naval" else commander_fields)
            else:
                continue
            for field in required:
                value = controls[field].text().strip()
                if not value or value.casefold() == "unknown":
                    issues.append(f"{face.title()} ratings: {labels[field]} missing or unknown.")
        return issues

    def check_definition(self, *_):
        if self.selected_type_id is None:
            return
        issues = self.definition_issues()
        QMessageBox.information(
            self, "Check Definition",
            ("Issues to review:\n\n" + "\n".join(f"• {issue}" for issue in issues)
             if issues else "No completeness issues found.")
            + "\n\nMetadata completeness only; ratings and gameplay rules still require manual review."
        )

    def confirm_verified_issues(self, issues):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Definition needs review")
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setText("This definition has unresolved completeness issues.")
        dialog.setInformativeText("\n".join(f"• {issue}" for issue in issues))
        editing = dialog.addButton("Return to Editing", QMessageBox.ButtonRole.RejectRole)
        progress = dialog.addButton("Save as In Progress", QMessageBox.ButtonRole.AcceptRole)
        dialog.setDefaultButton(editing)
        dialog.setEscapeButton(editing)
        dialog.exec()
        return dialog.clickedButton() == progress

    def mark_dirty(self, *_):
        if self.loading_fields or self.selected_type_id is None:
            return

        self.dirty = True
        self.statusBar().showMessage("Unsaved unit information")

    def save_definition(self, *_, refresh_selection=True):
        if not self.storage_ready:
            return False

        type_id = self.selected_type_id

        if type_id is None:
            return False

        front = self.front_image.currentData()
        back = self.back_image.currentData()

        saved_status = self.review_status.currentText()
        if saved_status == "Verified":
            issues = self.definition_issues()
            if issues:
                if not self.confirm_verified_issues(issues):
                    return False
                saved_status = "In progress"

        # Preserve any additional fields added in future steps.
        updated = self.unit_definitions.get(type_id, {}).copy()

        updated.update({
            "designation": self.designation.text().strip(),
            "counter_category":
                self.counter_category.currentText(),
            "nationality": self.nationality.text().strip(),
            "service": self.service.text().strip(),
            "unit_type": self.unit_type.currentText().strip(),
            "unit_size": self.unit_size.currentText().strip(),
            "front_image": front,
            "back_image": back,
            "review_status": saved_status,
            "notes": self.notes.toPlainText(),
        })

        if self.counter_category.currentText() == "Air unit":
            aircraft = updated.get("aircraft", {}).copy()

            for face, controls in self.aircraft_controls.items():
                face_values = aircraft.get(face, {}).copy()

                for field_name, control in controls.items():
                    text = control.text().strip()
                    face_values[field_name] = text or None

                aircraft[face] = face_values

            updated["aircraft"] = aircraft

        if self.counter_category.currentText() == "Ground unit":
            ground = updated.get("ground", {}).copy()

            # Each face now stores its own format.
            ground.pop("format", None)

            for face, controls in self.ground_controls.items():
                face_values = ground.get(face, {}).copy()

                face_values["format"] = (
                    self.ground_formats[face].currentText()
                )

                override_text = (
                    self.ground_type_overrides[face]
                    .currentText()
                    .strip()
                )

                face_values["unit_type_override"] = (
                    None
                    if override_text in ("", "Use shared unit type")
                    else override_text
                )

                for field_name, control in controls.items():
                    text = control.text().strip()
                    face_values[field_name] = text or None

                face_values["torpedoes"] = (
                    self.ground_torpedoes[face].currentText()
                )

                ground[face] = face_values

            updated["ground"] = ground

        appearance = self.back_appearance.currentText()

        updated["back_appearance"] = appearance
        updated["blank_back_color"] = self.blank_back_color

        faces = updated.get("faces", {}).copy()

        for face, controls in self.face_details_controls.items():
            face_values = faces.get(face, {}).copy()

            # Preserve any descriptors from a newer file version.
            descriptors = [
                name
                for name in face_values.get("descriptors", [])
                if name not in unit_descriptors
            ]

            descriptors.extend(
                name
                for name, checkbox in controls["descriptors"].items()
                if checkbox.isChecked()
            )

            face_values.update({
                "status": controls["status"].currentText(),
                "unit_size_override": (
                    None if controls["unit_size_override"].currentText().strip() in ("", "Use shared unit size")
                    else controls["unit_size_override"].currentText().strip()
                ),
                "printed_size_status":
                    controls["printed_size_status"].text().strip(),
                "descriptors": descriptors,
            })

            faces[face] = face_values

        updated["faces"] = faces

        category = self.counter_category.currentText()

        active_section = {
            "Naval unit": "naval",
            "Commander": "commander",
        }.get(category)

        if active_section is not None:
            section_values = updated.get(
                active_section, {}
            ).copy()

            for face, controls in (
                self.special_rating_controls[active_section].items()
            ):
                face_values = section_values.get(face, {}).copy()

                for field_name, control in controls.items():
                    text = control.text().strip()
                    face_values[field_name] = text or None

                section_values[face] = face_values

            updated[active_section] = section_values
        
        definitions = self.unit_definitions.copy()
        definitions[type_id] = updated

        data = {
            **self.definitions_metadata,
            "format": "tsww-barbarossa-unit-definitions",
            "version": 1,
            "definitions": definitions,
        }

        try:
            write_definitions(self.definitions_path, data)

        except (OSError, ValueError, TypeError) as error:
            QMessageBox.critical(
                self,
                "Unit information saving failed",
                str(error),
            )
            return False

        self.unit_definitions = definitions
        self.review_status.setCurrentText(saved_status)
        self.dirty = False
        self.refresh_review_progress()
        # Keep the active review filter consistent with the newly saved status.
        if refresh_selection:
            self.apply_review_filter()
        else:
            self.refresh_review_visibility()

        self.statusBar().showMessage(
            f"Saved {updated['designation'] or type_id}"
        )
        return True

    def finish_pending_edits(self):
        if not self.dirty:
            return True

        choice = QMessageBox.question(
            self,
            "Unsaved unit information",
            "Save changes to the current unit?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )

        if choice == QMessageBox.StandardButton.Save:
            # A navigation/filter handler may still hold current/previous items.
            # Rebuilding here would delete them while that handler is running.
            return self.save_definition(refresh_selection=False)

        if choice == QMessageBox.StandardButton.Discard:
            self.dirty = False
            return True

        return False

    def closeEvent(self, event):
        if self.finish_pending_edits():
            event.accept()
        else:
            event.ignore() 

def main():
    app = QApplication(sys.argv)

    window = UnitEditor()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
