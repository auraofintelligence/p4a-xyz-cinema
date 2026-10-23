# National expansion publication review - 23 October 2026

Luke authorised publishing the recovered 17-18 October national expansion on 23 October. This release prepares the existing council, state/territory and federal map-and-page foundation across all eight jurisdictions. It preserves the deeper Victoria atlas and Redlands journey. No new grassroots Twinkles were created.

The original dirty checkout remains intact. Publication uses an isolated checkout based on the verified remote `main` commit `6e924cc26a3c2e1fa50ec51e4b6a9874a2f6ab59`. The later GitHub Wiki links, wiki documentation and Oceania rebranding are excluded from this focused commit. No credentials, repository access settings, custom domain or Pages configuration were changed.

## Scope

| Item | Count |
| --- | ---: |
| Dedicated place pages | 2,080 |
| National/jurisdiction/institution directories | 33 |
| Delivered map layers | 49 |
| All public HTML routes, including existing work | 2,290 |
| Council/local area records | 1,479 |
| State/territory area records | 442 |
| Federal area records | 159 |
| Representative context records | 5,247 |
| Historical contestant records | 18,314 |

These are records, not unique people. Dated public roles, previous contestants, real institutions, historical/current/future boundary editions and unknown dates retain their distinctions. Source observations retain their original dates; publication does not make the rosters current as of 23 October.

## Publication fixes

The initial public tree exceeded GitHub Pages' [1 GB published-site limit](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits). Seven optional expanded GeoJSON duplicates totalled 348,541,152 bytes. Their gzip companions were decompressed and compared byte-for-byte before the expanded duplicates were excluded. Every coordinate, ring, feature and attribution remains in the exact compressed originals. Expanded originals remain in the original local checkout. Canonical delivery paths and generated maps use the compressed files; no geography or political records were simplified or removed.

The generator keeps optional expanded copies below 25 MiB, and the council adapter preserves the retained gzip delivery paths on future merges. The national validator now records the actual Brisbane validation date rather than a fixed 17 October report date. These are delivery/evidence fixes; source dates remain separate.

## Verification

Fresh national validation passed 1,001,438 assertions over all 2,113 generated pages, 2,112 map configurations, 49 lossless gzip round trips and 181,254 local references. It bound 3,051 public/source artifacts. Of the retained original source files, 204 available public files were hashed; 1,061 intentionally local-only research snapshots were absent from this public checkout and were recorded separately. This does not claim a fresh review of every official source.

Discovery passed for all 2,290 public routes with the licence unchanged. Existing Redlands and Victoria geometry, representation, Census/results, source-hash and navigation checks passed. National geometry, compressed-loader and clock checks passed, including holes, multipart geometry, selection/history behavior, postal deadlines, daylight saving and unknown dates. The final national rebuild, including the canonical gzip delivery paths, repeated with zero changes. The final generated pages received a fresh full validation.

The staged public tree passed the conservative 1,000,000,000-byte size gate and credential-signature/path review at approximately 973 MB. Exact raw Git blob bytes match all 2,223 required national/browser evidence paths. Forty-two incidental line-ending-only changes outside that evidence were excluded; the original source checkout is unchanged.

The [browser record](../../content/places/qa/browser-review.json) contains five actual scenarios across six HTML paths: desktop and 390/680-pixel directory layouts, five Index themes and nine Start ideas, search/no-results/clear/Escape, the eight-portal Australia footer, NSW council search/select/Open, current Ngadjuri boundaries with separate historical edition, and Perth federal map controls with separate Senate context. No horizontal overflow was observed in the measured narrow layouts. This is sampled Chromium evidence, not exhaustive per-place, physical-touch, screen-reader or multi-browser certification.

The [final contract report](../../content/places/qa/contract-validation.json) passed all 2,081 registered contracts with zero failures at `2026-10-23T11:49:38+10:00`, taking 546.031 seconds. The earlier aggregate found only two stale shared-navigation pins in the legacy Redlands contract. After the actual affected browser review, those pins were corrected and the complete final run passed. Structural contracts do not establish complete political source coverage or complete local civic journeys.

## Remaining gaps

The [17 October resumed report](2026-10-17-national-expansion-resumed.md) and scoped reports retain the detailed gaps. Fresh checks count 334 council/local records without individual current-office records, 291 without individual historical contestants, and 115 without event records. State coverage has one area without an individual current-office record and seven historical events without individual contestants. Partial council rosters/ballots, NSW upper-house seat-status evidence, SA transfer stages, WA numeric historical results and earlier Tasmanian ballots remain research tasks. No missing politician, candidate, result or date was invented.

Place-specific issues, motions, voting reasons, compatible statistics, cultural context, substantive proposals, participation and outcomes remain incomplete. New Twinkles remain for grassroots authorship. Unknown election dates stay unknown. Future dates were spot-checked against the linked official electoral sources before publication; this is not a blanket event/roster refresh.

## Publication state

This is the pre-push review record. The exact committed revision, remote push, Actions checks, Pages deployment and representative live-page verification are recorded by GitHub's commit/workflow history and the publication handover. Do not infer deployment success from these local checks.
