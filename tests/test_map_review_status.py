"""Map review status persistence and actual overlay colors, using synthetic data."""
import json
import os
from pathlib import Path
import tempfile
import unittest

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QImage, QPainter
from PySide6.QtWidgets import QApplication
from maps.campaign_grid_definitions import barbarossa_grids
from maps.hex_model import hex_center
from maps.map_view import MapView
from maps.terrain_editor import TerrainEditor


class MapReviewStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_draft_and_legacy_statuses_survive_editor_and_temp_save(self):
        key = ('Map 2', 'HP-ZF', 27, 63)
        view = MapView()
        editor = TerrainEditor()
        try:
            for status in ('In progress', 'Suggested', 'Verified', 'Unknown'):
                props = {'review_status': status, 'terrain': ['Glacier'],
                         'future_field': {'keep': True}}
                data = {'format': 'tsww-barbarossa-map-terrain', 'version': 1,
                        'hexes': [{'key': list(key), 'properties': props}]}
                with tempfile.TemporaryDirectory() as folder:
                    path = Path(folder) / 'terrain.json'
                    path.write_text(json.dumps(data), encoding='utf-8')
                    before = path.read_bytes()
                    view.load_map_definitions(path)
                    self.assertEqual(path.read_bytes(), before)
                    editor.show_hex('HP-ZF:2628', view.map_definitions[key])
                    self.assertEqual(editor.review_status.currentText(), status)
                    view.terrain_brush_path = path
                    view.write_terrain_records(view.map_definitions)
                    saved = json.loads(path.read_text())['hexes'][0]['properties']
                    self.assertEqual(saved, props)
        finally:
            editor.close()
            view.close()

    def test_terrain_and_transport_drafts_render_amber_verified_green(self):
        view = MapView()
        key = ('Map 2', 'HP-ZF', 27, 63)
        region = next(r for r in barbarossa_grids['Map 2']['regions'] if r['name']=='HP-ZF')
        x, y = hex_center(region['grid'], key[2], key[3])
        view.board_records = {'Map 2': {'origin': (0, 0)}}
        try:
            for transport in (False, True):
                for status in ('In progress', 'Suggested', 'Verified'):
                    if transport and status == 'Suggested':
                        continue
                    view.review_overlay_enabled = not transport
                    view.transport_review_overlay_enabled = transport
                    view.map_definitions = {key: {'review_status': status,
                                                 'transport_review_status': status}}
                    canvas = QImage(300, 300, QImage.Format.Format_RGB32)
                    canvas.fill(QColor('white'))
                    painter = QPainter(canvas)
                    painter.translate(150-x, 150-y)
                    view.drawForeground(painter, QRectF(x-150, y-150, 300, 300))
                    painter.end()
                    color = canvas.pixelColor(150, 150)
                    if status == 'Verified':
                        self.assertGreater(color.green(), color.red())
                        self.assertGreater(color.green(), color.blue())
                    else:
                        self.assertGreater(color.red(), color.green())
                        self.assertGreater(color.green(), color.blue())
        finally:
            view.close()
