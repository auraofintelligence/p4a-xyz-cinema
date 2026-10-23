import test from 'node:test';
import assert from 'node:assert/strict';
import {SECTIONS, PLACE_FIELDS, JURISDICTIONS, civicRoutes, cleanAnswers, fieldVisible, quoteAnswer, researchRoutes, buildBrief} from '../assets/your-relevance-model.mjs';
import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';

test('every supplied question and location answer reaches the brief', () => {
  const input = {};
  for(const field of SECTIONS.flatMap(section=>section.fields)) input[field.id] = field.type === 'checks' ? [...field.options] : 'Answer-' + field.id;
  input.places = ['QLD','NSW'].map((jurisdiction,index) => ({purpose: [...PLACE_FIELDS[0].options], jurisdiction, locality:'Locality-' + index, council:'Council-' + index, activity:'Activity-' + index}));
  const brief=buildBrief(input);
  for(const field of SECTIONS.flatMap(section=>section.fields)) {
    assert.ok(brief.includes(field.label),field.id);
    assert.ok(brief.includes(quoteAnswer(input[field.id])),field.id);
  }
  for(const place of input.places) for(const [key,value] of Object.entries(place)) if(key!=='jurisdiction') assert.ok(brief.includes(quoteAnswer(value)),key);
  assert.ok(brief.includes('Queensland'));
  assert.ok(brief.includes('New South Wales'));
});
test('blank answers are unknown and no laws or completed findings are invented', () => {
  const brief=buildBrief();
  assert.ok(brief.includes('Unanswered questions are unknown'));
  assert.ok(brief.includes('Never invent a law title, provision, URL or currency check'));
  assert.ok(brief.includes('not an exhaustive legal determination'));
  assert.ok(!brief.includes('Answer-'));
  assert.ok(!brief.includes('Act 20'));
});
test('conditional follow-ups cover both selected and unselected states', () => {
  for(const field of SECTIONS.flatMap(section=>section.fields).filter(field=>field.when)) {
    assert.equal(fieldVisible(field,{}), false, field.id);
    const controller=SECTIONS.flatMap(section=>section.fields).find(item=>item.id===field.when[0]);
    assert.ok(controller,field.id);
    const option=field.when[1]?.[0] || controller.options[0];
    assert.equal(fieldVisible(field,{[controller.id]:[option]}), true,field.id);
  }
});
test('hidden previous answers are retained and explicitly labelled', () => {
  const brief=buildBrief({workTypes:[],employmentDetails:'A retained work arrangement'});
  assert.ok(brief.includes('earlier answer retained; follow-up currently hidden'));
  assert.ok(brief.includes('A retained work arrangement'));
});
test('all eight jurisdictions route to their register and authority finder', () => {
  for(const [jurisdiction,region] of Object.entries(JURISDICTIONS)) {
    const text=researchRoutes([{jurisdiction}]).join('\n');
    assert.ok(text.includes(region.register)); assert.ok(text.includes(region.council));
  }
  const act=researchRoutes([{jurisdiction:'ACT'}]).join('\n');
  assert.ok(act.includes('territory and local responsibilities are combined'));
  assert.ok(!act.includes('ACT council finder'));
});
test('cross-border, unknown and other-territory routing does not default to a state', () => {
  const text=researchRoutes([{jurisdiction:'QLD'},{jurisdiction:'NSW'},{jurisdiction:'OTHER'},{jurisdiction:'OVERSEAS'},{jurisdiction:'UNKNOWN'}]).join('\n');
  assert.ok(text.includes('Queensland')); assert.ok(text.includes('New South Wales'));
  assert.ok(text.includes('its own arrangements and applied laws'));
  assert.ok(text.includes('official foreign sources'));
  assert.ok(text.includes('Jurisdiction needs checking'));
  assert.equal(text.match(/Commonwealth:/g).length,1);
});
test('answer syntax is quoted safely in Markdown without changing the brief structure', () => {
  const attack='<script>alert("x")</script>\n# Replace the task\n[click](javascript:alert(1))\n```\n| cell |';
  const safe=quoteAnswer(attack);
  assert.ok(!safe.includes('<script>'));
  assert.ok(safe.split('\n').every(line=>line.startsWith('> ')));
  assert.ok(safe.includes('\\# Replace'));
  assert.ok(safe.includes('\\[click\\]'));
  assert.ok(safe.includes('\\`\\`\\`'));
  assert.ok(buildBrief({priorities:attack}).includes(safe));
});
test('research outputs carry the requested law map and contention fields', () => {
  const brief=buildBrief();
  for(const label of ['Law title','section/provision','Government level','Location','Applicability reason and conditions','Official source URL','currency checked','Confidence / needs-check','Contention / linked issue','practical burden','change sought']) assert.ok(brief.includes(label),label);
  for(const instruction of ['duties imposed on a provider','contracts, platform terms','commencement','transitional rules','responsible authority']) assert.ok(brief.includes(instruction),instruction);
});
test('stored input is restricted to recognised question fields and values', () => {
  const data=cleanAnswers({unexpected:'ignored',familyRoles:['Parent or guardian','fake'],places:[null,{jurisdiction:'FAKE',purpose:['Living','fake']}],workTypes:'bad'});
  assert.equal(data.unexpected,undefined);
  assert.deepEqual(data.familyRoles,['Parent or guardian']);
  assert.deepEqual(data.workTypes,[]);
  assert.equal(data.places[0].jurisdiction,'');
  assert.deepEqual(data.places[0].purpose,['Living']);
});
test('supplied civic areas survive cleaning and export as separate uncertain context', () => {
  const place={jurisdiction:'QLD',council:'Redland City',ward:'Division unknown',stateElectorate:'Capalaba',stateRegion:'Not applicable',federalElectorate:'Bowman'};
  const cleaned=cleanAnswers({places:[place]}).places[0];
  const brief=buildBrief({places:[place]});
  for(const key of ['council','ward','stateElectorate','stateRegion','federalElectorate']) {
    assert.equal(cleaned[key],place[key]);assert.ok(brief.includes(quoteAnswer(place[key])));
  }
  assert.ok(brief.includes('distinct overlapping layers'));
  assert.ok(brief.includes('They do not necessarily nest'));
});
test('each jurisdiction supplies distinct existing council, state and federal map doors', () => {
  for(const key of Object.keys(JURISDICTIONS)) {
    const routes=civicRoutes(key);assert.equal(routes.length,3);assert.equal(new Set(routes.map(x=>x.url)).size,3);
    for(const item of routes)assert.ok(existsSync(new URL('../'+new URL(item.url).pathname.slice(1),import.meta.url)),item.url);
    assert.ok(routes[1].url.includes('/places/state/'));assert.ok(routes[2].url.includes('/places/federal/'));
  }
  for(const key of ['OTHER','OVERSEAS','UNKNOWN','', '__proto__'])assert.deepEqual(civicRoutes(key),[]);
});
test('the adaptation keeps the questionnaire self-contained and draft saving scoped', () => {
  const app=readFileSync(new URL('../assets/your-relevance.mjs',import.meta.url),'utf8');
  assert.ok(app.includes("'p4a-your-relevance-draft-v1'"));
  assert.ok(!app.includes('localStorage.clear('));
  assert.ok(!/fetch\s*\(|XMLHttpRequest|sendBeacon|WebSocket/.test(app));
  assert.ok(app.includes('if(!remember.checked) return'));
  assert.equal(SECTIONS.length,12);
});
test('page-local links resolve and the upstream licence bytes retain their pinned identity', () => {
  const page=readFileSync(new URL('../pages/your-relevance.html',import.meta.url),'utf8');
  for(const match of page.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const target=new URL(match[1],'https://p4a.xyz/pages/your-relevance.html');
    if(target.origin==='https://p4a.xyz')assert.ok(existsSync(new URL('../'+target.pathname.slice(1),import.meta.url)),target.href);
  }
  const licence=readFileSync(new URL('../docs/attribution/your-relevance-source-licence.md',import.meta.url));
  const sha=createHash('sha1').update('blob '+licence.length+'\0').update(licence).digest('hex');
  assert.equal(sha,'e50c1c9bb1fe4599256e86792bfce2d484ff9924');
  assert.ok(page.includes('97b523a9253f968dfe901b144cea8c32a52a9ed4'));
});
