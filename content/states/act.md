# Australian Capital Territory

```json state-data
{
  "order": 7,
  "slug": "act",
  "name": "Australian Capital Territory",
  "shortName": "ACT",
  "capital": "Canberra",
  "stateType": "Territory",
  "researchRun": "2026-05-08",
  "researchTimezone": "Australia/Brisbane",
  "researchStatus": "Current members, party breakdown and end-of-term date were checked against ACT Legislative Assembly and Elections ACT sources.",
  "government": {
    "leaderTitle": "Chief Minister",
    "leader": "Andrew Barr",
    "party": "Australian Labor Party",
    "arrangement": "Labor minority government with Greens support",
    "inPowerSince": "2014-12-11",
    "note": "The Assembly has 25 members and no upper house."
  },
  "elections": [
    {
      "label": "2028 ACT Legislative Assembly election",
      "date": "2028-10-21T08:00:00+11:00",
      "kind": "Territory general election",
      "scope": "general",
      "status": "Scheduled by fixed-term cycle",
      "note": "Current member terms end on 21 October 2028.",
      "source": "https://www.elections.act.gov.au/elections/our-electoral-system/current-members-of-the-legislative-assembly",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2024-10-19T08:00:00+11:00",
        "daysSinceLabel": "Previous ACT Legislative Assembly election polling day",
        "daysSinceSource": "https://www.elections.act.gov.au/__data/assets/pdf_file/0006/2900904/Election-Report-2024-.PDF",
        "archiveDaysSince": true,
        "cycleKey": "act-2028-general",
        "archiveWithCycle": "next-higher-order-cycle-after-act-2028-general",
        "archiveNote": "When this election becomes historical, keep days-since visible in the current cycle, then archive it with the next higher-order election cycle."
      }
    }
  ],
  "chambers": [
    {
      "name": "Legislative Assembly",
      "type": "Unicameral parliament",
      "seats": 25,
      "majority": 13,
      "note": "The ACT has five electorates, each returning five MLAs.",
      "source": "https://www.parliament.act.gov.au/members/current",
      "composition": [
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 10
        },
        {
          "party": "Canberra Liberals",
          "short": "LIB",
          "seats": 9
        },
        {
          "party": "ACT Greens",
          "short": "GRN",
          "seats": 4
        },
        {
          "party": "Fiona Carrick and Thomas Emerson",
          "short": "2 MLAs",
          "seats": 2,
          "memberSource": "https://www.parliament.act.gov.au/members/current",
          "members": [
            {
              "name": "Fiona Carrick",
              "seat": "Murrumbidgee"
            },
            {
              "name": "Thomas Emerson",
              "seat": "Kurrajong"
            }
          ]
        }
      ]
    }
  ],
  "strategyNotes": [
    "The ACT is the simplest chamber model: one house, five multi-member electorates.",
    "The Labor-Greens pattern makes it useful for testing coalition, confidence and supply language.",
    "Canberra is also symbolically important for the 2031 referendum simulator."
  ],
  "sources": [
    {
      "label": "ACT Legislative Assembly current members",
      "url": "https://www.parliament.act.gov.au/members/current"
    },
    {
      "label": "Elections ACT current members and term date",
      "url": "https://www.elections.act.gov.au/elections/our-electoral-system/current-members-of-the-legislative-assembly"
    },
    {
      "label": "Elections ACT elections page",
      "url": "https://www.elections.act.gov.au/elections"
    }
  ]
}
```
