# Storage cleanup, 6 November 2026

This focused change removes 120,900,048 bytes from the publishing branch without
changing any map geometry, map fallback, displayed image, video, page or political
record. It does not change hosting, the domain, HTTPS or access settings.

## Preserved source and evidence

The full pre-cleanup source is retained on the
[archive branch](https://github.com/auraofintelligence/p4a-xyz-cinema/tree/archive/p4a-full-source-before-cleanup-20261106),
at original commit `3bf2aac97eecf20377ce9cacde3a28627705eda5`. Git history is not
rewritten. The [exact manifest](2026-11-06-storage-cleanup.json) records paths,
byte counts and SHA-256 hashes for the archived copies.

- 107 QA screenshots have no retained content/runtime reference and are archived.
- 24 unused PNG/JPEG originals are archived. The existing WebP versions already
  used by the site stay unchanged; no new lossy conversion was performed.
- All 18 referenced QA images stay on the publishing branch with their reports.
- All 126 map assets, totalling 633,499,516 bytes, remain byte-for-byte unchanged,
  including raw GeoJSON, compressed delivery, offline/fallback formats and raster bases.
- Source/rights manifests, validators, current and historical civic records,
  contracts, active images and videos stay on the publishing branch.

Restore an original for editing or historical QA from the archive branch or the
original commit. Run the relevant source/image workflow and inspect references
before returning it to the publishing tree. Do not restore all archived files in
a bulk source upload: the complete historical source is intentionally larger than
the current deployment budget.

## Validation and capacity

The read-only full-tree audit identified these exact candidates before removal:
[audit run](https://github.com/auraofintelligence/p4a-xyz-cinema/actions/runs/42175243692).
The candidate scan retains named references in HTML, CSS, JavaScript, SVG, JSON,
Markdown and discovery files, including encoded paths. It is conservative and does
not replace the existing validators or actual browser review.

The original retained tree is 983,898,006 bytes before these small documentation
and size-check additions. `python -B scripts/check-site-size.py` reports the exact
current tracked size and fails at or above 1,000,000,000 bytes. Its separate GitHub
workflow is read-only. Like the existing Civic checks, it does not automatically
gate the independently configured branch-based Pages deployment.

The complete existing Civic checks must pass on the exact cleanup commit before
publication. The Pages run and post-publication live checks establish deployment;
this preparation record does not pre-claim either result.

The remaining margin is modest. Major membership, constitution-collaboration or
committee/inquiry expansion still needs an asset/data capacity plan. Private member
data must not be stored in this public static tree. This change adds no such features.
