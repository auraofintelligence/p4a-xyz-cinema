/* Coordinates remain untouched in the source. Drawing and picking share one
   reversible equirectangular projection (standard parallel 37 degrees south),
   with no geometry simplification. Its affine transform also preserves every
   straight GeoJSON segment exactly, including very long rural boundaries. */
(function (root) {
  'use strict';
  // Local origin improves Canvas path precision at close zoom without changing
  // the projection or any source vertex.
  const project = ([lon, lat]) => [(lon - 144) * Math.cos(37 * Math.PI / 180) * Math.PI / 180, -(lat + 37) * Math.PI / 180];
  const polygons = geometry => geometry.type === 'Polygon' ? [geometry.coordinates] : geometry.coordinates;
  const insideRing = (point, ring) => {
    let inside = false;
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      const a = ring[i], b = ring[j];
      if ((a[1] > point[1]) !== (b[1] > point[1]) && point[0] < (b[0] - a[0]) * (point[1] - a[1]) / (b[1] - a[1]) + a[0]) inside = !inside;
    }
    return inside;
  };
  const contains = (point, geometry) => polygons(geometry).some(rings => insideRing(point, rings[0]) && !rings.slice(1).some(r => insideRing(point, r)));
  const calendarDay = (instant, timeZone = 'Australia/Melbourne') => {
    const parts = new Intl.DateTimeFormat('en-AU', {timeZone, year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date(instant));
    const get = type => Number(parts.find(p => p.type === type).value);
    return Date.UTC(get('year'), get('month') - 1, get('day')) / 86400000;
  };
  const api = {project, polygons, contains, calendarDay, daysUntil: (target, now = Date.now()) => Math.max(0, calendarDay(target) - calendarDay(now))};
  root.P4A_VIC_GEOMETRY = api;
  if (typeof module !== 'undefined') module.exports = api;
})(globalThis);
