# Queensland

```json state-data
{
  "order": 3,
  "slug": "qld",
  "name": "Queensland",
  "shortName": "QLD",
  "capital": "Brisbane",
  "stateType": "State",
  "researchRun": "2026-05-08",
  "researchTimezone": "Australia/Brisbane",
  "researchStatus": "Current members were checked against the Queensland Parliament member list. Stafford is an active state by-election.",
  "government": {
    "leaderTitle": "Premier",
    "leader": "David Crisafulli",
    "party": "Liberal National Party",
    "arrangement": "Majority government",
    "inPowerSince": "2024-10-28",
    "note": "Queensland has a single chamber. Stafford is vacant until the scheduled by-election is completed."
  },
  "elections": [
    {
      "label": "2028 Queensland State election",
      "date": "2028-10-28T08:00:00+10:00",
      "kind": "State general election",
      "scope": "general",
      "status": "Scheduled by fixed-term cycle",
      "note": "Queensland state elections are held on the last Saturday in October every four years.",
      "source": "https://www.ecq.qld.gov.au/elections/election-events",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2024-10-26T08:00:00+10:00",
        "daysSinceLabel": "Previous Queensland State general election polling day",
        "daysSinceSource": "https://www.ecq.qld.gov.au/elections/election-events",
        "archiveDaysSince": true,
        "cycleKey": "qld-2028-general",
        "archiveWithCycle": "next-higher-order-cycle-after-qld-2028-general",
        "archiveNote": "When this election becomes historical, keep days-since visible in the current cycle, then archive it with the next higher-order election cycle."
      }
    },
    {
      "label": "Stafford State by-election",
      "date": "2026-05-16T08:00:00+10:00",
      "kind": "State by-election",
      "scope": "by-election",
      "status": "Scheduled",
      "note": "Polling day is Saturday 16 May 2026, with early voting from 5 May to 15 May.",
      "source": "https://www.ecq.qld.gov.au/elections/election-events/stafford-state-by-election",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2024-10-26T08:00:00+10:00",
        "daysSinceLabel": "Previous Queensland State general election polling day",
        "daysSinceSource": "https://www.ecq.qld.gov.au/elections/election-events",
        "archiveDaysSince": true,
        "cycleKey": "qld-2026-by-election",
        "archiveWithCycle": "qld-2028-general archive",
        "archiveNote": "Keep days-since visible while this event belongs to the current local cycle, then archive it with the next state or territory general election cycle."
      }
    }
  ],
  "chambers": [
    {
      "name": "Legislative Assembly",
      "type": "Unicameral parliament",
      "seats": 93,
      "majority": 47,
      "note": "Queensland has no upper house. Stafford is listed as vacant pending the by-election.",
      "source": "https://www.parliament.qld.gov.au/Members/Current-Members/Member-List",
      "composition": [
        {
          "party": "Liberal National Party",
          "short": "LNP",
          "seats": 53
        },
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 35
        },
        {
          "party": "Katter's Australian Party",
          "short": "KAP",
          "seats": 2
        },
        {
          "party": "Queensland Greens",
          "short": "GRN",
          "seats": 1
        },
        {
          "party": "Sandy Bolton",
          "short": "NOOSA",
          "seats": 1,
          "memberSource": "https://www.parliament.qld.gov.au/Members/Current-Members/Member-List",
          "members": [
            {
              "name": "Sandra (Sandy) Bolton",
              "seat": "Noosa"
            }
          ]
        },
        {
          "party": "Vacant",
          "short": "VAC",
          "seats": 1
        }
      ]
    }
  ],
  "strategyNotes": [
    "Queensland is the home-base page for the Brisbane 2032 runway.",
    "The unicameral system makes local electorate trust and member accountability especially important.",
    "Stafford is the live by-election timer and should be refreshed first after polling closes."
  ],
  "sources": [
    {
      "label": "Queensland Parliament current member list",
      "url": "https://www.parliament.qld.gov.au/Members/Current-Members/Member-List"
    },
    {
      "label": "ECQ Stafford State by-election",
      "url": "https://www.ecq.qld.gov.au/elections/election-events/stafford-state-by-election"
    },
    {
      "label": "ECQ election events",
      "url": "https://www.ecq.qld.gov.au/elections/election-events"
    },
    {
      "label": "ECQ state election participant dates",
      "url": "https://www.ecq.qld.gov.au/election-participants/state-election-participants"
    }
  ]
}
```
