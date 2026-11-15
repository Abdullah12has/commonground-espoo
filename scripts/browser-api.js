// Browser-only demonstration. No server, model calls, or shared participant data.
const demoStore={twins:structuredClone(DEMO.twins),runs:[],introductions:[],live_available:false,demo:true};
const demoClone=x=>structuredClone(x);
function browserFresh(r){return ['company','person'].every(k=>demoStore.twins.some(t=>t.id===r[k].id&&t.version===r[k].version&&t.approved));}
async function browserAPI(path,options={}){
 const b=JSON.parse(options.body||'{}'),parts=path.split('/').filter(Boolean),find=(table,id)=>{const r=demoStore[table].find(x=>x.id===id);if(!r)throw Error('Item not found');return r;};
 if(path==='/state'){demoStore.runs.forEach(r=>r.stale=!browserFresh(r));demoStore.introductions.forEach(i=>i.stale=!browserFresh(find('runs',i.run_id)));return demoClone(demoStore);}
 if(parts[0]==='twins'){
  const t=find('twins',parts[1]);if(t.version!==b.version)throw Error('Twin changed. Reload and review.');
  if(parts[2]==='approve')t.approved=true;
  else {if(b.summary.length<10||b.evidence_text.length<10)throw Error('Add a description and evidence.');Object.assign(t,{summary:b.summary,skills:b.skills.map(x=>x.trim().toLowerCase()),preferences:b.preferences,version:t.version+1,approved:false});t.evidence[0].text=b.evidence_text;if(t.kind==='person')t.evidence[0].skills=b.evidence_skills.map(x=>x.trim().toLowerCase());}
  return demoClone(t);
 }
 if(path==='/runs'){
  const c=find('twins',b.company_id),p=find('twins',b.person_id);if(!c.approved||!p.approved||c.version!==b.company_version||p.version!==b.person_version)throw Error('Review the current twins first.');
  const strategy=b.strategy||p.strategy,result=demoClone(DEMO.results[c.scenario][c.scenario==='revenue'?strategy:'discussion_only']);
  const evidence=new Set(p.evidence.flatMap(e=>e.skills||[]).filter(s=>p.skills.includes(s)));
  result.supported=c.skills.filter(s=>evidence.has(s));result.unknown=c.skills.filter(s=>!evidence.has(s));result.coverage=c.skills.length?Math.round(100*result.supported.length/c.skills.length):0;result.shared_preferences=p.preferences.filter(s=>c.preferences.includes(s));result.headline=result.supported.length?'Shared ground to explore':'More evidence needed';
  result.events[0].body=c.summary;result.events[0].source=c.evidence[0].id;result.events[1].body=p.evidence[0].text;result.events[1].source=p.evidence[0].id;
  result.questions=[...result.unknown.map(s=>'Could you walk through a concrete example of '+s+'?'),...result.friction,'What would make this opportunity worthwhile for both of you?'];
  result.limitation+=' Public browser demo uses precomputed benchmark outputs; the downloadable Python app executes the SQL checks.';
  const r={id:crypto.randomUUID().replaceAll('-','').slice(0,16),created_at:new Date().toISOString(),company:demoClone(c),person:demoClone(p),result};demoStore.runs.unshift(r);return demoClone(r);
 }
 if(parts[0]==='runs'){
  const r=find('runs',parts[1]);if(parts[2]!=='introduction')return demoClone(r);
  if(!browserFresh(r))throw Error('Run the current twins again.');
  let i=demoStore.introductions.find(i=>i.id===r.id);if(!i){i={id:r.id,run_id:r.id,company:r.company.name,person:r.person.name,company_consent:false,person_consent:false,created_at:new Date().toISOString(),feedback:null,agenda:r.result.questions};demoStore.introductions.unshift(i);}return demoClone(i);
 }
 if(parts[0]==='introductions'){
  const i=find('introductions',parts[1]),r=find('runs',i.run_id);if(!browserFresh(r))throw Error('This introduction is stale.');
  if(parts[2]==='consent'){if(r.company.version!==b.company_version||r.person.version!==b.person_version)throw Error('Twin versions changed.');i[b.party+'_consent']=b.consent;}
  else {if(!i.company_consent||!i.person_consent)throw Error('Both sides must opt in.');i.feedback={...b,at:new Date().toISOString()};}return demoClone(i);
 }
 throw Error('Unsupported demo action');
}
