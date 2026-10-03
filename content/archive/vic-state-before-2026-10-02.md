# Victoria

```json state-data
{
  "order": 2,
  "slug": "vic",
  "name": "Victoria",
  "shortName": "VIC",
  "capital": "Melbourne",
  "stateType": "State",
  "researchRun": "2026-05-08",
  "researchTimezone": "Australia/Brisbane",
  "researchStatus": "The next election date is official. Legislative Council representation is from Parliament of Victoria annual reporting; lower-house numbers are a current working count after the Nepean by-election.",
  "government": {
    "leaderTitle": "Premier",
    "leader": "Jacinta Allan",
    "party": "Australian Labor Party",
    "arrangement": "Majority government",
    "inPowerSince": "2023-09-27",
    "note": "Labor is seeking a fourth term at the November 2026 election."
  },
  "elections": [
    {
      "label": "2026 Victorian State election",
      "date": "2026-11-28T08:00:00+11:00",
      "kind": "State general election",
      "scope": "general",
      "status": "Scheduled",
      "note": "Victoria holds state elections on the last Saturday in November every four years.",
      "source": "https://www.vec.vic.gov.au/voting/types-of-elections/state-elections",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2022-11-26T08:00:00+11:00",
        "daysSinceLabel": "Previous Victorian State election polling day",
        "daysSinceSource": "https://www.parliament.vic.gov.au/election",
        "archiveDaysSince": true,
        "cycleKey": "vic-2026-general",
        "archiveWithCycle": "next-higher-order-cycle-after-vic-2026-general",
        "archiveNote": "When this election becomes historical, keep days-since visible in the current cycle, then archive it with the next higher-order election cycle."
      }
    },
    {
      "label": "Nepean District by-election",
      "date": "2026-05-02T08:00:00+10:00",
      "kind": "State by-election",
      "scope": "by-election",
      "status": "Recently held",
      "note": "The by-election was held on 2 May 2026 after Sam Groth resigned; Anthony Marsh retained the seat for the Liberal Party.",
      "source": "https://www.vec.vic.gov.au/voting/current-elections/nepean-by-election",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2026-05-02T08:00:00+10:00",
        "daysSinceLabel": "Nepean District by-election polling day",
        "daysSinceSource": "https://www.vec.vic.gov.au/voting/current-elections/nepean-by-election",
        "archiveDaysSince": true,
        "cycleKey": "vic-2026-by-election",
        "archiveWithCycle": "vic-2026-general archive",
        "archiveNote": "Keep days-since visible while this event belongs to the current local cycle, then archive it with the next state or territory general election cycle."
      }
    }
  ],
  "chambers": [
    {
      "name": "Legislative Assembly",
      "type": "Lower house",
      "seats": 88,
      "majority": 45,
      "note": "Working count after the Nepean by-election result; confirm against Parliament member search when the new member is fully reflected.",
      "source": "https://www.parliament.vic.gov.au/members/",
      "composition": [
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 54
        },
        {
          "party": "Liberal Party",
          "short": "LIB",
          "seats": 20
        },
        {
          "party": "The Nationals",
          "short": "NAT",
          "seats": 9
        },
        {
          "party": "Australian Greens Victoria",
          "short": "GRN",
          "seats": 3
        },
        {
          "party": "Will Fowles and Darren Cheeseman",
          "short": "2 MLAs",
          "seats": 2,
          "memberSource": "https://www.parliament.vic.gov.au/members/",
          "members": [
            {
              "name": "Will Fowles",
              "seat": "Ringwood"
            },
            {
              "name": "Darren Cheeseman",
              "seat": "South Barwon"
            }
          ]
        }
      ]
    },
    {
      "name": "Legislative Council",
      "type": "Upper house",
      "seats": 40,
      "majority": 21,
      "note": "Party representation recorded by the Department of the Legislative Council as at 30 June 2025.",
      "source": "https://www.parliament.vic.gov.au/4ab1be/globalassets/tabled-paper-documents/tabled-paper-9497/legislative-council-annual-report-2024-25.pdf",
      "composition": [
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 15
        },
        {
          "party": "Liberal Party",
          "short": "LIB",
          "seats": 12
        },
        {
          "party": "Australian Greens Victoria",
          "short": "GRN",
          "seats": 4
        },
        {
          "party": "The Nationals",
          "short": "NAT",
          "seats": 2
        },
        {
          "party": "Legalise Cannabis Victoria",
          "short": "LCV",
          "seats": 2
        },
        {
          "party": "Animal Justice Party",
          "short": "AJP",
          "seats": 1
        },
        {
          "party": "Democratic Labour Party",
          "short": "DLP",
          "seats": 1
        },
        {
          "party": "Libertarian Party",
          "short": "LIBT",
          "seats": 1
        },
        {
          "party": "Shooters, Fishers and Farmers Party",
          "short": "SFF",
          "seats": 1
        },
        {
          "party": "Adem Somyurek",
          "short": "1 MLC",
          "seats": 1,
          "memberSource": "https://www.parliament.vic.gov.au/members/",
          "members": [
            {
              "name": "Adem Somyurek",
              "seat": "Northern Metropolitan"
            }
          ]
        }
      ]
    }
  ],
  "strategyNotes": [
    "Victoria is the closest scheduled state election on the portal.",
    "The lower house is still a Labor majority, but the upper house already forces negotiation.",
    "The Nepean by-election should stay marked as a recent signal, not a settled statewide forecast."
  ],
  "sources": [
    {
      "label": "Victorian Electoral Commission state elections",
      "url": "https://www.vec.vic.gov.au/voting/types-of-elections/state-elections"
    },
    {
      "label": "Victorian Electoral Commission Nepean by-election",
      "url": "https://www.vec.vic.gov.au/voting/current-elections/nepean-by-election"
    },
    {
      "label": "ABC Nepean result report",
      "url": "https://www.abc.net.au/news/2026-05-02/victoria-nepean-by-election-results/106633600"
    },
    {
      "label": "Parliament of Victoria members",
      "url": "https://www.parliament.vic.gov.au/members/"
    },
    {
      "label": "Legislative Council annual report 2024-25",
      "url": "https://www.parliament.vic.gov.au/4ab1be/globalassets/tabled-paper-documents/tabled-paper-9497/legislative-council-annual-report-2024-25.pdf"
    }
  ]
}
```
