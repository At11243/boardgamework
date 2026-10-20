"""Importer regression checks use a temporary synthetic module only."""
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from counters.import_counters import extract_counters, referenced_image_names


class CounterImportTests(unittest.TestCase):
    def test_exact_comma_filename_and_duplicate_references(self):
        images = {'plane, variant.png': 'a', 'front.png': 'b', 'back.png': 'c'}
        self.assertEqual(referenced_image_names(
            'piece;;;plane, variant.png;front.png,back.png;front.png;missing.png', images),
            ['plane, variant.png', 'front.png', 'back.png'])

    def test_comma_faces_single_image_and_unresolved_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            module = root / 'test.vmdx'
            with ZipFile(module, 'w') as archive:
                archive.writestr('buildFile.xml', '''<root>
                    <VASSAL.build.widget.PieceSlot gpid="one" entryName="Paired">emb2;;front.png,back.png;piece;;;;</VASSAL.build.widget.PieceSlot>
                    <VASSAL.build.widget.PieceSlot gpid="two" entryName="Single">piece;;;single.png;</VASSAL.build.widget.PieceSlot>
                    <VASSAL.build.widget.PieceSlot gpid="three" entryName="Missing">piece;;;missing.png;</VASSAL.build.widget.PieceSlot>
                    </root>''')
                for name in ('front.png', 'back.png', 'single.png'):
                    archive.writestr('images/' + name, b'test artwork bytes')
            path, catalog = extract_counters(module, root)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), catalog)
            self.assertEqual(catalog['counter_types']['vassal:one']['image_names'],
                             ['front.png', 'back.png'])
            self.assertEqual(catalog['counter_types']['vassal:two']['image_names'], ['single.png'])
            self.assertEqual(catalog['unresolved_image_references'], ['vassal:three'])
            for record in catalog['counter_types'].values():
                for image in record['image_paths']:
                    self.assertEqual((root / image).read_bytes(), b'test artwork bytes')
