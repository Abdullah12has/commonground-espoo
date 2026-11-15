"""Inspectable fit hypotheses. Scores measure toy task execution, never a person."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'prometheus'))
from simulation import execute_checks

def simulate(company, person, strategy=None):
    supported=set(s for e in person['evidence'] for s in e.get('skills',[])) & set(person['skills'])
    required=company['skills']; overlap=[s for s in required if s in supported]; unknown=[s for s in required if s not in supported]
    shared=[p for p in person['preferences'] if p in company['preferences']]
    chosen=strategy or person.get('strategy','paid_only')
    events=[{'kind':'context','title':'Company twin sets the scene','body':company['summary'],'source':company['evidence'][0]['id']},
            {'kind':'evidence','title':'Participant evidence enters the scenario','body':person['evidence'][0]['text'],'source':person['evidence'][0]['id']}]
    if company['scenario']=='revenue':
        checks=execute_checks(chosen)
        events += [{'kind':'action','title':'Assumed repair strategy','body':{'contract_correct':'Validate the contract, filter refunds and deduplicate orders.','paid_only':'Filter paid orders; duplicate handling remains incomplete.','schema_only':'Repair the renamed field without checking refunds or duplicates.'}[chosen],'source':'Scenario assumption · editable'}]
        events += [{'kind':'pass' if c['passed'] else 'question','title':c['name'],'body':f"Expected €{c['expected']:,.2f}; simulated query returned €{c['actual']:,.2f}.",'source':'Fixed benchmark CG-SQL-1'} for c in checks]
        friction=['The assumed repair fails '+str(sum(not x['passed'] for x in checks))+' scenario checks. Discuss how to validate the result.'] if not all(x['passed'] for x in checks) else ['The toy repair passes all checks; how does this transfer to an unfamiliar system?']
    else:
        checks=[]
        events += [{'kind':'action','title':'Service disruption conversation','body':'Discuss what is confirmed, what is unknown, and when the next customer update should happen.','source':'HS-1 / HS-2'}, {'kind':'question','title':'Human response required','body':'A supplied work example can start this conversation. No automated communication or personality grade is assigned.','source':'Human discussion'}]
        friction=['How would you set a useful next update without promising a recovery time?']
    questions=[f'Could you walk through a concrete example of {s}?' for s in unknown]
    questions += friction + ['What would make this opportunity worthwhile for both of you?']
    coverage=round(100*len(overlap)/len(required)) if required else 0
    return {'headline':'Shared ground to explore' if overlap else 'More evidence needed','coverage':coverage,'supported':overlap,'unknown':unknown,'shared_preferences':shared,'friction':friction,'questions':questions,'checks':checks,'events':events,'assumption':chosen if company['scenario']=='revenue' else 'discussion_only','explanation':'Coverage counts requested skill areas with a supplied evidence reference. It is not a fit probability or a hiring score.','limitation':'A twin simulates supplied assumptions, not a real person. Task checks validate a toy query. Mutual suitability remains a human judgement.','dialogue':[],'mode':'local','model_status':'Not requested','benchmark':{'id':'CG-SQL-1','text':'Fixed demonstration contract: paid orders once per order_id, cents to EUR, excluding refunds. Editing company text does not change these test fixtures.'} if company['scenario']=='revenue' else None}
