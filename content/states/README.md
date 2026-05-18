# P4A State Portal Data

This folder is the source layer for the state and territory portal.

Each jurisdiction has one markdown file. Inside each file is a fenced block named `json state-data`. Future agents can use those facts for approved actions. Edits happen through permissioned review, then the build can run:

```powershell
.\tools\build-state-sites.ps1
```

That regenerates:

- `assets/state-data.js`
- `pages/states.html`
- `states/<state-or-territory>/index.html`

Keep the `researchRun` field current whenever data is checked. If a count is provisional or a recent by-election is not fully declared, say so plainly in `researchStatus` or the relevant election note.

Every item in `elections` also carries a `dayMetrics` object:

- `displayDaysUntil`: show the live days-until number on the timer card.
- `displayDaysSince`: show the live days-since number on the timer card.
- `daysSinceDate`: the previous polling day or held event date used for the days-since number.
- `daysSinceLabel`: a plain-English label for that reference date.
- `daysSinceSource`: the source used to verify that reference date.
- `archiveDaysSince`: keep the days-since value as part of the historical cycle record.
- `cycleKey`: a stable local key for the election or by-election.
- `archiveWithCycle`: the higher-order cycle that should receive the days-since record later.
- `archiveNote`: plain-English instructions for future agents.

For by-elections, archive days-since with the next state or territory general election cycle unless a future political-design pass says otherwise.

In each chamber `composition` row, use party names for parties and person names for non-party crossbenchers. If a row groups multiple named members, include:

- `members`: an array of `{ "name": "...", "seat": "..." }` entries.
- `memberSource`: the source used to verify those names.

Do not leave a row labelled only as `Independent` or `Independents`; name the people directly and let the seat count remain the numeric summary.
