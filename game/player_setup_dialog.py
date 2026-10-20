"""Local setup and assignments; online/PBEM/AI execution is not implemented here."""
from copy import deepcopy
import json
from uuid import uuid4
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QComboBox, QSpinBox,
    QTableWidget, QTableWidgetItem, QPushButton, QDialogButtonBox, QMessageBox,
)
from rules.sides import SIDES, MODES, max_team_size, validate_setup, validate_roster, count_placed_nations, balanced_assignments


class PlayerSetupDialog(QDialog):
    def __init__(self, view, parent=None):
        super().__init__(parent)
        self.view = view
        self.setup = deepcopy(view.player_setup)
        self.nations = self.setup["nations"]
        self.names = {p["player_id"]: p["name"] for team in self.setup["players"].values() for p in team}
        self.player_ids = {side: [p["player_id"] for p in self.setup["players"][side]] for side in SIDES}
        self.setWindowTitle("Players and Nations")
        self.resize(950, 720)
        layout = QVBoxLayout(self)
        note = QLabel("Axis players × Allied players. Whole nations stay with one player.\n"
                      "Chart groupings are editable setup defaults, not historical war-entry dates.\n"
                      "UICFB PDF p3; v1.6a 2.D-F, printed pp8-9 / PDF pp10-11.\n"
                      "Online/PBEM choices save assignments only; transport and AI opponents are not implemented.")
        note.setWordWrap(True)
        layout.addWidget(note)
        form = QFormLayout()
        layout.addLayout(form)
        self.mode = QComboBox()
        for label, mode in (("Two players (default)", "two_player"), ("Pass and play", "pass_and_play"),
                            ("Online setup only", "online"), ("PBEM setup only", "pbem"), ("Against AI (setup only)", "ai")):
            self.mode.addItem(label, mode)
        self.mode.setCurrentIndex(MODES.index(self.setup["mode"]))
        form.addRow("Mode", self.mode)
        self.ai_side = QComboBox()
        self.ai_side.addItems(SIDES)
        self.ai_side.setCurrentText(self.setup["ai_side"])
        form.addRow("AI side", self.ai_side)
        self.counts = {}
        for side in SIDES:
            spin = QSpinBox()
            spin.setRange(1, max_team_size(self.nations, side))
            spin.setValue(len(self.setup["players"][side]))
            self.counts[side] = spin
            form.addRow(f"{side.title()} players", spin)
        self.players_table = QTableWidget(0, 2)
        self.players_table.setHorizontalHeaderLabels(["Player", "Name (editable)"])
        self.players_table.setMaximumHeight(150)
        layout.addWidget(self.players_table)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Nation / group", "Side", "Player", "Nationality aliases", "Placed counters"])
        for column, width in enumerate((210, 95, 180, 260, 115)):
            self.table.setColumnWidth(column, width)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        buttons = QHBoxLayout()
        layout.addLayout(buttons)
        for label, callback in (("Add Nation", self.add_nation), ("Remove Selected Nation", self.remove_nation),
                                ("Suggest Balanced Split", self.suggest)):
            button = QPushButton(label)
            button.clicked.connect(callback)
            buttons.addWidget(button)
        self.report = QLabel()
        self.report.setWordWrap(True)
        self.report.setTextFormat(Qt.TextFormat.PlainText)
        layout.addWidget(self.report)
        controls = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        controls.accepted.connect(self.save_setup)
        controls.rejected.connect(self.reject)
        layout.addWidget(controls)
        self.mode.currentIndexChanged.connect(self.rebuild)
        self.ai_side.currentIndexChanged.connect(self.rebuild)
        for spin in self.counts.values():
            spin.valueChanged.connect(self.rebuild)
        self.rebuild()

    def capture(self):
        for row in range(self.players_table.rowCount()):
            self.names[self.players_table.item(row, 0).data(Qt.ItemDataRole.UserRole)] = self.players_table.item(row, 1).text()
        for row, nation in enumerate(self.nations):
            nation["name"] = self.table.item(row, 0).text().strip()
            nation["allegiance"] = self.table.cellWidget(row, 1).currentData()
            nation["aliases"] = [s.strip() for s in self.table.item(row, 3).text().split(",") if s.strip()]
            owner = self.table.cellWidget(row, 2).currentData()
            self.setup["assignments"].pop(nation["nation_id"], None)
            if owner is not None:
                self.setup["assignments"][nation["nation_id"]] = owner

    def teams(self):
        previous = {p["player_id"]: p for team in self.setup["players"].values() for p in team}
        teams = {}
        used = {uid for ids in self.player_ids.values() for uid in ids}
        for side in SIDES:
            teams[side] = []
            for i in range(1, self.counts[side].value() + 1):
                if i > len(self.player_ids[side]):
                    uid = f"{side}-{i}"
                    if uid in used:
                        uid = f"{side}-{uuid4().hex}"
                    self.player_ids[side].append(uid)
                uid = self.player_ids[side][i - 1]
                used.add(uid)
                player = deepcopy(previous.get(uid, {}))
                player.update(player_id=uid, name=self.names.get(uid, f"{side.title()} player {i}"),
                              controller="ai" if self.mode.currentData() == "ai" and self.ai_side.currentText() == side else "human")
                teams[side].append(player)
        return teams

    def rebuild(self, *_):
        if self.table.rowCount():
            self.capture()
        for side, spin in self.counts.items():
            spin.blockSignals(True)
            spin.setMaximum(max_team_size(self.nations, side))
            restricted = self.mode.currentData() in ("two_player", "ai")
            if restricted:
                spin.setValue(1)
            spin.setEnabled(not restricted)
            spin.blockSignals(False)
        self.ai_side.setEnabled(self.mode.currentData() == "ai")
        teams = self.teams()
        self.players_table.setRowCount(0)
        for side in SIDES:
            for player in teams[side]:
                row = self.players_table.rowCount()
                self.players_table.insertRow(row)
                item = QTableWidgetItem(f"{player['player_id']} ({player['controller']})")
                item.setData(Qt.ItemDataRole.UserRole, player["player_id"])
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.players_table.setItem(row, 0, item)
                self.players_table.setItem(row, 1, QTableWidgetItem(player["name"]))
        self.table.setRowCount(0)
        for nation in self.nations:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(nation["name"]))
            side_choice = QComboBox()
            for side in (*SIDES, "neutral"):
                side_choice.addItem(side.title(), side)
            side_choice.setCurrentIndex((*SIDES, "neutral").index(nation["allegiance"]))
            self.table.setCellWidget(row, 1, side_choice)
            owner_choice = QComboBox()
            owner_choice.addItem("Unassigned", None)
            for player in teams.get(nation["allegiance"], []):
                owner_choice.addItem(player["name"], player["player_id"])
            owner = self.setup["assignments"].get(nation["nation_id"])
            index = owner_choice.findData(owner)
            if index < 0 and owner_choice.count() == 2:
                index = 1
            owner_choice.setCurrentIndex(max(0, index))
            self.table.setCellWidget(row, 2, owner_choice)
            owner_choice.currentIndexChanged.connect(self.refresh_counts)
            self.table.setItem(row, 3, QTableWidgetItem(", ".join(nation.get("aliases", []))))
            item = QTableWidgetItem("—")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 4, item)
            side_choice.currentIndexChanged.connect(self.rebuild)
        self.show_counts()

    def read_counts(self):
        validate_roster(self.nations)
        path = self.view.counter_project_dir / "assets" / "counters" / "unit_definitions.json"
        definitions = {}
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            if (not isinstance(data, dict) or data.get("format") != "tsww-barbarossa-unit-definitions"
                    or data.get("version") != 1 or not isinstance(data.get("definitions"), dict)):
                raise ValueError("Invalid unit definitions file.")
            definitions = data["definitions"]
        return count_placed_nations(self.view.units, definitions, self.nations)

    def show_counts(self):
        try:
            counts, unknown = self.read_counts()
            for row, nation in enumerate(self.nations):
                self.table.item(row, 4).setText(str(counts[nation["nation_id"]]))
            totals = {p["player_id"]: 0 for team in self.teams().values() for p in team}
            for row, nation in enumerate(self.nations):
                owner = self.table.cellWidget(row, 2).currentData()
                if owner in totals:
                    totals[owner] += counts[nation["nation_id"]]
            self.report.setText(f"{sum(counts.values())} placed counters matched; {len(unknown)} unknown/unreviewed.\n"
                                + "Known-counter totals: " + ", ".join(f"{pid}: {n}" for pid, n in totals.items())
                                + ". Balance is approximate; nations stay whole. Save the campaign to keep setup.")
            self.report.setToolTip("\n".join(f"{uid}: {reason}" for uid, reason in unknown.items()))
        except (OSError, ValueError) as error:
            self.report.setText(str(error))

    def refresh_counts(self, *_):
        self.capture()
        self.show_counts()

    def add_nation(self):
        self.capture()
        self.table.setRowCount(0)
        self.nations.append({"nation_id": uuid4().hex, "name": "New nation", "allegiance": "neutral", "aliases": []})
        self.rebuild()

    def remove_nation(self):
        row = self.table.currentRow()
        if row < 0:
            return
        self.capture()
        nation = self.nations.pop(row)
        self.setup["assignments"].pop(nation["nation_id"], None)
        self.table.setRowCount(0)
        self.rebuild()

    def suggest(self):
        try:
            self.capture()
            counts, unknown = self.read_counts()
            self.setup["assignments"] = balanced_assignments(self.nations, self.teams(), counts)
            self.table.setRowCount(0)
            self.rebuild()
            totals = {p["player_id"]: 0 for team in self.teams().values() for p in team}
            for nation_id, player_id in self.setup["assignments"].items():
                totals[player_id] += counts[nation_id]
            self.report.setText("Suggested known-counter totals: " + ", ".join(f"{pid}: {n}" for pid, n in totals.items())
                                + f". {len(unknown)} unknown/unreviewed excluded. Adjust assignments if needed.")
        except (OSError, ValueError) as error:
            QMessageBox.warning(self, "Cannot Balance Teams", str(error))

    def save_setup(self):
        try:
            self.capture()
            self.setup.update(mode=self.mode.currentData(), ai_side=self.ai_side.currentText(), players=self.teams())
            self.view.player_setup = validate_setup(self.setup)
        except ValueError as error:
            QMessageBox.warning(self, "Check Player Setup", str(error))
            return
        self.accept()
