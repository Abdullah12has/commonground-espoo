import copy, os, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
TMP=tempfile.TemporaryDirectory()
os.environ['COMMONGROUND_DB']=str(Path(TMP.name)/'test.sqlite')
from commonground_app import app as m
from commonground_app.engine import simulate
from commonground_app.fixtures import COMPANIES, PEOPLE
from fastapi.testclient import TestClient

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        with m.db() as c:
            for table in ['introductions','runs','twins']:c.execute('DELETE FROM '+table)
        m.init();self.client=TestClient(m.app)
    def run_pair(self,**extra):
        return self.client.post('/api/runs',json={'company_id':'northstar','person_id':'alex','company_version':1,'person_version':1,**extra})
    def test_task_checks_are_not_coverage_or_fit(self):
        good=simulate(COMPANIES[0],PEOPLE[0],'contract_correct');bad=simulate(COMPANIES[0],PEOPLE[0],'schema_only')
        self.assertTrue(all(c['passed'] for c in good['checks']));self.assertFalse(all(c['passed'] for c in bad['checks']))
        self.assertEqual(good['coverage'],bad['coverage']);self.assertNotIn('fit_score',good)
        p=copy.deepcopy(PEOPLE[0]);p['evidence'][0]['skills']=[]
        result=simulate(COMPANIES[0],p);self.assertEqual(result['coverage'],0);self.assertEqual(result['unknown'],COMPANIES[0]['skills'])
    def test_second_company_has_its_own_scenario(self):
        r=simulate(COMPANIES[1],PEOPLE[1]);self.assertEqual(r['checks'],[]);self.assertEqual(r['assumption'],'discussion_only')
        self.assertIn('HS-1 / HS-2',[e['source'] for e in r['events']])
    def test_mutual_consent_and_withdrawal(self):
        run=self.run_pair().json();id=run['id'];self.client.post(f'/api/runs/{id}/introduction')
        fb={'useful':True,'notes':'Useful fictional meeting'}
        self.assertEqual(self.client.post(f'/api/introductions/{id}/feedback',json=fb).status_code,409)
        for party in ['person','company']:
            r=self.client.post(f'/api/introductions/{id}/consent',json={'party':party,'consent':True,'company_version':1,'person_version':1});self.assertEqual(r.status_code,200)
        self.assertEqual(self.client.post(f'/api/introductions/{id}/feedback',json=fb).status_code,200)
        self.client.post(f'/api/introductions/{id}/consent',json={'party':'person','consent':False,'company_version':1,'person_version':1})
        self.assertEqual(self.client.post(f'/api/introductions/{id}/feedback',json=fb).status_code,409)
    def test_edit_revokes_approval_and_stales_runs(self):
        r=self.run_pair().json();id=r['id'];self.client.post(f'/api/runs/{id}/introduction')
        p=PEOPLE[0];edit={'version':1,'summary':'A revised synthetic description.','skills':p['skills'],'preferences':p['preferences'],'evidence_text':p['evidence'][0]['text'],'evidence_skills':p['skills']}
        changed=self.client.put('/api/twins/alex',json=edit).json();self.assertFalse(changed['approved']);self.assertEqual(changed['version'],2)
        self.assertEqual(self.run_pair(person_version=2).status_code,409)
        self.assertEqual(self.client.post('/api/twins/alex/approve',json={'version':1}).status_code,409)
        self.assertEqual(self.client.post('/api/twins/alex/approve',json={'version':2}).status_code,200)
        self.assertEqual(self.run_pair().status_code,409)
        self.assertEqual(self.client.post(f'/api/runs/{id}/introduction').status_code,409)
        self.assertTrue(self.client.get(f'/api/runs/{id}').json()['stale'])
        self.assertEqual(self.client.post(f'/api/introductions/{id}/consent',json={'party':'person','consent':True,'company_version':1,'person_version':1}).status_code,409)
        self.assertEqual(self.run_pair(person_version=2).status_code,200)
    def test_failed_live_call_is_labelled_and_no_dialogue_fabricated(self):
        with patch.object(m,'live_dialogue',side_effect=ValueError('unavailable')):r=self.run_pair(mode='live').json()
        self.assertEqual(r['result']['mode'],'live_failed');self.assertEqual(r['result']['dialogue'],[])
    def test_invalid_inputs_and_idempotent_introduction(self):
        self.assertEqual(self.run_pair(strategy='DROP TABLE twins').status_code,422)
        self.assertEqual(self.run_pair(person_id='northstar').status_code,422)
        self.assertEqual(self.client.get('/api/runs/absent').status_code,404)
        id=self.run_pair().json()['id']
        a=self.client.post(f'/api/runs/{id}/introduction').json();b=self.client.post(f'/api/runs/{id}/introduction').json()
        self.assertEqual(a,b);self.assertEqual(len(self.client.get('/api/state').json()['introductions']),1)
    def test_run_snapshot_and_persistence(self):
        r=self.run_pair().json();m.init();other=TestClient(m.app)
        loaded=other.get('/api/runs/'+r['id']).json();self.assertEqual(loaded['company'],r['company']);self.assertEqual(loaded['result'],r['result'])
    def test_name_and_location_do_not_change_evidence(self):
        p=copy.deepcopy(PEOPLE[0]);baseline=simulate(COMPANIES[0],p)
        p['name']='Different name';p['location']='Different location'
        self.assertEqual(simulate(COMPANIES[0],p),baseline)

if __name__=='__main__':unittest.main()
