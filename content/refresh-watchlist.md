# Election Refresh Watchlist

This file is the trigger map for agents refreshing Australian election data
across the P4A site. Read this first; it tells you what to check, where the
truth lives, and exactly which files change. Designed to be token-lean: a
no-change run touches only `content/refresh-log.md`.

For an individual council, ward, state/territory or federal event, follow the
[fractal update guide](../docs/agents/fractal-election-updates.md), version 1.0,
17 October 2026. It defines scoped member/profile, previous-contestant and
countdown updates, canonical adapters, sitemap/navigation maintenance and checks.
The state files listed below are the state-summary adapter, not a universal
storage model for every council or federal event.

```json refresh-watchlist
{
  "purpose": "Detect and apply scoped council, state/territory and federal election, by-election, representation, contestant, public-profile and timetable changes; update only affected records and dependants.",
  "signals": [
    "A new by-election has been officially announced (add its separate event record and only supported countdown milestones)",
    "A scheduled by-election has been held (verify poll/count/declaration status; update result and composition only as supported)",
    "Seat composition changed for any reason (resignation, defection, recount, vacancy)",
    "Premier / Chief Minister or governing arrangement changed",
    "A general election date was set, moved or held",
    "A council/ward or federal event, replacement process, accepted nomination, public profile or historical contestant record changed",
    "An affected route, directory, source/profile link or discovery entry changed"
  ],
  "sourceOfTruthOrder": [
    "1. Resolve the target place/institution/chamber and event IDs; read its actual canonical files, local guide and dependency list.",
    "2. Edit canonical event, current-role, contestant/result and source records FIRST; keep historical events and boundary editions separate.",
    "3. For state-summary changes, content/states/<slug>.md is canonical; assets/state-data.js and affected state/parent HTML must remain in parity.",
    "4. Build the affected detail/map/profile views and parent summaries with their actual scoped adapters. Inspect shared outputs for unrelated changes.",
    "5. When routes/navigation change, update canonical templates and assets/site-nav.js as applicable, then rebuild and verify discovery using the fractal guide."
  ],
  "jurisdictions": [
    { "slug": "qld", "name": "Queensland" },
    { "slug": "nsw", "name": "New South Wales" },
    { "slug": "vic", "name": "Victoria" },
    { "slug": "wa",  "name": "Western Australia" },
    { "slug": "sa",  "name": "South Australia" },
    { "slug": "tas", "name": "Tasmania" },
    { "slug": "act", "name": "Australian Capital Territory" },
    { "slug": "nt",  "name": "Northern Territory" }
  ],
  "whereTheSourceUrlsLive": "Read the target's canonical source records and local guide. State-summary commission/parliament URLs live in content/states/<slug>.md sources[]; council, electorate, federal and event-specific records keep their own primary URLs. Do not assume the state source list covers every institution.",
  "checkMethod": [
    "Scope to the named place/event and affected dependants. Read its actual canonical records and official source URLs; use the state markdown when state summaries are affected.",
    "Check official notices, roster, timetable, nominations/ballot and results as applicable. Secondary reporting can identify a lead; preserve primary support for the published status.",
    "If nothing changed: append one scoped line to content/refresh-log.md and STOP. Do not bump research dates. Inaccessible or conflicting evidence is needs-follow-up, not no change.",
    "If something changed: verify the applicable institution/process and facts, then follow the recipe below and docs/agents/fractal-election-updates.md."
  ],
  "recipe": {
    "learnedFrom": "Stafford by-election update, 2026-07-14",
    "steps": [
      "Identify stable place/event IDs, boundary basis, actual canonical inputs, generated routes and dependent summaries. Preserve unrelated work and archive superseded facts using the existing history pattern.",
      "Edit canonical event/status/timetable, current office, historical contestants/results and public-profile links only as verified. Keep general elections and subsequent by-elections separate; published result measures must retain their actual meaning.",
      "Update state-summary JSON only when affected: event notes, sourced composition/leadership, source URLs and scoped check dates. A verified vacancy or count can change before a winner is declared.",
      "Run existing scoped generators from the target guide. The state -StateSlug adapter also writes shared assets/state-data.js and pages/states.html: inspect their complete diffs and preserve unrelated jurisdictions. Use narrow parity-checked source/output edits only where no safe generator exists.",
      "Ensure all countdown surfaces use the same supported event/date basis and local timezone. Separate ordinary, by-election and early/postal milestones; unknown dates get no exact countdown. Polling day alone does not establish a winner or officeholder.",
      "Update navigation/link dependencies. For route/directory changes follow the fractal guide's canonical navigation, sitemap build and discovery verification procedure; preserve working deep links and historical routes.",
      "Validate affected source joins, roster/contestant completeness, counts, dates, clock boundary states, links and delivered pages using actual existing tools. Research/source dates advance only for the facts actually checked; no unrelated date bumps.",
      "Append scoped evidence, actual validation, remaining gaps and delivery/publication state to content/refresh-log.md and relevant place history. Commit or publish only within existing operator authorisation."
    ]
  },
  "hardRules": [
    "Never invent a result or poll date. Verified vacancy, poll-held, counting and other supported facts may be updated while a winner remains unknown; record conflicting/inaccessible evidence as needs follow-up.",
    "Australian English in all copy.",
    "Edit canonical sources first; use actual scoped generators and inspect every shared output diff. Preserve unrelated places and dates; narrow manual parity repairs are for missing/unsafe adapters.",
    "Respect each file's existing line endings and .gitattributes; use whitespace-tolerant searches.",
    "Keep current officeholders, historical contestants and future candidate stages separate; retain verified public-profile links and event/boundary history.",
    "Create no new Twinkles in the current national expansion or routine election refresh; leave local authorship to grassroots implementation.",
    "The sibling Oceania pulse board (p4a-oceania-cinema/assets/oceania-pulse-data.js) follows the same ethic for national elections across the region; refresh it in its own repo with its own research stamp."
  ]
}
```

