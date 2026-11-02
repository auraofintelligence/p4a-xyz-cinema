# Site checks and publication records

This is the central index for P4A maintenance. It links to the records that hold the facts rather than replacing them.

## Whole-site review

The [2 November 2026 audit](../content/history/site-audits/2026-11-02.json) covers the complete public-page inventory and distinguishes structural/date checks from individual factual source checks. Its listed gaps are part of the result. A page appearing in the inventory does not mean every statement on it has been independently verified.

- [Public-page inventory](../content/site-page-inventory.json): every public HTML route.
- [Page and rule register](releases/2026-10-17-page-and-rule-register.md): dated implementation changes.
- [National place register](../content/history/national-place-review-register-2026-10-17.json): national place implementation records.
- [Scoped refresh history](../content/refresh-log.md): election and other targeted changes.
- [Publication evidence](../content/history/site-publications.json): verified commits and deployment runs.

## What each date means

| Date | Meaning |
| --- | --- |
| Work started / first verified build | Historical implementation milestones. |
| Page implementation updated | A recorded content or implementation change to that page, not a fresh check of all its facts. |
| Source checked | The stated source or claim was checked on that date. Its observation period and boundary edition remain separate. |
| Election or deadline date | The event itself, in its jurisdiction's timezone. An indicative legal cycle is not a confirmed timetable. |
| Validation / browser review | The stated technical or interaction checks were performed. This does not establish political, legal or medical truth. |
| Published revision | An exact remote commit with its deployment result and stated live checks. A prepared file or successful local build is not publication evidence. |

Small technical repairs, including favicon paths, can leave editorial/source dates unchanged. Their own maintenance records describe the change. Unknown dates stay unknown; file modification time and today's build date are not substitutes.

## Reporting a scoped update

Keep official evidence and changed facts in their existing canonical records. Add the reviewed scope, source-access gaps, actual checks and retained history to the relevant dated report and [refresh log](../content/refresh-log.md). Keep the page register and its rendered copies consistent.

Add an entry to the [maintenance index](../content/history/site-maintenance-index.json) linking that report; do not recopy all facts into this index. A nationwide election review remains election-specific, not a whole-site factual certification. An unchanged check does not renew unrelated page or source dates.

After publication, append the exact commit, successful deployment and verified live scope to [publication evidence](../content/history/site-publications.json). If publication is pending or blocked, record that state explicitly in the scoped report; do not replace the last verified published revision with local work.

The repository workflow runs checks on push, pull request or manual invocation. These records do not create a scheduled source-refresh job. Existing authorised election monitoring continues separately.
