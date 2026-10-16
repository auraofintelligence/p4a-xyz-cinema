# Agent instructions for P4A

Updated 17 October 2026, Australia/Brisbane. Page and rule changes are recorded in `content/history/civic-page-review-register-2026-10-17.json`; keep the relevant page/rule version and update date reviewable when changing this work.

Read `README.md`, `LOCALISE_WITH_AN_AGENT.md` and the current user's instructions before changing this repository. Preserve unrelated work. Edit reviewed content before regenerating affected pages; a build must not silently advance source dates.

## Civic places

Before creating or changing a council, council division, state electorate or federal electorate journey, read `docs/agents/local-place-pattern.md` and the separate guide for the requested level:

- Councils and their divisions: `docs/agents/council-journey-rules.md`.
- State and territory electorates: `docs/agents/state-electorate-journey-rules.md`.
- Federal electorates: `docs/agents/federal-electorate-journey-rules.md`.

Read `docs/agents/existing-place-coverage.md` before starting a new implementation. Reuse existing maps, reviewed data and generators; identify the missing journey instead of replacing working features. Victoria has an existing electorate atlas; Redlands is the fuller local journey example.

The repeated interaction is map -> search or select -> inspect -> open. Use exact attributed official geometry on Canvas with a registered raster geographic base where available. No new SVG maps or guessed boundaries. Provide readable text navigation as well. Each overview has one purposeful interactive map; historical map copies belong with sources. Keep water distinguishable from administrative marine boundaries, roads subdued by default, and narrow-screen controls readable without overlap or page overflow.

Follow the actual Twinkle rules at `content/rooms/twinkle.html#format`: one ordinary scene, one everyday gripe, one spoken breath; aim humour at machinery, with the quiet format where care is needed. Show the short seed before the serious context. Link evidence, policy rooms and meaningful participation underneath. A policy concept alone is a room, not a Twinkle.

Carry three accounts together: what it cost, what was given freely, what changed. Preserve the human's purpose, meaningful choices, lyric meanings where relevant, source dates and uncertainty. A freely given verified hour is counted once; there is no fixed dollar conversion. Static examples must not claim to be operating databases or civic authorities.

Do not assume Queensland election dates, mayoral rules, division structures or time zones apply elsewhere. Distinguish current office, announced candidacy and accepted nomination. Preserve private reflection and do not infer a person's candidacy. Voting records need the exact motion; a stated reason requires an attributable source and an inferred explanation must be labelled.

## Completion

Use `docs/agents/council-build-acceptance.md` and `docs/agents/council-expansion-report-template.md` for every place level. Create a place-specific acceptance manifest from `content/local/council-pattern-contract.json`, then run `python tools/verify-council-pattern.py --manifest <manifest-path>`. Run the applicable existing validators as well. A structural pass cannot replace source, browser, accessibility or editorial review. Report missing evidence and partial completion accurately; do not call a build complete while required checks or parts of the journey are missing.

Register each reviewed manifest under `content/` with a unique name ending in `-pattern-contract.json`. `python tools/verify-place-contracts.py` and the GitHub Actions workflow discover it automatically; never register a copied manifest with unreviewed source dates or passing evidence from another place.

Keep council, state and federal coverage reports and rules separate. New institutions or places require their own sourced data and adapters; do not mass-copy Redlands names, counts, laws, dates, councillors or issue prevalence.

## GitHub preparation

Keep human and machine discovery together: `python tools/build-human-site-map.py` rebuilds the readable sitemap, actual public-page inventory, `sitemap.xml`, `robots.txt` and `llms.txt`. Run `python tools/verify-discovery.py` after navigation changes. Use supported implementation dates for sitemap updates; never substitute the build date for unknown content dates. Preserve the Strange But True licence and third-party rights. Crawl discovery grants no extra reuse or training permission. Follow `docs/discovery-and-rights.md` when changing crawler policy.

Keep public source and source licences. Exclude browser profiles, credentials, private notes, dependencies, caches and local upload output. Never stage the entire dirty checkout without reviewing the intended scope. `scripts/prepare-github-upload.py` prepares a checked, explicit public-source snapshot without changing the Git index, committing or pushing. Follow `docs/github-upload.md` for this repository. Upload or publication follows the user's requested scope; preparation alone does not imply publication.
