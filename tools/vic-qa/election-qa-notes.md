# Victoria election QA

Evidence snapshot: 2 October 2026. Election browser tests cover file and localhost HTTP at 1440px and 390px. Source data has 482 distinct records, 407 Assembly/75 Council and 14 affiliations. Announced/preselected records are distinct from formal nominations.

Run Python helpers from a writable working directory. They create local `qa/` evidence; screenshots are for local inspection only. Browser helpers expect a dedicated Chromium CDP browser on port 9227 and a read-only repository HTTP server at 127.0.0.1:8766. The file protocol fixture targets the current Aura2020 repository location; adapt it if relocated. Never attach these helpers to a personal browser. Terminal helper runs scoped generators, so use only when edits/builds are authorised.

`election-browser-report.json`: all filter options, all 96 area joins, local links, no-JS coverage, source conflicts and navigation. Zero repository runtime exceptions. Six errors explicitly naming managed `chrome-extension://` dynamic imports were classified separately, not hidden as application successes.

`election-visual-report.json`: latest mobile polish, visible keyboard focus, gold heading/link colours, no overflow and four-link footer. Local screenshots visually inspected.

`election-terminal-report.json`: exact counts and conflict destinations, source caveats, reproducible outputs, syntax/diff checks, unchanged project licence and Git HEAD/cached origin reference. No remote was contacted.
