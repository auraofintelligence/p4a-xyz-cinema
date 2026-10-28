# Capricornia: announced retirement at the next election

Checked 29 October 2026, Australia/Brisbane (28 October UTC). Scope: Michelle Landry's current federal membership and announcement that she will not recontest Capricornia at the next federal election. This is a future retirement announcement, with continued service until that election. No immediate vacancy, by-election, successor, nomination or new countdown is created.

The [official announcement](https://michellelandry.com.au/michelle-landry-mp-stepping-down-at-next-election/) is dated 23 October 2026. Parliament's existing [current Handbook API](https://handbookapi.aph.gov.au/api/individuals?$filter=InCurrentParliament%20eq%20'True') returned HTTP 200 and lists PHID 249764, Michelle Landry, Capricornia, The Nationals, `InCurrentParliament: True`. Only that membership was reviewed. Generated end-date values in service-history arrays are not interpreted as a resignation date. The [AEC's final 2025 result](https://results.aec.gov.au/31496/Website/HouseDivisionPage-31496-157.htm) remains unchanged; the [AEC timing explanation](https://www.aec.gov.au/learn/election-timetable.htm) does not announce the next polling date.

The direct APH profile fetch was unavailable. A direct archival download of the announcement failed because of an expired TLS certificate; the announcement was read through web retrieval. No certificate or access restriction was bypassed, and no personal or external browser was used. The working original Handbook response remains in the ignored local research cache; only minimal public membership facts and source fingerprints are published.

Canonical data is `content/places/federal.json`, place `federal-house-157`. The existing [Capricornia page](https://p4a.xyz/states/qld/federal/capricornia/index.html#people) uses its established Current representation card and adjacent official website link; the source list names the dated announcement. `retirementAnnouncement` preserves its source/date and future effective stage separately from current office and election events. `content/places/sources/capricornia-retirement-2026-10-29.json` retains the minimal verification facts. The preceding place record is retained in `content/places/history/capricornia-before-retirement-2026-10-29.json`.

The scoped build command is:

```text
python -B tools/build-national-places.py --place federal-house-157 --jurisdiction qld --scope federal
```

The shared renderer, CSS, scripts, boundaries, other place records, 2025 contestants and next-election event/date are unchanged. The check date applies to Capricornia's reviewed status, not every federal seat. Site review/discovery dates distinguish this update from the shared renderer's earlier implementation date.

Verification uses the existing national source/data/page validator, clock checks, link/fragment checks, scoped preservation checks, current evidence bindings and registered contracts. Under the user's requested repository/non-browser workflow, no new browser interaction or responsive-rendering review is claimed; existing renderer/browser evidence retains its actual scope and dates. Exact publication, CI/Pages and live-file outcomes must be confirmed separately.
