# Civic journey upload preparation 17 October 2026

Prepared in the local `p4a-xyz-cinema` checkout, Australia/Brisbane. Publication state: no commit, push or deployment performed for this preparation.

## Delivered

- Root `AGENTS.md` entry instructions and separate council, state and federal electorate guides, with a shared civic journey contract, concrete acceptance requirements and a handover report template.
- A manifest-driven structural/source-integrity validator, tested against the Redlands reference and nine negative controls. A discovery runner and read-only GitHub Actions workflow find new registered place contracts automatically.
- An existing-coverage inventory distinguishing Victoria's 88 Assembly districts and eight Legislative Council regions from complete per-electorate deep journeys. Bowman remains contextual federal map material; no complete federal atlas was found in this checkout.
- A code/content comparison of Victoria and Redlands, with priorities and target files for transferring statistical sorting, traceable results, efficient exact geometry, human journeys, Twinkles and braided outcomes.
- A public-source packaging tool with an explicit path allowlist, per-file hashes, tracked-file completeness, archive readback and exclusion of local browser profiles. Existing public work, source licences, exact boundary bytes, CNAME and linked backend/document files are retained.

## Readiness repairs

The existing Victoria test exposed two punctuation differences between canonical state data and its generated browser record. Those two strings were aligned without changing political facts, dates or other states. A wrongly nested early-voting script path in the sitemap was corrected in both canonical room content and its public page. No electorate atlas was replaced or described as a new deep dive.

The general localisation prompt's SVG-map example now follows the actual no-SVG boundary/raster pattern. Nested raw GeoJSON is marked for byte preservation in Git. Local browser session/cache output is excluded from Git and the public-source bundle. `.nojekyll` accompanies the buildless static tree.

## Validation scope

The registered Redlands reference checks 20 entry/journey routes, 1,507 local references, four map placements, two original geometry layers, two geographic PNG bases, 43 connected records, 24 Twinkles, 18 indicators and ten dated councillor listings. Existing Redlands checks cover its 19 generated pages and unchanged geometry. Victoria's existing atlas/source-parity, result/Census and council checks are run separately. Election clock checks use fixed AEST boundary cases and synthetic early-voting dates, not a new published timetable.

The saved Redlands browser/picking evidence remains dated 17 October 2026. This documentation/packaging pass does not claim a new physical-device touch test, a live review of every external source, or a fresh nationwide political audit. New agent rules require affected source, browser and editorial review before completing future place builds. The prepared GitHub workflow has not run remotely until upload.

All listed local commands passed in this preparation. Nine in-memory negative controls confirmed that the generic validator rejects broken onward routes, duplicate maps, wrong source counts, undeclared comparison layers, checksum/date drift, invented early voting, broken record relationships and stale review evidence. A final read-only audit checked 177 public HTML pages and 7,236 local href/src references: no missing files, outside-root targets or case-only filename mismatches. External links and dynamic fragment behaviour were outside that file-path audit.

See `../github-upload.md` for commands and the snapshot manifest. The bundle is the complete current public source, including earlier uncommitted public changes, rather than a selective patch. No unrelated working changes or Git history have been reset.

## Page dates and human navigation follow-up

The explicit [page and rule register](2026-10-17-page-and-rule-register.md) lists all 19 new routes, documented work-start and first-verified-build dates, last implementation update, what changed and review triggers. It separately identifies existing entry pages that were modified. The public Sources & dates page renders the register at `#review-register`; the division directory's inherited 16 October start stamp was corrected to its actual 17 October addition. Source observation/check dates remain unchanged.

The human sitemap covers all 177 public routes once in its directory, with purpose groups, local journey order, numeric division links, search, separate council/state/federal coverage and a visible review-date route. The README now opens with a short route guide. Shared Index search and selected footer links expose Redlands divisions, Twinkles, people, outcomes and review dates. Sitemap ownership is consolidated in `tools/build-human-site-map.py`; both legacy sitemap builders delegate to it so later builds do not restore the file tree. Canonical and public sitemap copies, route coverage and repeat generation were checked.

Browser checks passed for sitemap search (including Division 5), no-results, clearing, shared Index search and its opening link to the dated register. Synthetic 390px/680px sitemap and 390px expanded register frames have zero page overflow and zero overlapping navigation controls. Evidence is `qa/redland-20261017/navigation-layout-results.json`. Updated scoped checks passed: 1,441 Redlands local references and 1,534 registered-contract references; the existing Victoria atlas check also passed after sitemap changes. These results extend, rather than redate, the earlier checks above. The public-source bundle is regenerated after these changes; publication state remains local/prepared.

## Search discovery and rights follow-up

Added root `robots.txt`, `sitemap.xml` and `llms.txt`, using the recent Aura Genesis repository examples. The sitemap and assistant guide cover the same 177 public HTML routes as the human directory. Only the 24 routes with explicit implementation dates receive sitemap `lastmod` values; no unknown dates or source observations are made freshly current. Search and OAI-SearchBot discovery remain available, with separate GPTBot training crawl opt-out and repeated source/QA exclusions for the named search group. Discovery grants no additional reuse or training permission; third-party rights remain separate. These cooperative signals do not enforce rights or guarantee indexing.

The licence file remains byte-identical locally and has no Git diff. The validator accepts only the original CRLF hash and Git's known LF equivalent, preventing an Ubuntu false failure without accepting changed licence text. The discovery check passed, both known byte variants were confirmed against Git, and an altered-licence control was rejected. The rebuilt inventory is checked against actual public HTML files, as well as human sitemap source/public parity, unique XML and guide coverage, supported dates and generator parity. The read-only GitHub workflow now includes this check. Local HTTP checks returned 200 with appropriate text/XML/HTML content types for all three discovery files and the human sitemap. Evidence: `qa/redland-20261017/discovery-results.json`.

The human sitemap builder regenerates the discovery files too; the upload allowlist includes them. README, agent entry rules and `docs/discovery-and-rights.md` explain maintenance, source examples and review triggers. The local preview server has the correct `.txt`/`.xml` types. No push, search-console submission, live policy change or deployment was performed.
