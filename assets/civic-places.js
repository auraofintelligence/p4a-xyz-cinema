/* Exact source coordinates projected for Canvas display. No boundary simplification. */
(() => {
  'use strict';
  const normal = value => String(value ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const dayNumber = (date, zone) => {
    const parts = new Intl.DateTimeFormat('en-CA', {timeZone: zone, year: 'numeric', month: '2-digit', day: '2-digit'}).formatToParts(date);
    const part = type => parts.find(p => p.type === type).value;
    return Date.UTC(Number(part('year')), Number(part('month')) - 1, Number(part('day'))) / 86400000;
  };
  function clockLabel(event, now = new Date()) {
    if (!event.date || !/^\d{4}-\d{2}-\d{2}/.test(event.date)) return 'Date not announced';
    const zone = event.timezone || 'Australia/Brisbane';
    const target = Date.parse(event.date.slice(0, 10) + 'T00:00:00Z') / 86400000;
    const delta = target - dayNumber(now, zone);
    const milestone = event.milestoneLabel || 'polling day', closes = /closes/i.test(milestone);
    if (delta > 0) return `${delta.toLocaleString('en-AU')} day${delta === 1 ? '' : 's'} ${closes ? 'until' : 'to'} ${milestone}`;
    if (delta === 0 && closes && event.dateTime && Number.isFinite(Date.parse(event.dateTime))) {
      const remaining = Date.parse(event.dateTime) - now.getTime();
      if (remaining <= 0) return 'Voting closed today · check official results';
      const minutes = Math.ceil(remaining / 60000), hours = Math.floor(minutes / 60), rest = minutes % 60;
      return `Voting closes today · ${hours ? hours + ' hour' + (hours === 1 ? '' : 's') + ' ' : ''}${rest} minute${rest === 1 ? '' : 's'} remaining`;
    }
    if (delta === 0) return (closes ? 'Voting closes today' : milestone[0].toUpperCase() + milestone.slice(1)) + ' · check official voting information';
    return `${(-delta).toLocaleString('en-AU')} day${delta === -1 ? '' : 's'} since ${closes ? 'voting closed' : milestone}`;
  }
  window.P4A_CIVIC_CLOCK = {clockLabel, dayNumber};
  document.querySelectorAll('[data-civic-clock]').forEach(el => {
    try {
      const event = JSON.parse(el.dataset.civicClock);
      const update = () => { el.textContent = clockLabel(event); };
      update(); setInterval(update, 60000);
    } catch { el.textContent = 'Check the official timetable'; }
  });
  document.querySelectorAll('[data-directory-filter]').forEach(input => {
    const list = document.getElementById(input.getAttribute('aria-controls'));
    if (!list) return;
    input.addEventListener('input', () => {
      const query = normal(input.value);
      let found = 0;
      for (const li of list.children) { li.hidden = !normal(li.textContent + ' ' + (li.dataset.search || '')).includes(query); if (!li.hidden) found++; }
      const status = input.parentElement.querySelector('[data-directory-count]');
      if (status) status.textContent = found ? `${found} matching places` : 'No matching place. Clear the search to see every area.';
    });
  });
  const root = document.querySelector('[data-civic-map]');
  if (!root) return;
  const configEl = document.getElementById('civic-map-config');
  if (!configEl) return;
  const config = JSON.parse(configEl.textContent);
  const canvas = root.querySelector('canvas'), ctx = canvas.getContext('2d');
  const siteRoot = new URL(config.siteRoot, location.href);
  const selectLayer = root.querySelector('[data-civic-layer]');
  const input = root.querySelector('[data-civic-search]');
  const results = root.querySelector('[data-civic-results]');
  const count = root.querySelector('[data-civic-count]');
  const message = root.querySelector('[data-civic-message]');
  const selection = root.querySelector('[data-civic-selection]');
  const cache = new Map(), pointers = new Map();
  const colours = ['#a297bd', '#80aaac', '#b5a98a', '#8fa7c0', '#bba2a6', '#9eaf91'];
  let shapes = [], items = [], selected = null, layer = null, view = {x: 0, y: 0, scale: 1};
  let width = 0, height = 0, dpr = 1, raf = 0, sequence = 0, quiet = true, initial = true;
  let baseImage = null, detailImage = null, detailExtent = null, detailTimer = 0;
  const R = 6378137;
  const project = ([lon, lat]) => [R * lon * Math.PI / 180, R * Math.log(Math.tan(Math.PI / 4 + Math.max(-85.0511, Math.min(85.0511, lat)) * Math.PI / 360))];
  const inverse = ([x, y]) => [x / R * 180 / Math.PI, (2 * Math.atan(Math.exp(y / R)) - Math.PI / 2) * 180 / Math.PI];
  const screen = ([x, y]) => [(x - view.x) * view.scale + width / 2, (view.y - y) * view.scale + height / 2];
  const world = ([x, y]) => [(x - width / 2) / view.scale + view.x, view.y - (y - height / 2) / view.scale];
  const point = event => { const rect = canvas.getBoundingClientRect(); return [event.clientX - rect.left, event.clientY - rect.top]; };
  function fit(bounds) {
    if (!bounds || !Number.isFinite(bounds[0])) return;
    view.x = (bounds[0] + bounds[2]) / 2; view.y = (bounds[1] + bounds[3]) / 2;
    view.scale = Math.min((width - 54) / Math.max(100, bounds[2] - bounds[0]), (height - 54) / Math.max(100, bounds[3] - bounds[1]));
    queue(); scheduleDetail();
  }
  const boundsOf = entries => entries.reduce((b, s) => [Math.min(b[0], s.bounds[0]), Math.min(b[1], s.bounds[1]), Math.max(b[2], s.bounds[2]), Math.max(b[3], s.bounds[3])], [Infinity, Infinity, -Infinity, -Infinity]);
  const allBounds = () => boundsOf(shapes);
  function queue() { if (!raf) raf = requestAnimationFrame(() => { raf = 0; draw(); }); }
  function raster(image, extent, muted) {
    if (!image || !extent) return;
    const [x, y] = screen([extent.xmin, extent.ymax]);
    ctx.save(); ctx.filter = muted ? 'grayscale(1) opacity(0.7)' : 'none';
    ctx.drawImage(image, x, y, (extent.xmax - extent.xmin) * view.scale, (extent.ymax - extent.ymin) * view.scale);
    ctx.restore();
  }
  function draw() {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = '#e5e8e9'; ctx.fillRect(0, 0, width, height);
    raster(baseImage, config.basemap?.extent, true);
    raster(detailImage, detailExtent, quiet);
    const lo = world([0, height]), hi = world([width, 0]);
    ctx.setTransform(dpr * view.scale, 0, 0, -dpr * view.scale, dpr * (width / 2 - view.x * view.scale), dpr * (height / 2 + view.y * view.scale));
    for (const shape of shapes) {
      const b = shape.bounds;
      if (b[2] < lo[0] || b[0] > hi[0] || b[3] < lo[1] || b[1] > hi[1]) continue;
      ctx.fillStyle = shape.item?.id === selected?.id ? '#e9b93677' : colours[shape.index % colours.length] + '35';
      ctx.strokeStyle = shape.item?.id === selected?.id ? '#785500' : '#50446699';
      ctx.lineWidth = (shape.item?.id === selected?.id ? 2.2 : .85) / view.scale;
      ctx.fill(shape.path, 'evenodd'); ctx.stroke(shape.path);
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function buildShape(feature, index, item) {
    const path = new Path2D(), bounds = [Infinity, Infinity, -Infinity, -Infinity];
    const source = feature.geometry.type === 'Polygon' ? [feature.geometry.coordinates] : feature.geometry.coordinates;
    const polygons = source.map(polygon => polygon.map(ring => ring.map(coordinate => {
      const p = project(coordinate); bounds[0] = Math.min(bounds[0], p[0]); bounds[1] = Math.min(bounds[1], p[1]); bounds[2] = Math.max(bounds[2], p[0]); bounds[3] = Math.max(bounds[3], p[1]); return p;
    })));
    for (const polygon of polygons) for (const ring of polygon) {
      ring.forEach(([x, y], i) => i ? path.lineTo(x, y) : path.moveTo(x, y)); path.closePath();
    }
    return {path, polygons, bounds, item, index};
  }
  function insideRing([x, y], ring) {
    let inside = false;
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      const [xi, yi] = ring[i], [xj, yj] = ring[j];
      if (((yi > y) !== (yj > y)) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside;
    }
    return inside;
  }
  function pick(p) {
    for (let i = shapes.length - 1; i >= 0; i--) {
      const s = shapes[i], b = s.bounds;
      if (!s.item || p[0] < b[0] || p[0] > b[2] || p[1] < b[1] || p[1] > b[3]) continue;
      if (s.polygons.some(poly => poly.reduce((inside, ring) => inside !== insideRing(p, ring), false))) return s.item;
    }
    return null;
  }
  function updateURL(replace = false) {
    const url = new URL(location.href); url.searchParams.set('layer', layer.id);
    if (selected) url.searchParams.set('area', selected.id); else url.searchParams.delete('area');
    history[replace ? 'replaceState' : 'pushState']({}, '', url);
  }
  function choose(item, zoom = false, historyMode = 'push') {
    selected = item; selection.hidden = false;
    selection.querySelector('[data-civic-selection-name]').textContent = item.name;
    selection.querySelector('[data-civic-selection-kind]').textContent = item.kindLabel || item.kind;
    selection.querySelector('[data-civic-selection-people]').textContent = (item.members || []).join(' · ') || 'Open the page for representation, election history and sources.';
    const open = selection.querySelector('[data-civic-open]'), destination = new URL(item.url, siteRoot);
    destination.searchParams.set('layer', layer.id); destination.searchParams.set('area', item.id);
    open.href = destination; open.textContent = 'Open ' + item.name;
    message.textContent = item.name + ' · selected';
    if (zoom) { const selectedShapes = shapes.filter(s => s.item?.id === item.id); if (selectedShapes.length) fit(boundsOf(selectedShapes)); }
    renderResults(); queue(); if (historyMode !== 'none') updateURL(historyMode === 'replace');
  }
  function renderResults() {
    const query = normal(input.value), matches = items.filter(item => normal(item.name + ' ' + (item.aliases || '') + ' ' + (item.members || []).join(' ')).includes(query));
    results.replaceChildren();
    count.textContent = matches.length ? `${matches.length} matching areas` : 'No matching area. Try its official name or clear the search.';
    for (const item of matches.slice(0, 120)) {
      const li = document.createElement('li'), button = document.createElement('button'); button.type = 'button'; button.textContent = item.name;
      button.setAttribute('aria-pressed', item.id === selected?.id ? 'true' : 'false');
      const note = document.createElement('small'); note.textContent = item.kindLabel || item.kind; button.append(note);
      button.addEventListener('click', () => choose(item, true)); li.append(button); results.append(li);
    }
    if (matches.length > 120) { const li = document.createElement('li'); li.textContent = 'Refine your search or use the full text directory below.'; results.append(li); }
  }
  async function fetchGeometry(entry) {
    const rawURL = new URL(entry.geometryFile, siteRoot);
    const compressedURL = entry.compressedFile && new URL(entry.compressedFile, siteRoot);
    if (entry.compressedFile && typeof DecompressionStream !== 'undefined') {
      try {
        const response = await fetch(new URL(entry.compressedFile, siteRoot)); if (!response.ok) throw Error('compressed response');
        const bytes = new Uint8Array(await response.arrayBuffer());
        if (bytes[0] === 31 && bytes[1] === 139) return JSON.parse(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).text());
        return JSON.parse(new TextDecoder().decode(bytes));
      } catch (error) {
        // A gzip-only original has no separate plain-file fallback. Do not
        // request the same large asset again or attempt to parse gzip as JSON.
        if (compressedURL.href === rawURL.href) throw error;
      }
    }
    if (rawURL.pathname.endsWith('.gz')) throw Error('This exact boundary layer requires browser gzip support. Use the linked text directory or official source.');
    const response = await fetch(rawURL); if (!response.ok) throw Error(`Boundary data returned ${response.status}`); return response.json();
  }
  async function loadLayer(id, selectedId = null, historyMode = 'none') {
    const entry = config.layers.find(l => l.id === id) || config.layers[0]; if (!entry) return;
    const token = ++sequence; layer = entry; selectLayer.value = entry.id; selected = null; shapes = []; selection.hidden = true; input.value = '';
    items = config.places.filter(p => p.layerId === entry.id); renderResults();
    message.textContent = 'Loading exact source boundaries…'; root.setAttribute('aria-busy', 'true'); queue();
    try {
      if (!cache.has(entry.id)) cache.set(entry.id, fetchGeometry(entry));
      const source = await cache.get(entry.id); if (token !== sequence) return;
      const joins = new Map(items.flatMap(p => (p.featureIds || [p.featureId]).map(id => [String(id), p])));
      // A scoped view filters whole source features before projection; every
      // coordinate/ring of each displayed feature remains intact.
      shapes = source.features.filter(f => f.geometry && ['Polygon', 'MultiPolygon'].includes(f.geometry.type) && (!config.filterGeometry || joins.has(String(f.properties?.[entry.featureIdField] ?? f.id)))).map((f, i) => buildShape(f, i, joins.get(String(f.properties?.[entry.featureIdField] ?? f.id))));
      message.textContent = `${entry.name} · exact source boundaries`;
      fit(allBounds());
      const item = items.find(p => p.id === selectedId);
      if (item) choose(item, true, historyMode); else if (historyMode !== 'none') updateURL(historyMode === 'replace');
      initial = false;
    } catch (error) {
      if (token !== sequence) return;
      cache.delete(entry.id); message.textContent = 'Map unavailable. Use the complete linked text directory below.';
      console.warn('P4A civic layer unavailable:', entry.id, error.message);
    } finally { if (token === sequence) root.setAttribute('aria-busy', 'false'); }
  }
  function zoom(factor, position = [width / 2, height / 2]) {
    const before = world(position); view.scale = Math.max(0.000001, Math.min(.2, view.scale * factor));
    const after = world(position); view.x += before[0] - after[0]; view.y += before[1] - after[1]; queue(); scheduleDetail();
  }
  function scheduleDetail() {
    clearTimeout(detailTimer); if (!config.basemap?.onlineDetailService) return;
    detailTimer = setTimeout(async () => {
      try {
        const lo = world([0, height]), hi = world([width, 0]);
        const service = new URL(config.basemap.onlineDetailService + '/export');
        service.search = new URLSearchParams({bbox: [...lo, ...hi].join(','), bboxSR: '3857', imageSR: '3857', size: `${Math.min(1600, Math.round(width * dpr))},${Math.min(1200, Math.round(height * dpr))}`, format: 'png32', f: 'json'});
        const response = await fetch(service), metadata = await response.json(); if (!metadata.href || !metadata.extent) throw Error('No registered image');
        const image = new Image(); image.onload = () => { detailImage = image; detailExtent = metadata.extent; queue(); }; image.onerror = () => { message.textContent = 'Online detail unavailable; retained geographic background remains.'; }; image.src = metadata.href;
      } catch { message.textContent = 'Online detail unavailable; retained geographic background remains.'; }
    }, 400);
  }
  canvas.addEventListener('pointerdown', e => { canvas.setPointerCapture(e.pointerId); pointers.set(e.pointerId, {p: point(e), start: point(e), moved: false}); });
  canvas.addEventListener('pointermove', e => {
    const active = pointers.get(e.pointerId); if (!active) return;
    const p = point(e), old = active.p;
    active.moved ||= Math.hypot(p[0] - active.start[0], p[1] - active.start[1]) > 5;
    if (pointers.size === 2) {
      const other = [...pointers.entries()].find(([id]) => id !== e.pointerId)[1];
      const before = Math.hypot(old[0] - other.p[0], old[1] - other.p[1]), after = Math.hypot(p[0] - other.p[0], p[1] - other.p[1]);
      if (before > 0) zoom(after / before, [(p[0] + other.p[0]) / 2, (p[1] + other.p[1]) / 2]);
      active.moved = true; other.moved = true;
    } else { view.x -= (p[0] - old[0]) / view.scale; view.y += (p[1] - old[1]) / view.scale; queue(); }
    active.p = p;
  });
  canvas.addEventListener('pointerup', e => { const active = pointers.get(e.pointerId); pointers.delete(e.pointerId); if (active && !active.moved) { const item = pick(world(point(e))); if (item) choose(item); } scheduleDetail(); });
  canvas.addEventListener('pointercancel', e => pointers.delete(e.pointerId));
  canvas.addEventListener('wheel', e => { e.preventDefault(); zoom(Math.exp(-e.deltaY * .0015), point(e)); }, {passive: false});
  canvas.addEventListener('dblclick', e => { const item = pick(world(point(e))); if (item) choose(item, true); });
  canvas.addEventListener('keydown', e => {
    const moves = {ArrowLeft: [-65, 0], ArrowRight: [65, 0], ArrowUp: [0, 65], ArrowDown: [0, -65]};
    if (moves[e.key]) { e.preventDefault(); view.x += moves[e.key][0] / view.scale; view.y += moves[e.key][1] / view.scale; queue(); scheduleDetail(); }
    else if (['+', '=', '-', 'Home', 'r', 'R'].includes(e.key)) { e.preventDefault(); if (['Home', 'r', 'R'].includes(e.key)) fit(allBounds()); else zoom(e.key === '-' ? .75 : 1.33); }
  });
  root.querySelector('[data-civic-zoom-in]').addEventListener('click', () => zoom(1.5));
  root.querySelector('[data-civic-zoom-out]').addEventListener('click', () => zoom(1 / 1.5));
  root.querySelector('[data-civic-reset]').addEventListener('click', () => fit(allBounds()));
  root.querySelector('[data-civic-selected]').addEventListener('click', () => { if (selected) choose(selected, true, 'none'); });
  root.querySelector('[data-civic-detail]').addEventListener('click', e => { quiet = !quiet; e.currentTarget.setAttribute('aria-pressed', String(!quiet)); e.currentTarget.textContent = quiet ? 'Detailed map / roads' : 'Quiet map'; queue(); scheduleDetail(); });
  input.addEventListener('input', renderResults); selectLayer.addEventListener('change', () => loadLayer(selectLayer.value, null, 'push'));
  addEventListener('popstate', () => { const params = new URL(location.href).searchParams; loadLayer(params.get('layer') || config.initialLayer || config.layers[0]?.id, params.get('area') || config.selectedId); });
  new ResizeObserver(() => { const rect = canvas.getBoundingClientRect(); width = rect.width; height = rect.height; dpr = window.devicePixelRatio || 1; canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr); if (initial && shapes.length) fit(allBounds()); queue(); }).observe(canvas);
  if (config.basemap?.image) { baseImage = new Image(); baseImage.onload = queue; baseImage.src = new URL(config.basemap.image, siteRoot); }
  const params = new URL(location.href).searchParams;
  requestAnimationFrame(() => loadLayer(params.get('layer') || config.initialLayer || config.layers[0]?.id, params.get('area') || config.selectedId));
  // Read-only geometry helpers support independent source-coordinate QA.
  window.P4A_CIVIC_MAP = {getState: () => ({layer: layer?.id, selected: selected?.id, areas: items.length, shapes: shapes.length, view: {...view}}), pickLonLat: p => pick(project(p))?.id ?? null, screenPoint: p => screen(project(p)), project, inverse};
})();
