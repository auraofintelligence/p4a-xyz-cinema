# Sitemap byte portability correction - 23 October 2026

The initial national expansion commit `a3057c1` deployed successfully and all 18 sampled live paths matched its committed bytes. Its GitHub civic workflow passed the national and contract checks, then found that the readable sitemap's source and public copies differed in bytes on Linux.

The Windows generator wrote both copies with platform newline translation. Git preserves the public copy's exact reviewed bytes while normalizing the canonical content mirror, so the two files differed after checkout despite matching locally. The generator now writes the same explicit UTF-8 byte string to both paths. The correction changes newline delivery only; it changes no page text, political record, map coordinate, source observation or grassroots Twinkle scope.

Validation: regenerate the sitemap, run `python tools/verify-discovery.py`, compare the exact staged Git blobs for `pages/site-map.html` and `content/rooms/site-map.html`, and preserve all national/browser evidence fingerprints. The correction's CI and deployment outcomes are recorded in GitHub's subsequent commit/workflow history. The [national publication review](2026-10-23-national-expansion-publication.md) retains the full scope and remaining source/history/journey gaps.
