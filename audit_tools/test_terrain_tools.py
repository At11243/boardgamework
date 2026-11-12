import json, tempfile, unittest
from pathlib import Path
import numpy as np
from audit_tools.terrain_baseline import fit, predict
from audit_tools.terrain_labeler import save_labels

class TerrainToolsTests(unittest.TestCase):
    def test_separable_centroids_and_finite_scores(self):
        x=np.array([[0,0],[.1,0],[5,5],[5.1,5],[10,0],[10.1,0]])
        model=fit(x,['Clear','Clear','Steppe','Steppe','Swamp','Swamp'])
        scores,_=predict(x,model)
        np.testing.assert_array_equal(scores.argmax(axis=1),[0,0,1,1,2,2])
        np.testing.assert_allclose(scores.sum(axis=1),1)
        self.assertTrue(np.isfinite(scores).all())

    def test_atomic_labels_backup_preserves_unknown_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'labels.json'; original={'T1':{'label':'Clear','extra':17}}
            save_labels(p,original); updated={**original,'T2':{'label':'Steppe'}}; save_labels(p,updated)
            self.assertEqual(json.loads(p.read_text()),updated)
            self.assertEqual(json.loads(p.with_suffix('.json.bak').read_text()),original)
            self.assertFalse(p.with_suffix('.json.tmp').exists())

    def test_evaluation_board_not_in_seed_labels(self):
        p=Path('audits/20261109/terrain/seed_labels_pending_swamp.json')
        self.assertTrue(all(z['key'][0]!='Map 9' for z in json.loads(p.read_text())))

if __name__=='__main__': unittest.main()
