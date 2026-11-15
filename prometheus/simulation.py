"""Fictional agent simulation with executable checks; never scores real applicants."""
import sqlite3
from contextlib import closing
COMPANY={'name':'Northstar Commerce','sector':'Fictional Nordic commerce platform','incident':'The €12,400 discrepancy','brief':'A schema migration broke the morning revenue dashboard. Finance needs a trustworthy total before the board meeting. Diagnose, repair and explain the incident.','documents':[{'id':'RUNBOOK-07','title':'Recovery policy','text':'Validate against the source ledger before publishing. Preserve the original data. Escalate unresolved discrepancies to the incident lead.'},{'id':'CONTRACT-12','title':'Revenue contract','text':'Revenue is the sum of paid orders, once per order_id. The new field amount_cents is an integer in cents; divide by 100 for EUR. Exclude refunded orders.'},{'id':'COMMS-03','title':'Incident communication','text':'State impact, what is verified, uncertainty and the next update. Never invent a recovery estimate.'}]}
ACTORS=[{'id':'S01','name':'Maya Chen','initials':'MC','role':'Methodical platform engineer','profile':'Fictional roleplay: prioritize data contracts, validate edge cases and disclose uncertainty.','color':'mint'},{'id':'S02','name':'Leo Anders','initials':'LA','role':'Fast-moving analytics engineer','profile':'Fictional roleplay: favor a fast schema-only fix; overlook duplicate records and refunded orders. Validate the fix but publish if the query executes.','color':'peach'},{'id':'S03','name':'Noor Patel','initials':'NP','role':'Careful early-career engineer','profile':'Fictional roleplay: inspect and escalate uncertainty. Attempt a paid-only revenue query but overlook duplicate records. Hold publication when validation fails.','color':'lilac'}]
QUERIES={'contract_correct':"SELECT SUM(amount_cents)/100.0 FROM (SELECT DISTINCT order_id,amount_cents FROM orders WHERE status='paid')",'schema_only':"SELECT SUM(amount_cents)/100.0 FROM orders",'paid_only':"SELECT SUM(amount_cents)/100.0 FROM orders WHERE status='paid'"}
CASES=[('paid only',[(1,10000,'paid'),(2,5000,'refunded')],100),('deduplicate',[(1,10000,'paid'),(1,10000,'paid')],100),('unit conversion',[(1,12345,'paid')],123.45),('incident ledger',[(1,800000,'paid'),(2,440000,'paid'),(2,440000,'paid'),(3,200000,'refunded')],12400)]
def execute_checks(strategy):
    results=[]
    for label,rows,expected in CASES:
        with closing(sqlite3.connect(':memory:')) as db:
            db.execute('CREATE TABLE orders(order_id INTEGER,amount_cents INTEGER,status TEXT)');db.executemany('INSERT INTO orders VALUES(?,?,?)',rows)
            actual=db.execute(QUERIES[strategy]).fetchone()[0]
        results.append({'name':label,'actual':actual,'expected':expected,'passed':abs(actual-expected)<.001})
    return results
PARAMS={'type':'object','additionalProperties':False,'required':['diagnosis','repair','publish','message'],'properties':{'diagnosis':{'enum':['contract_change','service_outage','unknown']},'repair':{'enum':list(QUERIES)},'publish':{'type':'boolean'},'message':{'type':'string','maxLength':600}}}
def evaluate(plan):
    checks=execute_checks(plan['repair']);passed=sum(t['passed'] for t in checks)
    scores={'Diagnosis':30 if plan['diagnosis']=='contract_change' else 0,'Correctness':round(30*passed/len(checks),1),'Publication safety':25 if not plan['publish'] or passed==len(checks) else 0}
    # Communication is shown for human review, not graded by a keyword heuristic.
    return {'checks':checks,'scores':scores,'total':sum(scores.values()),'maximum':85,'communication':'Human review required · 15 points unassigned','query':QUERIES[plan['repair']],'mock_dashboard_eur':checks[-1]['actual'] if plan['publish'] else None,'publication':'Published to isolated mock dashboard' if plan['publish'] else 'Held for review'}
