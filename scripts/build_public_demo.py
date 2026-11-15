from pathlib import Path
import sys,json,shutil,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from commonground_app.fixtures import COMPANIES,PEOPLE
from commonground_app.engine import simulate
out=ROOT/'public-demo/dist';out.mkdir(parents=True,exist_ok=True)
results={c['scenario']:{s:simulate(c,PEOPLE[0],s if s!='discussion_only' else None) for s in (['contract_correct','paid_only','schema_only'] if c['scenario']=='revenue' else ['discussion_only'])} for c in COMPANIES}
data={'twins':COMPANIES+PEOPLE,'results':results}
js=(ROOT/'commonground_app/static/app.js').read_text();a=js.index('async function api(');b=js.index('\nfunction post(',a);js=js[:a]+'async function api(path,options={}){return browserAPI(path,options);}\n'+js[b:]
js=js.replace('Add a live AI conversation','Live AI is available in the downloadable app').replace('Local scenario checks','Browser scenario preview').replace('Local checks + live AI conversation','Scenario preview')
(out/'app.js').write_text('const DEMO='+json.dumps(data)+';\n'+(ROOT/'scripts/browser-api.js').read_text()+'\n'+js)
html=(ROOT/'commonground_app/static/index.html').read_text().replace('/static/style.css','style.css').replace('/static/app.js','app.js').replace('Fictional demo workspace','Browser demo · reload to reset').replace('People choose the connection. CommonGround helps prepare the conversation.','Browser preview: fictional data, session-only changes, precomputed SQL outputs. No model calls. <a href="index.html">Video, deck and source ↗</a>')
(out/'demo.html').write_text(html);shutil.copy(ROOT/'commonground_app/static/style.css',out/'style.css')
for name in ['CommonGround_Demo.mp4','CommonGround_Espoo_Pitch.pdf','CommonGround_Espoo_Pitch.pptx','CommonGround_Source.zip']:
 p=ROOT/'submission'/name
 if p.exists():shutil.copy(p,out/name)
