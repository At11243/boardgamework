"""Clean helper module for physical counter sheet coordinate mapping and features."""
import os
import json
import re
from pathlib import Path
from functools import lru_cache
import numpy as np

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QImageReader
from PySide6.QtCore import Qt

QImageReader.setAllocationLimit(1024)
app = QApplication.instance() or QApplication([])

root = Path.cwd()
base = root / 'tmp/physical_next1000'
source = root / 'tmp/physical_third1000'

g199 = json.loads((root / 'audit_tools/source_calibration/grid.json').read_text()) if (root / 'audit_tools/source_calibration/grid.json').is_file() else {}
g120 = json.loads((root / 'audit_tools/source_calibration/120-grid.json').read_text()) if (root / 'audit_tools/source_calibration/120-grid.json').is_file() else {}
g185 = json.loads((root / 'audit_tools/source_calibration/185-grid.json').read_text()) if (root / 'audit_tools/source_calibration/185-grid.json').is_file() else {}


@lru_cache(maxsize=32)
def photo(n: int, p: int) -> QImage:
    """Load photo for document n, page p."""
    if n in [199, 185, 120]:
        for folder in [base, root / 'tmp/physical_1000']:
            f = folder / f'{n}-p{p}.jpeg'
            if f.exists():
                return QImage(str(f))
    f_png = source / f'{n}-p{p}.png'
    if f_png.exists():
        return QImage(str(f_png))
    import fitz
    pdf = Path.home() / 'Downloads' / f'KIC Document {n}.pdf'
    if not pdf.exists(): return QImage()
    with fitz.open(pdf) as doc:
        page = doc[p-1]
        images = page.get_images(full=True)
        if not images: return QImage()
        item = max(images, key=lambda x: x[2]*x[3])
        return QImage.fromData(doc.extract_image(item[0])['image'])


def original_geom(n: int, p: int, r: int, c: int):
    """Fallback geometric coordinate mapping for sheets without precomputed grid."""
    if n == 120 and p <= 4:
        gg = g120.get(str(p), {})
        if gg:
            return gg['xs'][c - 1] * 2.88, gg['ys'][r - 1] * 2.88, 132
    if n == 132 or n == 120:
        xs = np.linspace(430, 854, 10) if c <= 10 else np.linspace(936, 1352, 10)
        ys = np.array([232, 282, 345, 395, 456, 508, 566, 617, 679, 732, 791, 844, 905, 958], float)
        yy = ys[r - 1] + (c - 1 if c <= 10 else 20 - c) * 2.4
        return xs[(c - 1) % 10] * 2.88, yy * 2.88, 137
    if n == 108:
        xs = np.linspace(153, 839, 10) if c <= 10 else np.linspace(975, 1648, 10)
        ys = np.array([49, 137, 244, 329, 424, 509, 598, 684, 778, 864, 969, 1058, 1162, 1253], float)
        yy = ys[r - 1] + ((c - 1) / 9 * 30 if c <= 10 else -(c - 11) / 9 * 32) * (1 - (r - 1) / 15)
        return xs[(c - 1) % 10] * 3172 / 1800, yy * 2395 / 1359, 135
    return 0.0, 0.0, 145.0


@lru_cache(maxsize=20000)
def geom_before_naval_gap(n: int, p: int, r: int, c: int):
    if n == 199 and str(p) in g199:
        gg = g199[str(p)]
        ys = gg['rows'][r - 1]
        yy = ys[1]
        xx = float(np.polyval(gg['columns'][c - 1], yy - 1700)) + 65
        yy = float(np.polyval(ys, xx - 2500))
        return xx, yy, 145
    if (n == 120 and p <= 4) or n == 185:
        grids = g120 if n == 120 else g185
        if str(p) not in grids:
            return original_geom(132, p, r, c)
        gg = grids[str(p)]
        return gg['xs'][c - 1] * 2.88, gg['ys'][r - 1] * 2.88, 145
    return original_geom(n, p, r, c)


@lru_cache(maxsize=20000)
def geom(n: int, p: int, r: int, c: int):
    """Accurate physical cell center and dimensions."""
    if n == 199 and p in [11, 12] and r >= 9:
        if r <= 13:
            return geom_before_naval_gap(n, p, r + 1, c)
        x1, y1, size = geom_before_naval_gap(n, p, 13, c)
        x2, y2, size = geom_before_naval_gap(n, p, 14, c)
        return 2 * x2 - x1, 2 * y2 - y1, size
    return geom_before_naval_gap(n, p, r, c)


def arr(im: QImage, dim: int = 36) -> np.ndarray:
    """Normalized interior feature vector of counter image."""
    edge = max(1, round(im.width() * 0.04))
    im = im.copy(edge, edge, im.width() - 2 * edge, im.height() - 2 * edge)
    im = im.scaled(dim, dim, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation).convertToFormat(QImage.Format.Format_RGB888)
    rgb = np.frombuffer(im.bits(), np.uint8).reshape(dim, im.bytesPerLine())[:, :dim * 3].reshape(dim, dim, 3).astype(np.float32)
    bg = np.median(rgb, axis=(0, 1))
    a = rgb.mean(axis=2)
    median = np.median(a)
    light = (bg[1] > bg[0] * 1.15 or bg[2] > bg[0] * 1.15)
    a = np.maximum(a - median, 0) if light else np.maximum(median - a, 0)
    a = a / (np.linalg.norm(a) + 1e-6)
    return a.reshape(-1)


def literal(v: dict) -> str:
    """Extract clean designation string for literal OCR matching."""
    name = v.get('designation', '')
    prefix = v.get('unit_type', '') + ' ' + v.get('unit_size', '') + ' '
    if name.lower().startswith(prefix.lower()):
        name = name[len(prefix):]
    return re.sub(r'[^a-z0-9/]', '', name.lower())


