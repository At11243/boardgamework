import copy,json,tempfile,unittest
from pathlib import Path
from audit_tools.counter_full_audit import reconcile,RUN
from counters.unit_storage import write_definitions

class CounterAuditTests(unittest.TestCase):
    def fixture(self):
        return {'future_top':{'keep':True},'definitions':{
            'vassal:133:236608':{'nationality':'German','ratings':{'zero':'0','unknown':None,'na':'N/A'}},
            'A':{'review_status':'Verified','front_image':'a.png','back_image':'b.png','unknown':{'x':[1,2]},'ground':{'format':'legacy','movement':'0'},'physical_back_review':{'result':'Blank confirmed','confidence':.98},'batch_review':{'review':{'identity':{'checked':True,'confidence':.98,'extra':'keep'},'front':{'checked':True},'back':{'checked':True}},'issues':[]}},
            'B':{'review_status':'In progress','front_image':'c.png','notes':'Manual notes','back_appearance':'Blank color'}}}

    def test_provenance_withdrawal_preserves_art_ratings_unknown_fields_and_history(self):
        original=self.fixture();unchanged=copy.deepcopy(original)
        result,changes=reconcile(original,[{'type_id':'A','kind':'confirmed_locator_mismatch','detail':'Wrong cell','source_reference':'PDF p1 r1 c1'}],[])
        self.assertEqual(original,unchanged);self.assertEqual(result['future_top'],original['future_top'])
        a=result['definitions']['A'];self.assertEqual(a['review_status'],'In progress')
        for field in ['front_image','back_image','unknown','ground']:self.assertEqual(a[field],original['definitions']['A'][field])
        self.assertEqual(a['physical_back_review']['confidence'],0)
        self.assertEqual(a['counter_audit_history'][0]['physical_back_review'],original['definitions']['A']['physical_back_review'])
        self.assertEqual(a['batch_review']['review']['identity']['extra'],'keep')
        self.assertFalse(a['batch_review']['review']['back']['checked'])
        self.assertEqual(result['definitions']['vassal:133:236608']['nationality'],'Germany')
        self.assertEqual(result['definitions']['vassal:133:236608']['ratings'],original['definitions']['vassal:133:236608']['ratings'])
        again,new_changes=reconcile(result,[{'type_id':'A','kind':'confirmed_locator_mismatch','detail':'Wrong cell','source_reference':'PDF p1 r1 c1'}],[])
        self.assertEqual(result,again);self.assertEqual(new_changes,[])

    def test_collision_does_not_merge_ids_or_invent_reverse_and_atomic_backup(self):
        original=self.fixture();collision={'type_ids':['A','B'],'location':['hash',1,2,3]}
        result,_=reconcile(original,[],[collision]);self.assertEqual(set(result['definitions']),set(original['definitions']))
        self.assertEqual(result['definitions']['B']['back_appearance'],'Blank color')
        self.assertNotIn('back_image',result['definitions']['B']);self.assertIn('Manual notes',result['definitions']['B']['notes'])
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'definitions.json';path.write_text(json.dumps(original));before=path.read_bytes()
            write_definitions(path,result);self.assertEqual(json.loads(path.read_text()),result)
            backups=list((path.parent/'unit_definition_backups').glob('*.json'))
            self.assertEqual(len(backups),1);self.assertEqual(backups[0].read_bytes(),before)

if __name__=='__main__':unittest.main()
