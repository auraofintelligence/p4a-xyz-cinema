# Focused Victorian candidate refresh, 1 November 2026

## Scope and evidence

This is a bounded candidate update, not a fresh review of every Victorian candidate, officeholder or legal requirement. The baseline remains checked 2 October; each new record is checked 1 November. No nomination is asserted before the VEC process opens.

- The [Australian Democrats' official 27 October announcement](https://vic.democrats.org.au/posts/meet-our-candidates-for-the-2026-victorian-election/) supplies twelve Council candidates in six regions. No ticket order or ballot label is inferred.
- The [Liberal-authorised Our Plan directory](https://ourplan.au/find-your-candidate/) explicitly lists Toby Wooldridge for Croydon. Its older footer date is not used as an announcement date.
- [ABC's Collins report](https://www.abc.net.au/news/2026-11-01/one-nation-melbourne-candidate-matthew-collins-steps-down/107333132) and [Croydon report](https://www.abc.net.au/news/2026-10-13/croydon-liberal-candidate-grant-hutchinson-replaced/107260434) flag discrepancies with older announcements. The records retain original evidence and check dates, with explicit current-status uncertainty. An explicit primary withdrawal notice was not retrieved; Liberal profile/API access was unsuccessful. These are not newly confirmed current candidacies or verified VEC withdrawals.

Canonical data: `content/elections/vic-2026.json`; per-party research: `vic-candidate-research.json`. The recoverable full prior record is `content/archive/vic-candidates-before-2026-11-01.json`. Generated dependants are the candidate directory and `vic-election-data.js` / `vic-people.js`. There are 495 sourced records (408 Assembly, 87 Council, 15 affiliations), including earlier disputed announcements, not 495 verified current candidacies. No change to current MPs, polling dates, legal/process facts, advocacy, boundaries, or Redland's removed invented Twinkles.

## Delivery and checks

Changed data-script cache references prevent old browser data from supplying stale filters. Atlas candidate context now directs visitors to each record's source date instead of implying every record was checked on 2 October. Existing layout and licence are unchanged. Review-register and sitemap dates reflect these two affected pages only.

Candidate assertions, duplicate counts, generated-data parity, reproducible candidate/map builds, JavaScript syntax, original archive parity and focused diff checks pass. The historical candidate-terminal test's PowerShell portal-rebuild step could not run because `pwsh` is unavailable; the unchanged portal is instead covered by the existing source/generated parity validator. This is not represented as an unmodified full historical-script pass.

Cloud HTTP browser checks cover party filtering (12 Democrats), search (Toby Wooldridge and Matthew Collins), discrepancy disclosure, reload persistence, the candidate-to-atlas link and Back restoration. Narrow effective-width visual review uses browser zoom, not a physical-device claim. Full structural, clock, link, contract and discovery checks are recorded externally for this run. GitHub history, exact-commit CI/Pages and live verification establish publication; a local build alone does not.