## Log

Every run appends to [refresh-log.md](refresh-log.md) — one line per jurisdiction checked, even when nothing changed. That log is the cheap path: most runs should end there.

## Victoria electorate atlas

Refresh `content/electorates/vic.md` and `content/states/vic.md` together after membership changes. Reconcile Assembly members plus vacancies to 88 and Council members to 40; join by official district/region codes. Check VEC boundary edition and retain original coordinate sequences, provenance and licence. Never overwrite historical result periods or Census observation years with a retrieval date. Verify nominations after they open; keep announced and formally nominated candidates separate. Archive prior state facts and changed observation periods before regeneration. Build with `pwsh -File tools/build-state-sites.ps1 -StateSlug vic -SkipHistory` then `python tools/build-vic-map.py`; validate the navigation and geometry tests.


## Victoria source-use triggers

Consult [source-use register](licences/vic-source-register.md) and [machine-readable conditions](licences/vic-source-register.json) if this personal/public non-commercial research workbench becomes an actual political party, commercial operation, fundraising tool or wider dataset distributor. Check source-specific exceptions; preserve the project licence and community cultural permissions.


- Victoria 2026 candidates: refresh all primary directories and campaign confirmations; preserve null announcement dates unless evidenced. Resolve the two AJP source conflicts with future primary updates; retain history separately. Expand unknown party/independent coverage without inferring withdrawal. Before/after 4–9 November, separately reconcile accepted VEC nominations and final ballot labels/order; do not promote an announcement automatically. Validate any changed registration, nomination, voting, donation or authorisation guidance against current VEC/legislation. Canonical source: `content/elections/vic-2026.json`; coverage/review records: `vic-candidate-research.json`.

- Homepage ticker: review `content/home-ticker.json` against its primary sources before changing factual wording. Archive superseded dated claims, keep jurisdiction labels, and run `python tools/build-home-ticker.py`. It is a reviewed issue feed, not automated news. Keep tax amounts out unless specifically sourced and dated. Check countdown election-day/post-election states, hover/focus pause, mobile controls, reduced motion and external-link semantics.

## Redland City local journey: added 16 October 2026

Read [the repeatable local-place pattern](../docs/agents/local-place-pattern.md) before maintaining or expanding the local journey. Current source order: `content/councils/redland.json` for reviewed local facts/maps and `content/local/redland-connections.json` for issue/system connections; then `python tools/build-redland.py` and `python tools/verify-redland.py`. Preserve the existing state source order for state facts. Local routes begin at `states/qld/councils/index.html` and drill into `states/qld/councils/redland/`. A build timestamp must not replace an observation, map edition or source-check date.

- Vacancy/election: check official council minutes, current applicable legislation and ECQ notices when a leave decision, absence, resignation, vacancy or poll is reported. These are different events. Keep any potential mayoral by-election conditional until verified; do not infer a candidate or promote speculation into a countdown.
- Representation/results: check ECQ/AEC and official representative sources after changes. Preserve historical results, election/boundary editions, primary/2CP/2PP distinctions and announcement versus accepted-nomination status. Candidate personal learning/Genesis material remains an optional voluntary branch within candidates.
- Geography/maps: check new commission boundary editions, redistributions and the terms of each map asset. Use attributed raster source maps for this local pattern, not new SVG drawings. Retain original map/file links and conversion notes. Do not estimate overlap percentages visually or equate cultural, service, statistical and electoral boundaries.
- Statistics: check new ABS releases/revisions and their exact geography/observation period. Retain old Census dates until comparable official releases are available. Estimated population and Census counts are separate measures; unknown values are not zero.
- Local issues/projects: check adopted budgets, annual reports, service notices, council decisions and responsible project bodies when their status changes. Distinguish proposal, allocation, commitment, delivery and observed result. A general system connection is not evidence of a dedicated or deployed local solution.
- Civic records: refresh original minutes/divisions/Hansard alongside public voting explanations. Preserve motion/stage/absence/recusal distinctions; stated reasons and interpretations remain labelled separately.
- Wider use/rights: reassess asset-specific terms when purpose, redistribution, fundraising or party/campaign status changes. General site licences may exclude maps. The project licence does not replace third-party rights.

Append every scoped check to `content/refresh-log.md`; place-specific changes also go to `content/history/redland.md`. Record no-change and needs-follow-up outcomes honestly. Check the full navigation route, direct arrivals, keyboard/mobile use, static content, map attribution, links and search after relevant changes. No refresh, commit, push, external message or publication is automatically authorised by this watchlist.

- Local countdown addition, 16 October 2026: canonical timing is `content/local/redland-election.json`. The hub and candidates page use the same rule-derived next ordinary election date, 25 March 2028, from the ECQ last-Saturday-in-March four-year rule, subject to regulation; ECQ election events checked 16 October 2026. Check for a changed regulation or official election notice before revising the date/status. Calendar timing is Queensland AEST to the start of the date, not poll opening. Source early-voting opening/closing dates and locations separately; keep dates null until an official notice. The conditional mayoral by-election retains a separate null date and no timer until officially supported. Verify before/on/after-date behaviour and show verification needed after the date rather than assuming results or a new cycle.
