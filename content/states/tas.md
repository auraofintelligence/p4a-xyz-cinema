# Tasmania

```json state-data
{
  "order": 6,
  "slug": "tas",
  "name": "Tasmania",
  "shortName": "TAS",
  "capital": "Hobart",
  "stateType": "State",
  "researchRun": "2026-05-08",
  "researchTimezone": "Australia/Brisbane",
  "researchStatus": "House members were checked against the 2025 TEC elected-candidates list. Legislative Council member names now include Clare Glade-Wright after the 7 May 2026 Huon result; Rosevears remains to be confirmed in final declarations.",
  "government": {
    "leaderTitle": "Premier",
    "leader": "Jeremy Rockliff",
    "party": "Liberal Party",
    "arrangement": "Minority government",
    "inPowerSince": "2022-04-08",
    "note": "The 2025 House of Assembly election returned a hung parliament."
  },
  "elections": [
    {
      "label": "Next Tasmanian House of Assembly election",
      "date": "2029-07-19T08:00:00+10:00",
      "kind": "State general election",
      "scope": "general",
      "status": "Last-possible guide, not fixed",
      "note": "Tasmanian House elections are held at least every four years, but the date is not fixed and can be earlier.",
      "source": "https://www.tec.tas.gov.au/house-of-assembly/",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2025-07-19T08:00:00+10:00",
        "daysSinceLabel": "Previous Tasmanian House of Assembly general election polling day",
        "daysSinceSource": "https://www.tec.tas.gov.au/House_of_Assembly_Elections/",
        "archiveDaysSince": true,
        "cycleKey": "tas-2029-general",
        "archiveWithCycle": "next-higher-order-cycle-after-tas-2029-general",
        "archiveNote": "When this election becomes historical, keep days-since visible in the current cycle, then archive it with the next higher-order election cycle."
      }
    },
    {
      "label": "2027 Legislative Council periodic elections",
      "date": "2027-05-01T08:00:00+10:00",
      "kind": "Legislative Council periodic elections",
      "scope": "upper-house",
      "status": "Expected cycle",
      "note": "Derwent, Mersey and Windermere are due in 2027 according to the TEC candidate handbook cycle table.",
      "source": "https://www.tec.tas.gov.au/legislative-council/elections-2026/downloads/2026-Legislative-Council-Candidate-Handbook.pdf",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2026-05-02T08:00:00+10:00",
        "daysSinceLabel": "Most recent Tasmanian Legislative Council periodic election polling day",
        "daysSinceSource": "https://www.tec.tas.gov.au/legislative-council/elections-2026/results/huon/index.html",
        "archiveDaysSince": true,
        "cycleKey": "tas-2027-upper-house",
        "archiveWithCycle": "tas-2029-general archive",
        "archiveNote": "Keep days-since visible while this event belongs to the current local cycle, then archive it with the next state or territory general election cycle."
      }
    },
    {
      "label": "2026 Huon and Rosevears Legislative Council elections",
      "date": "2026-05-02T08:00:00+10:00",
      "kind": "Legislative Council periodic elections",
      "scope": "recent",
      "status": "Counting and declaration process active during research run",
      "note": "Huon had an unassailable lead update on 7 May; Rosevears counting had adjourned on 7 May.",
      "source": "https://www.tec.tas.gov.au/legislative-council/elections-2026/results/huon/index.html",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2026-05-02T08:00:00+10:00",
        "daysSinceLabel": "2026 Huon and Rosevears Legislative Council polling day",
        "daysSinceSource": "https://www.tec.tas.gov.au/legislative-council/elections-2026/results/huon/index.html",
        "archiveDaysSince": true,
        "cycleKey": "tas-2026-recent",
        "archiveWithCycle": "tas-2029-general archive",
        "archiveNote": "Keep days-since visible while this event belongs to the current local cycle, then archive it with the next state or territory general election cycle."
      }
    }
  ],
  "chambers": [
    {
      "name": "House of Assembly",
      "type": "Lower house",
      "seats": 35,
      "majority": 18,
      "note": "Final elected-candidate party labels from the 2025 state election.",
      "source": "https://www.tec.tas.gov.au/house-of-assembly/elections-2025/candidates-elected.html",
      "composition": [
        {
          "party": "Liberal Party",
          "short": "LIB",
          "seats": 14
        },
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 10
        },
        {
          "party": "Tasmanian Greens",
          "short": "GRN",
          "seats": 5
        },
        {
          "party": "George Razay, Craig Garland, Kristie Johnston, Peter George and David O'Byrne",
          "short": "5 MHAs",
          "seats": 5,
          "memberSource": "https://www.tec.tas.gov.au/house-of-assembly/elections-2025/candidates-elected.html",
          "members": [
            {
              "name": "George Razay",
              "seat": "Bass"
            },
            {
              "name": "Craig Garland",
              "seat": "Braddon"
            },
            {
              "name": "Kristie Johnston",
              "seat": "Clark"
            },
            {
              "name": "Peter George",
              "seat": "Franklin"
            },
            {
              "name": "David O'Byrne",
              "seat": "Franklin"
            }
          ]
        },
        {
          "party": "Shooters, Fishers, Farmers TAS",
          "short": "SFF",
          "seats": 1
        }
      ]
    },
    {
      "name": "Legislative Council",
      "type": "Upper house",
      "seats": 15,
      "majority": 8,
      "note": "Official October 2025 member list has been updated with the 7 May 2026 Huon result: Clare Glade-Wright replaces Dean Harriss. Rosevears final declaration should still be refreshed.",
      "source": "https://www.parliament.tas.gov.au/__data/assets/pdf_file/0031/97591/Legislative-Council-Members-List-13-October-2025.pdf",
      "composition": [
        {
          "party": "Rosemary Armitage plus seven named MLCs",
          "short": "8 MLCs",
          "seats": 8,
          "memberSource": "https://www.tec.tas.gov.au/legislative-council/elections-2026/results/huon/index.html",
          "members": [
            {
              "name": "Rosemary Armitage",
              "seat": "Launceston"
            },
            {
              "name": "Ruth Forrest",
              "seat": "Murchison"
            },
            {
              "name": "Mike Gaffney",
              "seat": "Mersey"
            },
            {
              "name": "Clare Glade-Wright",
              "seat": "Huon"
            },
            {
              "name": "Casey Hiscutt",
              "seat": "Montgomery"
            },
            {
              "name": "Tania Rattray",
              "seat": "McIntyre"
            },
            {
              "name": "Bec Thomas",
              "seat": "Elwick"
            },
            {
              "name": "Meg Webb",
              "seat": "Nelson"
            }
          ]
        },
        {
          "party": "Liberal Party",
          "short": "LIB",
          "seats": 3
        },
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 3
        },
        {
          "party": "Tasmanian Greens",
          "short": "GRN",
          "seats": 1
        }
      ]
    }
  ],
  "strategyNotes": [
    "Tasmania is the best stress test for proportional, minority and crossbench politics.",
    "The upper house is deliberately crossbench-heavy and should not be framed like a mainland party chamber.",
    "The House election date is a guide only; future agents should refresh it before any public campaign claim."
  ],
  "sources": [
    {
      "label": "TEC 2025 House of Assembly elected candidates",
      "url": "https://www.tec.tas.gov.au/house-of-assembly/elections-2025/candidates-elected.html"
    },
    {
      "label": "TEC House of Assembly elections explainer",
      "url": "https://www.tec.tas.gov.au/house-of-assembly/"
    },
    {
      "label": "Tasmanian Legislative Council member list",
      "url": "https://www.parliament.tas.gov.au/__data/assets/pdf_file/0031/97591/Legislative-Council-Members-List-13-October-2025.pdf"
    },
    {
      "label": "TEC Huon 2026 results",
      "url": "https://www.tec.tas.gov.au/legislative-council/elections-2026/results/huon/index.html"
    },
    {
      "label": "TEC Rosevears 2026 results",
      "url": "https://www.tec.tas.gov.au/legislative-council/elections-2026/results/rosevears/index.html"
    },
    {
      "label": "ABC Huon crossbench result report",
      "url": "https://www.abc.net.au/news/2026-05-07/clare-glade-wright-huon-election-result/106654874"
    }
  ]
}
```
