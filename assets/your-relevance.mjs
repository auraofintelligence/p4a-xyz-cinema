import {SECTIONS, PLACE_FIELDS, JURISDICTIONS, FEDERAL, TERRITORIES, ACT_CONTEXT, civicRoutes, buildBrief, cleanAnswers, fieldVisible, hasValue} from './your-relevance-model.mjs?v=20261023';

const byId = id => document.getElementById(id);
const STORAGE_KEY = 'p4a-your-relevance-draft-v1';
const form = byId('life-form');
const output = byId('brief-output');
const remember = byId('remember');
const fieldControls = new Map();
const panels = [];
const navButtons = [];
let placeControls = [];
let nextPlaceId = 0;
let active = 0;
let edited = false;
let dirty = true;
let restored = null;

function el(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
}
function link(text, href) {
  const element = el('a', text); element.href = href; return element;
}
function button(text, callback, className) {
  const element = el('button', text, className); element.type = 'button';
  element.addEventListener('click', callback); return element;
}
function createField(field, prefix = '') {
  const id = prefix + field.id;
  const group = el(field.type === 'checks' ? 'fieldset' : 'div', undefined, 'field');
  group.dataset.field = field.id;
  const controls = [];
  if (field.type === 'checks') {
    group.append(el('legend', field.label));
    const choices = el('div', undefined, 'choices');
    for (const [index, option] of field.options.entries()) {
      const label = el('label', undefined, 'check-line');
      const input = el('input'); input.type = 'checkbox'; input.name = id; input.id = id + '-' + index; input.value = option;
      label.append(input, document.createTextNode(option)); choices.append(label); controls.push(input);
    }
    group.append(choices);
  } else {
    const label = el('label', field.label); label.htmlFor = id; group.append(label);
    if (field.hint) {
      const hint = el('span', field.hint, 'hint'); hint.id = id + '-hint'; group.append(hint);
    }
    const input = el(field.type === 'select' ? 'select' : field.type === 'textarea' ? 'textarea' : 'input');
    if(input.tagName === 'INPUT') input.type = 'text';
    if(input.tagName === 'TEXTAREA') input.rows = 3;
    input.id = id; input.name = id;
    if(field.hint) input.setAttribute('aria-describedby', id + '-hint');
    if(field.type === 'select') {
      const placeholder = el('option', 'Choose, or leave blank'); placeholder.value = ''; input.append(placeholder);
      for (const [value, name] of field.options) { const option = el('option', name); option.value = value; input.append(option); }
    }
    group.append(input); controls.push(input);
  }
  return {field, group, controls};
}
function readControl({field, controls}) {
  return field.type === 'checks' ? controls.filter(control => control.checked).map(control => control.value) : controls[0].value;
}
function fillControl({field, controls}, value) {
  if(field.type === 'checks') controls.forEach(control => { control.checked = Array.isArray(value) && value.includes(control.value); });
  else controls[0].value = typeof value === 'string' ? value : '';
}
function readAnswers() {
  return cleanAnswers({
    ...Object.fromEntries([...fieldControls.entries()].map(([id, control]) => [id, readControl(control)])),
    places: placeControls.map(place => Object.fromEntries(place.fields.map(control => [control.field.id, readControl(control)])))
  });
}
function renderPlaceRoute(place) {
  const key = readControl(place.fields.find(control => control.field.id === 'jurisdiction'));
  const region = JURISDICTIONS[key];
  const route = place.route; route.replaceChildren();
  const paragraph = el('p'); paragraph.append(link('Commonwealth register', FEDERAL)); route.append(paragraph);
  if(region) {
    const p = el('p'); p.append(link(region.name + ' legislation', region.register), document.createTextNode(' · '), link(key === 'ACT' ? 'ACT municipal services' : 'Find the council', region.council));
    if(region.boundaries) p.append(document.createTextNode(' · '), link('Council boundary maps',region.boundaries));
    route.append(p);
    const maps=el('nav',undefined,'civic-route-links'); maps.setAttribute('aria-label',region.name+' civic maps');
    maps.append(el('strong','Find your P4A civic areas'));
    for(const item of civicRoutes(key,new URL('../',import.meta.url).href)) maps.append(link(item.label,item.url));
    route.append(maps,el('p','Council/ward, state/territory and federal areas are separate overlapping layers. Use each map, then open the existing area page; the boundaries do not necessarily nest.'));
    const note = el('p');
    if(key === 'ACT') note.append(document.createTextNode('The ACT combines territory and local responsibilities. '), link('How this works', ACT_CONTEXT));
    else note.textContent = 'Confirm the council or administering authority for this activity. On its official site, look for local laws/by-laws and planning instruments.';
    route.append(note);
  } else if(key === 'OTHER') {
    const p=el('p'); p.append(document.createTextNode('Name the territory above. Check its own arrangements and applied laws: '), link('Australian territories', TERRITORIES)); route.append(p);
  } else if(key === 'OVERSEAS') route.append(el('p', 'Name the country and activity above. The brief will ask for a separate cross-border and official-source check.'));
  else route.append(el('p', 'Choose a state or territory to see its official starting points. An unknown location stays a research gap.'));
}
function addPlace(values = {}, focus = true) {
  const id = ++nextPlaceId;
  const node = el('fieldset', undefined, 'place-card');
  const legend = el('legend'); node.append(legend);
  const fields = PLACE_FIELDS.map(field => createField(field, 'place-' + id + '-'));
  fields.forEach(control => { fillControl(control, values[control.field.id]); node.append(control.group); });
  const route = el('div', undefined, 'routing');
  const place = {node, fields, legend, route};
  const remove = button('Remove this place', () => {
    if(fields.some(control => hasValue(readControl(control))) && !confirm('Remove this place and its answers from the draft?')) return;
    node.remove(); placeControls = placeControls.filter(item => item !== place);
    if(!placeControls.length) addPlace({}, false);
    renumberPlaces(); changed(); byId('add-place').focus();
  }, 'quiet-button');
  node.append(remove, route); byId('places-list').append(node); placeControls.push(place);
  renumberPlaces(); renderPlaceRoute(place);
  if(focus) { changed(); fields[0].controls[0].focus(); }
}
function renumberPlaces() { placeControls.forEach((place,index) => { place.legend.textContent = 'Place ' + (index + 1); }); }

