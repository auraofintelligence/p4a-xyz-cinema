# Civic map navigation — 23 October 2026

The national Australia map now opens each jurisdiction's electorate map directly. Every state/territory portal puts compact Maps, Members and Elections choices before the political summaries. Electorate, council/local-area and federal map pages share visible choices, an active-map highlight and reciprocal Australia/state routes. ACT local areas remain explicitly separate from elected councils. South Australia's map opens its current 2026 House edition; historical editions remain selectable.

The public clone strips, tailoring cards, agent/template setup sections and source-file editing instructions were removed from this visitor journey. Engineering documentation and reusable builders remain in the repository. Existing Victoria and Queensland atlases and the Redlands journey are retained. No roster research, political facts, boundary coordinates, licence terms or grassroots Twinkles changed.

The existing map renderer supplies all interaction. This is a navigation correction, not a replacement map system or a claim that every place has a complete local civic journey.

## Review and checks

The [browser record](../../content/places/qa/browser-review.json) and [observed fixtures](../../content/places/qa/navigation-browser-fixture-2026-10-23.json) record eight scenarios across 27 actual HTML paths. All eight phone portals placed their three map choices before political summaries, with 21.6 px navigation headings, 44.375 px link heights and equal 375 px client/scroll widths after fonts settled. All eight electorate maps loaded their intended layer with readable controls. WA state/whole-state upper-house switching, selection, Open and browser Back/Forward passed; the council Open route and Back restored Perth. ACT Kurrajong retained five representatives and the local-area map retained its unincorporated context. NT electorate/local-map transitions and 680/1280 layouts passed. Federal return choices and keyboard national-map routes passed. The affected legacy Queensland atlas and Redlands candidate doorway retained their map/content and readable phone layout.

The all-jurisdiction navigation regression check validates eight national targets, eight prominent portal entries and 24 reciprocal map directories. National structural validation, contracts, discovery, geometry/delivery and clock outcomes are in the current QA reports and Actions run. Historical reviews are retained under `content/places/qa/pre-navigation-2026-10-23/`; new evidence has its own scope rather than claiming the earlier Index or source reviews were repeated.

The full run exposed an existing bounded-cache eviction defect on Windows Python: `OrderedDict.popitem` could invoke the cache's overridden getter after unlinking its key. The runner now deletes the oldest cached entry directly, preserving the same 96-entry LRU limit and all original validator checks. A regression exercises overflow, eviction, retained reads and replacement. The archived legacy declaration uses a snapshot filename so it cannot be discovered as an active contract.

The complete local run passed all 2,081 contracts with zero failures. Its final metadata-only rebind cites the unchanged common script by canonical Git bytes instead of a Windows working-copy newline fingerprint. All 2,081 declarations were compared unchanged apart from the browser report hash; original evidence checks and current artifact fingerprints passed. The saved report retains the original full-run time and records the separate rebind explicitly. CI repeats the full checks on the committed revision.

This is sampled Chromium evidence. Physical touch, screen-reader hardware and a multi-browser matrix were not tested. Earlier roster/history gaps and source dates remain unchanged, as detailed in the [national publication review](2026-10-23-national-expansion-publication.md).

## Publication evidence

This review is prepared before the focused commit. The exact pushed revision, CI result, Pages deployment and representative live-byte/browser checks are recorded by GitHub's commit/workflow history and the publication handover. A local passing check alone does not establish deployment.
