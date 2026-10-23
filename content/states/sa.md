# South Australia

```json state-data
{
  "order": 5,
  "slug": "sa",
  "name": "South Australia",
  "shortName": "SA",
  "capital": "Adelaide",
  "stateType": "State",
  "researchRun": "2026-10-23",
  "researchTimezone": "Australia/Brisbane",
  "researchStatus": "Scoped review 23 October: current House roster (source updated 22 May) confirms Labor 33 and five independents, including Speaker Nat Cook. Council summary now matches the retained 17 October roster; fresh full Council access was blocked. Final 2026 Council elected-order file and 7 April 2027 council postal deadline rechecked. Historical ballots and current affiliations remain separate.",
  "government": {
    "leaderTitle": "Premier",
    "leader": "Peter Malinauskas",
    "party": "Australian Labor Party",
    "arrangement": "Majority government",
    "inPowerSince": "2022-03-21",
    "note": "Labor won an expanded House of Assembly majority at the 2026 South Australian election."
  },
  "elections": [
    {
      "label": "2030 South Australian State election",
      "date": "2030-03-16T08:00:00+10:30",
      "kind": "State general election",
      "scope": "general",
      "status": "Scheduled by fixed-term cycle",
      "note": "Rule-derived ordinary date: third Saturday in March every four years, subject to the Act; not a newly announced 2030 timetable.",
      "source": "https://ecsa.sa.gov.au/html/publications/2022-State-and-by-Election-Reports/chapter-2.html",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2026-03-21T08:00:00+10:30",
        "daysSinceLabel": "Previous South Australian State election polling day",
        "daysSinceSource": "https://ecsa.sa.gov.au/images/Compliance%20branch/Forms%20and%20guides/Guides/SE2026/Compliance%20Key%20Dates%20-%202026%20State%20Election.pdf",
        "archiveDaysSince": true,
        "cycleKey": "sa-2030-general",
        "archiveWithCycle": "next-higher-order-cycle-after-sa-2030-general",
        "archiveNote": "When this election becomes historical, keep days-since visible in the current cycle, then archive it with the next higher-order election cycle."
      }
    },
    {
      "label": "2026 South Australian State election",
      "date": "2026-03-21T08:00:00+10:30",
      "kind": "State general election",
      "scope": "recent",
      "status": "Final results published",
      "note": "Kept here as the most recent research anchor after the March 2026 election.",
      "source": "https://result.ecsa.sa.gov.au/",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2026-03-21T08:00:00+10:30",
        "daysSinceLabel": "2026 South Australian State election polling day",
        "daysSinceSource": "https://ecsa.sa.gov.au/images/Compliance%20branch/Forms%20and%20guides/Guides/SE2026/Compliance%20Key%20Dates%20-%202026%20State%20Election.pdf",
        "archiveDaysSince": true,
        "cycleKey": "sa-2026-recent",
        "archiveWithCycle": "sa-2030-general archive",
        "archiveNote": "Keep days-since visible while this event belongs to the current local cycle, then archive it with the next state or territory general election cycle."
      }
    },
    {
      "label": "2027 periodic council elections — postal receipt deadline",
      "date": "2027-04-07T17:00:00+09:30",
      "kind": "Ordinary council elections",
      "scope": "local-government",
      "status": "Official timetable published",
      "note": "Voting packages must be received by 5 pm Adelaide time. Rolls close 4 January; nominations run 26 January–9 February (noon). This replaces the earlier November 2026 schedule; council-specific exceptions remain separate.",
      "source": "https://www.councilelections.sa.gov.au/about/key-dates",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": false,
        "archiveDaysSince": true,
        "cycleKey": "sa-2027-periodic-council-elections-postal-receipt-deadline",
        "archiveNote": "Preserve this event separately from the ordinary general-election cycle."
      }
    }
  ],
  "chambers": [
    {
      "name": "House of Assembly",
      "type": "Lower house",
      "seats": 47,
      "majority": 24,
      "note": "Current official House roster, last updated 22 May 2026 and read 23 October. Nat Cook is Independent Speaker; her March election affiliation remains in historical results.",
      "source": "https://contact-details-api.parliament.sa.gov.au/api/HAMembersDetails",
      "composition": [
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 33
        },
        {
          "party": "Liberal Party",
          "short": "LIB",
          "seats": 5
        },
        {
          "party": "Pauline Hanson's One Nation",
          "short": "ONP",
          "seats": 4
        },
        {
          "party": "Geoff Brock, Matt Schultz, Lou Nicholson, Travis Fatchen, Nat Cook",
          "short": "5 MHAs",
          "seats": 5,
          "memberSource": "https://contact-details-api.parliament.sa.gov.au/api/HAMembersDetails",
          "members": [
            {
              "name": "Geoff Brock",
              "seat": "Stuart"
            },
            {
              "name": "Matt Schultz",
              "seat": "Kavel"
            },
            {
              "name": "Lou Nicholson",
              "seat": "Finniss"
            },
            {
              "name": "Travis Fatchen",
              "seat": "Mount Gambier"
            },
            {
              "name": "Nat Cook",
              "seat": "Hurtle Vale"
            }
          ]
        }
      ]
    },
    {
      "name": "Legislative Council",
      "type": "Upper house",
      "seats": 22,
      "majority": 12,
      "note": "22-member roster retained from the 17 October review: One Nation 3 and Family First 1. Fresh complete roster access was blocked on 23 October; this is not a new full certification.",
      "source": "https://www.parliament.sa.gov.au/en/Legislative-Council/Members",
      "composition": [
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 10
        },
        {
          "party": "Liberal Party",
          "short": "LIB",
          "seats": 6
        },
        {
          "party": "Pauline Hanson's One Nation",
          "short": "ONP",
          "seats": 3
        },
        {
          "party": "The Greens",
          "short": "GRN",
          "seats": 2
        },
        {
          "party": "Family First Party",
          "short": "FF",
          "seats": 1
        }
      ]
    }
  ],
  "strategyNotes": [
    "SA is the freshest full state-election result in the portal.",
    "The 2026 result shows how quickly a chamber map can change when a minor party surges.",
    "Keep SA marked as a post-election learning page before turning it into campaign assumptions."
  ],
  "sources": [
    {
      "label": "ECSA final 2026 elected Legislative Council members",
      "url": "https://result.ecsa.sa.gov.au/assets/Elected_Members_of_Parliament_2026.csv"
    },
    {
      "label": "ECSA results website",
      "url": "https://result.ecsa.sa.gov.au/"
    },
    {
      "label": "ECSA 2026 compliance key dates",
      "url": "https://ecsa.sa.gov.au/images/Compliance%20branch/Forms%20and%20guides/Guides/SE2026/Compliance%20Key%20Dates%20-%202026%20State%20Election.pdf"
    },
    {
      "label": "ECSA elections",
      "url": "https://ecsa.sa.gov.au/elections"
    },
    {
      "label": "ABC SA 2026 results and named crossbench winners",
      "url": "https://www.abc.net.au/news/elections/sa/2026/results"
    },
    {
      "label": "Official assembly source",
      "url": "https://contact-details-api.parliament.sa.gov.au/api/HAMembersDetails"
    },
    {
      "label": "Official stateElectionSchedule source",
      "url": "https://ecsa.sa.gov.au/html/publications/2022-State-and-by-Election-Reports/chapter-2.html"
    }
  ],
  "previousResearchRun": "2026-05-08",
  "researchReview": {
    "checked": "2026-10-23",
    "timezone": "Australia/Brisbane",
    "scope": "State summary and named election/process changes; see researchStatus and linked evidence for partial reviews. Unchanged or inaccessible underlying records retain their dated checks.",
    "previousResearchRun": "2026-05-08",
    "sourceDatesPreserved": true
  }
}
```
