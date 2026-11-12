"""Standalone human labeling; writes only isolated audit labels, never live maps."""
import json, os, time
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

ROOT = Path('audits/20261109/terrain')

def save_labels(path, data):
    path = Path(path)
    if path.exists():
        path.with_suffix('.json.bak').write_bytes(path.read_bytes())
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data, indent=2), encoding='utf-8')
    os.replace(temporary, path)

class Labeler(QWidget):
    def __init__(self):
        super().__init__()
        self.queue = json.loads((ROOT/'review_queue.json').read_text())
        self.path = ROOT/'human_labels.json'
        self.answers = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.index = 0
        self.setWindowTitle('Terrain review — isolated labels')
        layout = QVBoxLayout(self)
        self.title = QLabel(); layout.addWidget(self.title)
        self.picture = QLabel(); layout.addWidget(self.picture)
        self.status = QLabel(); layout.addWidget(self.status)
        row = QHBoxLayout(); layout.addLayout(row)
        for label in ['Clear', 'Steppe', 'Swamp', 'Other', 'Mixed', 'Unsure']:
            button = QPushButton(label); button.clicked.connect(lambda checked=False, x=label: self.record(x)); row.addWidget(button)
        nav = QHBoxLayout(); layout.addLayout(nav)
        for text, delta in [('Previous', -1), ('Skip / Next', 1)]:
            button = QPushButton(text); button.clicked.connect(lambda checked=False, d=delta: self.move(d)); nav.addWidget(button)
        self.show_crop()

    def show_crop(self):
        z = self.queue[self.index]
        self.title.setText(f"{self.index+1}/{len(self.queue)} | {z['key']} | {z['hex_id']} | {z['split']}")
        pix = QPixmap(z['crop'])
        self.picture.setPixmap(pix.scaled(pix.width()*4, pix.height()*4, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation))
        old = self.answers.get(z['queue_id'], {}).get('label', 'unanswered')
        self.status.setText(f'Current answer: {old}. Primary texture only; choose Mixed when a single class is misleading.')
        self.started = time.perf_counter()

    def record(self, label):
        z = self.queue[self.index]; old = self.answers.get(z['queue_id'], {})
        self.answers[z['queue_id']] = {**old, 'key': z['key'], 'label': label,
            'status': 'confirmed' if label in ['Clear', 'Steppe', 'Swamp'] else 'needs_review',
            'seconds': round(time.perf_counter()-self.started, 3), 'mode': 'manual', 'split': z['split']}
        save_labels(self.path, self.answers); self.move(1)

    def move(self, delta):
        self.index = max(0, min(len(self.queue)-1, self.index+delta)); self.show_crop()

if __name__ == '__main__':
    app = QApplication([]); window = Labeler(); window.show(); app.exec()
