import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const script = readFileSync(new URL('../assets/p4a-builders.js', import.meta.url), 'utf8');
const moduleIds = [...script.slice(script.indexOf('const moduleConfigs ='), script.indexOf('const builderFieldText =')).matchAll(/^    "([a-z-]+)": \{/gm)].map(m => m[1]);
const ids = ['noticeboard-contract', 'private-profile', ...moduleIds];

function run(id, legacy = {}) {
  const fields = ['group_name','civic_name','record_title','public_offer','public_roles','public_summary'].map(name => ({ name, type: 'text', value: '', setAttribute() {} }));
  const events = {};
  const form = { dataset: { p4aBuilder: id }, hasAttribute: () => false,
    querySelectorAll: () => fields, querySelector: () => null,
    addEventListener: (name, callback) => { events[name] = callback; },
    reset: () => fields.forEach(field => { field.value = ''; }) };
  const output = { value: '' };
  const buttons = { clear: { addEventListener: (name, callback) => { events.clear = callback; } } };
  const key = `p4a-builder:${id}`;
  const storage = new Map([[key, JSON.stringify(legacy)]]);
  const context = {
    document: { querySelector: selector => selector === '[data-p4a-builder]' ? form : selector === '[data-builder-output]' ? output : selector === '[data-clear-builder]' ? buttons.clear : null, querySelectorAll: () => [] },
    window: { location: { search: '' } }, URLSearchParams, Date,
    sessionStorage: { getItem: k => storage.get(k), setItem: (k,v) => storage.set(k,v), removeItem: k => storage.delete(k) },
    FormData: class { get(name) { return fields.find(f => f.name === name)?.value ?? null; } getAll() { return []; } }
  };
  vm.runInNewContext(script, context);
  return { output, fields, events, storage, key };
}

test('all fourteen builders omit retired private/excluded fields from Markdown', () => {
  assert.equal(ids.length, 14);
  for (const id of ids) {
    const legacy = { private_boundary: 'PRIVATE_SENTINEL', private_exclusions: 'EXCLUDED_SENTINEL', public_summary: 'Chosen public summary', public_offer: 'Chosen public offer', public_roles: 'Chosen public roles' };
    const result = run(id, legacy);
    assert.doesNotMatch(result.output.value, /PRIVATE_SENTINEL|EXCLUDED_SENTINEL|## Private Or Excluded Material|## Private Boundary|## Private Or Permissioned Boundary/, id);
    assert.match(result.output.value, /Chosen public (summary|offer|roles)/, id);
    assert.match(result.output.value, /^---\nschema: p4a\./, id);
    // Opening the revised builder does not clear any saved draft.
    assert.deepEqual(JSON.parse(result.storage.get(result.key)), legacy);
    // The next normal edit preserves displayed fields and no longer stores retired inputs.
    result.events.input();
    const saved = JSON.parse(result.storage.get(result.key));
    assert.equal(saved.private_boundary, undefined);
    assert.equal(saved.private_exclusions, undefined);
    assert.equal(saved.public_summary, legacy.public_summary);
  }
});

test('forms have no retired input and explain that only chosen Markdown content belongs here', () => {
  for (const name of ['noticeboard-contract-builder', 'private-civic-profile-builder', 'p4a-builder']) {
    const html = readFileSync(new URL(`../pages/${name}.html`, import.meta.url), 'utf8');
    assert.doesNotMatch(html, /name="(?:private_boundary|private_exclusions)"/);
    assert.match(html, /Include only what you want in the Markdown file\. Leave private or excluded information out\./);
    assert.match(html, /p4a-builders\.js\?v=20261102-markdown-fields/);
  }
});

test('ordinary edit and clear behaviour remain intact', () => {
  const result = run('noticeboard-contract', { group_name: 'Community noticeboard', public_offer: 'Weekly updates' });
  assert.match(result.output.value, /Community noticeboard Public Noticeboard/);
  result.fields.find(f => f.name === 'public_offer').value = 'New public update';
  result.events.change();
  assert.match(result.output.value, /New public update/);
  assert.equal(JSON.parse(result.storage.get(result.key)).public_offer, 'New public update');
  result.events.clear();
  assert.equal(result.storage.has(result.key), false);
  assert.doesNotMatch(result.output.value, /New public update|Community noticeboard/);
});
