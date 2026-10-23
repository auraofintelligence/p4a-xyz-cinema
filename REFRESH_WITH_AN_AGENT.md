# Refresh Election Data With An Agent

Paste this prompt into a capable coding agent working in this repo to check
and refresh an individual council, ward, state/territory or federal event,
member/profile, previous contest or countdown. Follow the
[fractal update guide](docs/agents/fractal-election-updates.md), including its
sitemap and link procedure. A no-change check updates only the refresh log.

---

You are refreshing election data for the P4A public workbench.

1. Read `AGENTS.md`, `docs/agents/fractal-election-updates.md` and
   `content/refresh-watchlist.md`, then the guide for the actual place level.
2. Scope: the place, event or jurisdictions the operator named. Resolve a
   named by-election to its area/event IDs; follow only affected dependencies.
   Use all eight jurisdictions only for an explicitly national check.
   If no target can be inferred, clarify the scope before a broad refresh.
3. Find the real canonical place/event/people/contestant records and official
   source URLs. Check the current election stage, membership and required
   timetable/profile/result sources; preserve their distinct dates and editions.
4. If nothing changed, append one scoped "no change" entry to
   `content/refresh-log.md`. Leave data and research dates unchanged.
5. For verified changes, edit canonical records first, then use the actual
   scoped adapter and review all outputs, including shared files. Keep current
   office, previous contestants and future candidacy separate. Update affected
   countdowns, summaries, public profile links and navigation/discovery; validate
   using the guide's applicable checks and log the evidence and remaining gaps.
6. Never guess a winner or poll date. Verified vacancy, poll-held or counting
   status can change while a winner remains unknown. Record inaccessible or
   conflicting evidence as "needs follow-up". Create no new Twinkles. Commit
   or publish only within the operator's existing authorisation; report the
   exact delivery state.

---

The same pattern, one level up: the sibling repo `p4a-oceania-cinema` keeps
regional national-election clocks in `assets/oceania-pulse-data.js` with its
own research stamp and follow-up flags — refresh that in its own repo run.


## Victoria atlas and candidate scope

For the implemented Victoria workbench, also read `content/electorates/vic-implementation.md` and the source-use register. Candidate records live in `content/elections/vic-2026.json`; preserve checked dates, null announcement dates, conflicts and separate historical events. Party announcements, preselection and accepted VEC nomination are distinct. Never infer recontesting from office-holding. Update the reviewed source, run the scoped state/election/map generators as needed, then verify source joins, counts, links, desktop/mobile and file/HTTP behaviour. Other jurisdictions and sibling repositories require their own scope. The homepage countdown updates automatically and does not refresh the underlying political data.