for (const [index, section] of SECTIONS.entries()) {
  const panel = el('section', undefined, 'question-panel'); panel.id = 'section-' + section.id; panel.hidden = true;
  panel.setAttribute('aria-labelledby', section.id + '-heading');
  const heading = el('h2', section.title); heading.id = section.id + '-heading'; heading.tabIndex = -1;
  panel.append(el('p', 'Section ' + (index + 1) + ' · Optional', 'kicker'), heading, el('p', section.intro, 'intro'));
  for (const field of section.fields) {
    const control = createField(field); fieldControls.set(field.id, control); panel.append(control.group);
  }
  const retained = el('p', 'Earlier answers from hidden follow-ups are still included in your brief. Reopen the relevant options to review or clear them.', 'retained-note');
  retained.hidden = true; retained.dataset.retained = section.id; panel.append(retained);
  if(section.id === 'places') {
    panel.append(el('div')); panel.lastChild.id = 'places-list';
    const add = button('Add another place', () => addPlace()); add.id = 'add-place'; panel.append(add);
  }
  panel.append(button('Clear this section', () => {
    if(!confirm('Clear the answers in ' + section.title + '?')) return;
    section.fields.forEach(field => fillControl(fieldControls.get(field.id), ''));
    if(section.id === 'places') {
      byId('places-list').replaceChildren(); placeControls = []; addPlace({}, false);
    }
    changed(); heading.focus(); byId('form-status').textContent = section.title + ' cleared.';
  }, 'quiet-button section-clear'));
  byId('question-sections').append(panel); panels.push(panel);
}
panels.push(byId('brief-section'));
for (const [index, title] of [...SECTIONS.map(section => section.title), 'Review & export'].entries()) {
  const option = el('option', (index + 1) + '. ' + title); option.value = String(index); byId('section-choice').append(option);
  const item = el('li');
  const nav = button((index + 1) + '. ' + title, () => showSection(index)); nav.setAttribute('aria-controls', panels[index].id);
  nav.append(el('span')); item.append(nav); byId('section-list').append(item); navButtons.push(nav);
}
const sourceList = el('ul');
for (const [key, region] of Object.entries(JURISDICTIONS)) {
  const item = el('li'); item.append(link(region.name + ' legislation', region.register), document.createTextNode(' · '), link(key === 'ACT' ? 'Municipal services' : 'Council finder', region.council));
  if(region.boundaries) item.append(document.createTextNode(' · '), link('Council boundary maps',region.boundaries));
  sourceList.append(item);
}
byId('all-sources').append(sourceList);

