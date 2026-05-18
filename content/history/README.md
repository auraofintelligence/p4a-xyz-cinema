# P4A state history data

These files are the source of truth for the generated state and territory history pages.

Each file contains one fenced block:

```json history-data
{ ... }
```

Authorised agents can use these JSON records for approved tasks. Any update to the records belongs in a permissioned review step, then the pages can be rebuilt with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\build-state-sites.ps1
```

## Editing rules

- Use Australian English.
- Update `researchRun`, `researchTimezone` and `researchStatus` whenever a research refresh is performed.
- Keep `sortYear` numeric. Use approximate years where needed so sorting still works.
- Use `level: "basic"` for the public timeline path and `level: "advanced"` for deeper constitutional, electoral or institutional history.
- Keep at least one source on every event.
- Prefer official parliament, electoral commission, government, archival, AIATSIS or national collection sources.
- Do not overwrite First Peoples history with colonial chronology. Colonial formation is not the beginning of governance.
