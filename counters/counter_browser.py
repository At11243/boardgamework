import json
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QComboBox,
    QLabel,
    QPushButton,
    QCheckBox,
    QMessageBox,
)


class CounterBrowser(QWidget):
    place_requested = Signal(dict)

    def __init__(self, project_dir, parent=None, *, show_review_controls=False):
        super().__init__(parent)

        self.project_dir = Path(project_dir)
        self.counter_types = {}
        self.review_definitions = {}

        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search counter name...")
        layout.addWidget(self.search)

        self.verified_only = QCheckBox("Verified only")
        self.reload_reviews_button = QPushButton("Reload Reviews")
        self.verified_only.setVisible(show_review_controls)
        self.reload_reviews_button.setVisible(show_review_controls)
        layout.addWidget(self.verified_only)
        layout.addWidget(self.reload_reviews_button)
        self.verified_only.toggled.connect(self.filter_counters)
        self.reload_reviews_button.clicked.connect(self.reload_reviews)

        self.results = QListWidget()
        layout.addWidget(self.results)

        layout.addWidget(QLabel("Image / counter state"))

        self.image_choice = QComboBox()
        layout.addWidget(self.image_choice)

        self.preview = QLabel("Select a counter")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setMinimumHeight(160)
        layout.addWidget(self.preview)

        self.place_button = QPushButton("Place on Selected Hex")
        self.place_button.setEnabled(False)
        layout.addWidget(self.place_button)

        self.count_label = QLabel()
        layout.addWidget(self.count_label)

        self.search.textChanged.connect(self.filter_counters)
        self.results.currentItemChanged.connect(self.show_counter)
        self.image_choice.currentIndexChanged.connect(
            self.show_image
        )
        self.place_button.clicked.connect(self.request_placement)

    def load_catalog(self, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))

        if (
            data.get("format") != "tsww-barbarossa-counter-catalog"
            or data.get("version") != 1
            or not isinstance(data.get("counter_types"), dict)
        ):
            raise ValueError("Invalid counter catalog.")

        self.counter_types = data["counter_types"]
        self.filter_counters()

    def filter_counters(self, *_):
        query = self.search.text().strip().casefold()

        self.results.clear()

        for type_id, record in self.counter_types.items():
            if (self.verified_only.isChecked()
                    and self.review_definitions.get(type_id, {}).get("review_status") != "Verified"):
                continue
            searchable = (
                record["name"] + " "
                + " ".join(record.get("palette", []))
            ).casefold()

            if query and query not in searchable:
                continue

            item = QListWidgetItem(record["name"])
            item.setData(Qt.ItemDataRole.UserRole, type_id)
            item.setToolTip(
                " / ".join(record.get("palette", []))
            )
            self.results.addItem(item)

        self.count_label.setText(
            f"{self.results.count()} counter definitions"
        )

        self.update_review_indicators(self.review_definitions)

    def load_review_definitions(self):
        path = self.project_dir / "assets" / "counters" / "unit_definitions.json"
        definitions = {}
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            if (not isinstance(data, dict)
                    or data.get("format") != "tsww-barbarossa-unit-definitions"
                    or data.get("version") != 1
                    or not isinstance(data.get("definitions"), dict)
                    or not all(isinstance(value, dict) for value in data["definitions"].values())):
                raise ValueError("Invalid unit definitions file.")
            definitions = data["definitions"]
        current = self.results.currentItem()
        selected = current.data(Qt.ItemDataRole.UserRole) if current else None
        self.review_definitions = definitions
        self.filter_counters()
        for index in range(self.results.count()):
            item = self.results.item(index)
            if item.data(Qt.ItemDataRole.UserRole) == selected:
                self.results.setCurrentItem(item)
                break

    def reload_reviews(self, *_):
        try:
            self.load_review_definitions()
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "Review Status Loading Failed", str(error))

    def show_counter(self, current, previous):
        self.image_choice.clear()
        self.preview.clear()
        self.place_button.setEnabled(False)

        if current is None:
            self.preview.setText("Select a counter")
            return

        type_id = current.data(Qt.ItemDataRole.UserRole)
        record = self.counter_types[type_id]

        for name, path in zip(
            record.get("image_names", []),
            record.get("image_paths", []),
        ):
            self.image_choice.addItem(name, path)

        if self.image_choice.count() == 0:
            self.preview.setText(
                "Image references need review."
            )
        else:
            self.show_image()

    def show_image(self, *_):
        relative_path = self.image_choice.currentData()

        if not relative_path:
            self.place_button.setEnabled(False)
            return

        pixmap = QPixmap(
            str(self.project_dir / relative_path)
        )

        if pixmap.isNull():
            self.preview.setText("Cannot load this image.")
            self.place_button.setEnabled(False)
            return

        self.preview.setPixmap(
            pixmap.scaled(
                160,
                160,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.place_button.setEnabled(True)

    def request_placement(self):
        item = self.results.currentItem()
        image_path = self.image_choice.currentData()

        if item is None or not image_path:
            return

        type_id = item.data(Qt.ItemDataRole.UserRole)
        record = self.counter_types[type_id]

        self.place_requested.emit({
            "type_id": type_id,
            "name": record["name"],
            "image_path": image_path,
        })

    def update_review_indicators(self, definitions):
        self.review_definitions = definitions

        symbols = {
            "Unreviewed": "○",
            "In progress": "…",
            "Verified": "✓",
        }

        for index in range(self.results.count()):
            item = self.results.item(index)
            type_id = item.data(Qt.ItemDataRole.UserRole)
            record = self.counter_types[type_id]

            status = definitions.get(type_id, {}).get(
                "review_status", "Unreviewed"
            )

            symbol = symbols.get(status, "?")

            item.setText(f"{symbol} {record['name']}")
            item.setToolTip(
                " / ".join(record.get("palette", []))
                + f"\nReview: {status}"
            )