function sectionCount(section, data) {
  return section.fields.filter(field => hasValue(data[field.id])).length + (section.id === 'places' ? data.places.filter(place => PLACE_FIELDS.some(field => hasValue(place[field.id]))).length : 0);
}
function refresh(data = readAnswers()) {
  for (const section of SECTIONS) {
    let retained = false;
    for(const field of section.fields) {
      const visible = fieldVisible(field, data); fieldControls.get(field.id).group.hidden = !visible;
      if(!visible && hasValue(data[field.id])) retained = true;
    }
    document.querySelector('[data-retained="' + section.id + '"]').hidden = !retained;
  }
  placeControls.forEach(renderPlaceRoute);
  const counts = SECTIONS.map(section => sectionCount(section, data));
  counts.forEach((count, index) => { navButtons[index].querySelector('span').textContent = count ? count + ' answered' : 'Optional'; });
  navButtons.at(-1).querySelector('span').textContent = edited ? 'Edited brief' : 'Copy or download';
  byId('answer-count').textContent = counts.filter(Boolean).length + ' of ' + SECTIONS.length + ' sections have answers';
  if(active === SECTIONS.length) renderSummary(data);
}
function renderSummary(data) {
  const summary = byId('review-summary'); summary.replaceChildren();
  const count = SECTIONS.filter(section => sectionCount(section, data)).length;
  summary.append(el('p', count + ' of ' + SECTIONS.length + ' question sections have answers. Unanswered topics remain unknown.'));
  const list=el('ul');
  for(const section of SECTIONS) {
    const count=sectionCount(section,data);
    if(count) { const item=el('li'); item.append(button(section.title + ': ' + count + ' answered', () => showSection(SECTIONS.indexOf(section)), 'summary-link')); list.append(item); }
  }
  if(count) summary.append(list);
  if(!data.places.some(place => JURISDICTIONS[place.jurisdiction] || ['OTHER','OVERSEAS'].includes(place.jurisdiction))) summary.append(el('p', 'Location routing needs checking. Add a state, territory or country if you want a more focused brief.'));
  const hiddenAnswers=SECTIONS.flatMap(section=>section.fields).filter(field=>!fieldVisible(field,data)&&hasValue(data[field.id])).length;
  if(hiddenAnswers) summary.append(el('p', hiddenAnswers + ' earlier follow-up answers are included even though their options are now unticked. Return to those sections to review or clear them.'));
}
function refreshBrief() {
  if(!edited && dirty) { output.value = buildBrief(readAnswers()); dirty = false; }
  byId('brief-status').textContent = edited && dirty ? 'Answers changed since you edited this brief. Rebuild to include the latest answers, or keep your edited text.' : edited ? 'Your edited brief is kept.' : 'Built from your current answers. Review and edit before sharing.';
}
function showSection(index, focus = true) {
  active = Math.max(0, Math.min(panels.length - 1, Number(index) || 0));
  panels.forEach((panel, i) => { panel.hidden = i !== active; });
  navButtons.forEach((nav, i) => { if(i === active) nav.setAttribute('aria-current', 'step'); else nav.removeAttribute('aria-current'); });
  byId('section-choice').value = String(active);
  byId('position').textContent = 'Section ' + (active + 1) + ' of ' + panels.length;
  byId('section-progress').max = panels.length; byId('section-progress').value = active + 1;
  byId('previous-section').disabled = active === 0;
  byId('next-section').hidden = active === panels.length - 1;
  byId('next-section').textContent = active === SECTIONS.length - 1 ? 'Review & export' : 'Next section';
  byId('review-brief').hidden = active === panels.length - 1;
  byId('form-status').textContent = ''; byId('export-status').textContent = '';
  if(active === SECTIONS.length) refreshBrief();
  refresh(); saveDraft();
  if(focus) panels[active].querySelector('h2').focus();
}
function saveDraft() {
  if(!remember.checked) return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({version: 1, optedIn: true, answers: readAnswers(), active, edited, dirty, brief: edited ? output.value : ''}));
    byId('save-status').textContent = 'Draft saved on this device, including any edited brief. Clear / reset removes it. Other people using this browser may see it.';
  } catch {
    byId('save-status').textContent = 'Device saving failed. Keep this tab open, or download your brief before leaving.';
  }
}
function changed() {
  dirty = true; refresh(); saveDraft(); byId('form-status').textContent = '';
}
form.addEventListener('submit', event => event.preventDefault());
form.addEventListener('input', changed);
form.addEventListener('change', changed);
byId('section-choice').addEventListener('change', event => showSection(event.target.value));
byId('previous-section').addEventListener('click', () => showSection(active - 1));
byId('next-section').addEventListener('click', () => showSection(active + 1));
byId('review-brief').addEventListener('click', () => showSection(SECTIONS.length));
remember.addEventListener('change', () => {
  if(remember.checked) saveDraft();
  else {
    try { localStorage.removeItem(STORAGE_KEY); byId('save-status').textContent = 'Device saving is off. The saved draft was removed; current answers stay in this tab.'; }
    catch { byId('save-status').textContent = 'Device saving is off, but the previous saved draft could not be removed. Use your browser’s site-data controls to remove it.'; }
  }
});
output.addEventListener('input', () => { edited = true; refreshBrief(); refresh(); saveDraft(); });
byId('rebuild-brief').addEventListener('click', () => {
  if(edited && !confirm('Replace your edited brief with a fresh brief from the current answers?')) return;
  edited = false; dirty = true; refreshBrief(); refresh(); saveDraft();
  byId('export-status').textContent = 'Brief rebuilt from your answers.';
});
function readyToExport() {
  refreshBrief();
  if(edited && dirty && !confirm('Your answers changed after you edited this brief. Export your edited text as it is? Cancel, then use Rebuild to include the latest answers.')) return false;
  if(!output.value.trim()) { byId('export-status').textContent = 'The brief is empty. Add text or rebuild it from your answers.'; output.focus(); return false; }
  return true;
}
byId('copy-brief').addEventListener('click', async () => {
  if(!readyToExport()) return;
  try { await navigator.clipboard.writeText(output.value); byId('export-status').textContent = 'Brief copied. You choose where to paste it.'; }
  catch { output.focus(); output.select(); byId('export-status').textContent = 'Clipboard access is unavailable. The brief is selected for manual copying, or use Download .md.'; }
});
byId('download-brief').addEventListener('click', () => {
  if(!readyToExport()) return;
  const url = URL.createObjectURL(new Blob([output.value], {type: 'text/markdown;charset=utf-8'}));
  const anchor = link('', url); anchor.download = 'my-p4a-law-research-brief.md'; document.body.append(anchor); anchor.click(); anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
  byId('export-status').textContent = 'Brief downloaded. Review it before sharing.';
});
document.querySelectorAll('[data-reset]').forEach(control => control.addEventListener('click', () => {
  if(!confirm('Clear all answers, edited brief and the saved draft on this device? Download first if you want to keep a copy.')) return;
  let removed = true;
  try { localStorage.removeItem(STORAGE_KEY); } catch { removed = false; }
  fieldControls.forEach(control => fillControl(control, ''));
  byId('places-list').replaceChildren(); placeControls = []; addPlace({}, false);
  remember.checked = false; edited = false; dirty = true; output.value = ''; showSection(0);
  byId('save-status').textContent = removed ? 'Draft cleared. Device saving is off.' : 'Form cleared and saving is off. The saved draft could not be removed; use your browser’s site-data controls.';
  byId('form-status').textContent = 'Answers and edited brief cleared.';
}));
// The Job Ad Formula's floating-control pattern: keep both corners clear of inputs.
const toTop = byId('to-top');
function updateToTop() {
  if(document.activeElement === toTop) return;
  toTop.hidden = window.scrollY < 400;
  if(toTop.hidden) return;
  const controls = [...document.querySelectorAll('input,textarea,select,button,a,label,summary,[tabindex]')].filter(control=>control!==toTop && control.getClientRects().length);
  for(const left of [false,true]) {
    toTop.classList.toggle('to-top-left',left);
    const box=toTop.getBoundingClientRect();
    const blocked=controls.some(control=>{
      const rect=control.getBoundingClientRect();
      return rect.left < box.right+8 && rect.right > box.left-8 && rect.top < box.bottom+8 && rect.bottom > box.top-8;
    });
    if(!blocked) return;
  }
  toTop.hidden = true;
}
let topUpdateQueued = false;
function scheduleTopUpdate() {
  if(topUpdateQueued) return;
  topUpdateQueued = true;
  requestAnimationFrame(()=>{topUpdateQueued=false;updateToTop();});
}
window.addEventListener('scroll',scheduleTopUpdate,{passive:true});
window.addEventListener('resize',scheduleTopUpdate);
for(const event of ['focusin','focusout','input','change']) document.addEventListener(event,scheduleTopUpdate);
toTop.addEventListener('click', event => {
  event.preventDefault(); window.scrollTo({top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  const heading = document.querySelector('h1'); heading.tabIndex = -1; heading.focus({preventScroll: true});
});

try {
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
  if(saved && saved.version === 1 && saved.optedIn === true && saved.answers && typeof saved.answers === 'object') restored = saved;
} catch { byId('save-status').textContent = 'No readable saved draft is available. Device saving is off.'; }
const initial = cleanAnswers(restored?.answers);
fieldControls.forEach((control,id) => fillControl(control, initial[id]));
for(const place of initial.places.length ? initial.places : [{}]) addPlace(place, false);
if(restored) {
  remember.checked = true; edited = restored.edited === true && typeof restored.brief === 'string'; dirty = restored.dirty === true;
  output.value = edited ? restored.brief : buildBrief(initial);
}
showSection(restored?.active ?? 0, false);
byId('questionnaire').hidden = false;
updateToTop();
