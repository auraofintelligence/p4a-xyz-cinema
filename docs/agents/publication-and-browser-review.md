# Publish first, review the live browser afterward

Version 1.0, 9 November 2026, Australia/Brisbane. This sequencing implements the requested workflow reset and supersedes older instructions that made browser acceptance a prerequisite for publication. It does not remove source, factual, data, clock, link, geometry, privacy, build or civic checks.

## Before publication

1. Verify actual changes against sources; preserve dates, candidate stages, history and declared gaps. Build affected dependants and run applicable non-browser validators.
2. Run `python -B tools/verify-national-places.py --source-hashes` to create current structural evidence when national inputs change. This is not new external research or browser evidence.
3. Run `python -B tools/build-national-contracts.py --publication` and `python -B tools/verify-place-contracts.py --publication`. These preserve structural snapshots, canonical identity pins, dates, routes, source/geometry checks and concurrent-edit guards. Only saved browser/renderer review evidence is deferred. Do not update browser fingerprints or PASS results without doing the review.
4. Run remaining applicable `.github/workflows/civic-place-checks.yml` checks, review the scoped diff and publish through an authorised route. Genuine data/build failures still require correction. Permissions and repository settings are unchanged; Pages remains independent of the read-only civic workflow.
5. Verify the exact remote commit, corresponding deployment and served changed files over HTTP. A pushed commit alone is not a live update.

## After confirmed live deployment

Use a cloud browser on live URLs for affected navigation, maps, direct links, clocks and responsive interactions. Do not request or control a personal computer. Record actual routes, viewport, results and limits against the deployed revision. If cloud browser access is unavailable, mark live browser verification outstanding; do not hold up publication or claim acceptance.

Default commands without `--publication` retain strict dated-review acceptance. After actual affected browser review, preserve prior evidence, record new evidence and current structural bindings, then run `python -B tools/build-national-contracts.py` and `python -B tools/verify-place-contracts.py`. These commands do not launch a browser. A strict failure from stale browser evidence means acceptance is outstanding, not that publication did not happen.

Report publication and browser acceptance separately. Structural PASS does not certify current external sources, full local journeys, editorial quality, accessibility or browser behavior. Fix observed live defects without fabricating passing evidence.
