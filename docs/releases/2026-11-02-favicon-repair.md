# Favicon repair, 2 November 2026

The Redlands local shell omitted its icon link. The 18 local journey pages and Queensland councils index now declare the existing SVG icon using the correct depth. The separate national Redland election overview already declared it and is unchanged.

The 98 room source mirrors used a public-page-relative icon path that failed when opened under content/rooms. The source mirrors now use ../../assets/favicon.svg; the room publisher rebases only that href to the existing ../assets/favicon.svg used by public pages. Their working public copies remain unchanged. The human sitemap source and public page share /assets/favicon.svg to preserve their required byte-for-byte mirror contract. No favicon artwork, styles, page copy, civic facts, election data or licence changed. Existing editorial/source dates remain unchanged by this head-only maintenance.

A focused checker covers every public inventory route and the room source mirrors, verifies local icon resolution and SVG syntax, and rejects missing or broken references. It runs in CI.

The existing Victoria link checker now resolves root-relative URLs against the site root, rather than the operating system root; it still verifies the target exists. Its previous resolution incorrectly rejected the valid shared sitemap icon path. No check is skipped or relaxed.
