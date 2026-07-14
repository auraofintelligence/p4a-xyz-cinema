# Refresh Election Data With An Agent

Paste this prompt into a capable coding agent working in this repo to check
and refresh Australian election data (by-elections, seat splits, leadership,
election dates) across the whole site. It is designed to conserve tokens: a
run where nothing has changed reads two small files per state and writes one
log line.

---

You are refreshing election data for the P4A public workbench.

1. Read `content/refresh-watchlist.md` in full. It defines the signals to
   check, the source-of-truth order, the exact update recipe and the hard
   rules. Follow it precisely.
2. Scope: the jurisdictions the operator named, or all eight if unspecified.
3. For each jurisdiction in scope, read only `content/states/<slug>.md`,
   then check the live sources listed in that file's `sources[]` array plus
   a web search for "<state> by-election <current year>".
4. If the site data still matches reality, append one "no change" line to
   `content/refresh-log.md` and move on. Touch nothing else.
5. If something changed, verify it against an official or expert source,
   then apply the watchlist recipe through every layer (canonical md →
   assets/state-data.js → rendered HTML), validate, log it, and commit.
6. Never invent or guess a result. Unclear or undeclared results are logged
   as "needs follow-up" and the site keeps saying what it currently says.

---

The same pattern, one level up: the sibling repo `p4a-oceania-cinema` keeps
regional national-election clocks in `assets/oceania-pulse-data.js` with its
own research stamp and follow-up flags — refresh that in its own repo run.
