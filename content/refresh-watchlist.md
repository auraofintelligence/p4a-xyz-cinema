# Election Refresh Watchlist

This file is the trigger map for agents refreshing Australian election data
across the P4A site. Read this first; it tells you what to check, where the
truth lives, and exactly which files change. Designed to be token-lean: a
no-change run touches only `content/refresh-log.md`.

```json refresh-watchlist
{
  "purpose": "Detect and apply changes to by-elections, seat composition, government leadership and election dates for each Australian state and territory.",
  "signals": [
    "A new by-election has been announced (add an elections[] entry + timer cards)",
    "A scheduled by-election has been held (apply the result: status, notes, composition, sources)",
    "Seat composition changed for any reason (resignation, defection, recount, vacancy)",
    "Premier / Chief Minister or governing arrangement changed",
    "A general election date was set, moved or held"
  ],
  "sourceOfTruthOrder": [
    "1. content/states/<slug>.md  (canonical JSON block — edit FIRST)",
    "2. assets/state-data.js      (mirror of the same JSON, wider indentation — keep in lockstep)",
    "3. states/<slug>/index.html  (summary panels, timer cards, chamber rows, notes, sources)",
    "4. states/<slug>/architecture/index.html and states/<slug>/constitution/index.html (researchStatus sentence + research date)",
    "5. pages/states.html         (the state's portal card em-text and its timer cards ONLY — never touch other states' blocks)"
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
  "whereTheSourceUrlsLive": "Each jurisdiction's canonical md carries its own electoral-commission and parliament member-list URLs in its sources[] array. Do not duplicate URLs here; read the state md.",
  "checkMethod": [
    "For the jurisdiction in scope, read ONLY content/states/<slug>.md (small file).",
    "Web-check: search '<state> by-election <current year>' and fetch the commission events URL from the md's sources[]. Compare against the md's elections[] and researchRun.",
    "If nothing changed: append one line to content/refresh-log.md and STOP for that state. Do not touch any other file, do not bump researchRun.",
    "If something changed: verify the fact against at least one official or expert source (commission results page, parliament member list, ABC/Antony Green), then follow the recipe below."
  ],
  "recipe": {
    "learnedFrom": "Stafford by-election update, 2026-07-14",
    "steps": [
      "Update the canonical md JSON: researchRun (today), researchStatus sentence, government.note if affected, the elections[] entry status + note (include winner, party, 2PP and swing), chambers[].composition seat numbers (remove/add Vacant rows as needed), strategyNotes if they referenced the pending event, and append result sources to sources[].",
      "Mirror the exact same changes into assets/state-data.js (same strings, wider indentation; whitespace-tolerant regex recommended). Run node --check afterwards.",
      "Rendered HTML: use grep to find the same sentences — they appear verbatim in states/<slug>/index.html, the two sub-pages and pages/states.html. Replace sentence-for-sentence. Chamber rows: update <span class=\"party-seats\">N</span> and the party-bar width percentage (seats/total, rounded); delete a Vacant <li class=\"party-row\"> block entirely if the vacancy is filled.",
      "Timer cards: the <p class=\"timer-status\"> inside the card whose data-election-label matches — 'Scheduled' becomes 'Held - <result>' — and the card's note paragraph gets the result sentence. The countdown flips to 'Held ... ago' automatically from data-election-date; do not edit the date unless the poll was moved.",
      "Research dates: bump the date ONLY in that state's files (md, states/<slug>/*.html). The national badge in pages/states.html and other states' researchRun stamps keep their own dates — they were not re-verified.",
      "Validate: canonical md JSON parses; composition seats sum to the chamber total; node --check assets/state-data.js; grep confirms no stale sentence remains.",
      "Append a dated entry to content/refresh-log.md describing what changed and the sources used.",
      "Commit with message 'Refresh <state> election data: <one-line summary>' and the standard Co-Authored-By trailer. Push only when the operator has asked for publishing."
    ]
  },
  "hardRules": [
    "Never invent a result. If sources conflict or a result is not yet declared, record 'needs follow-up' in the log and leave the site data untouched.",
    "Australian English in all copy.",
    "Sentence-level find-and-replace across layers; never regenerate whole files.",
    "Files in this repo use CRLF line endings — use whitespace-tolerant patterns.",
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
