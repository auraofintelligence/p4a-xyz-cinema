# Western Australia

```json state-data
{
  "order": 4,
  "slug": "wa",
  "name": "Western Australia",
  "shortName": "WA",
  "capital": "Perth",
  "stateType": "State",
  "researchRun": "2026-10-29",
  "researchTimezone": "Australia/Brisbane",
  "researchStatus": "Election review 29 October: December extraordinary postal polls close on 3 December at 6 pm Perth (AWST). Esperance Town Ward has a vacancy following Cr Johnston’s August resignation. Bridgetown-Greenbushes Cr Simon Robinson resigned effective 9 October; the council awaits advice on the replacement process and date. State Parliament composition retains its earlier review; individual council results and federal rosters are not freshly certified.",
  "government": {
    "leaderTitle": "Premier",
    "leader": "Roger Cook",
    "party": "Australian Labor Party",
    "arrangement": "Majority government",
    "inPowerSince": "2023-06-08",
    "note": "WA Labor holds a large lower-house majority after the 2025 state election."
  },
  "elections": [
    {
      "label": "2029 Western Australian State election",
      "date": "2029-03-10T08:00:00+08:00",
      "kind": "State general election",
      "scope": "general",
      "status": "Scheduled by fixed-term rule",
      "note": "WA state general elections are held on the second Saturday in March every four years.",
      "source": "https://www.elections.wa.gov.au/about-us/media/state-elections-information",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": true,
        "daysSinceDate": "2025-03-08T08:00:00+08:00",
        "daysSinceLabel": "Previous Western Australian State election polling day",
        "daysSinceSource": "https://www.elections.wa.gov.au/elections/state",
        "archiveDaysSince": true,
        "cycleKey": "wa-2029-general",
        "archiveWithCycle": "next-higher-order-cycle-after-wa-2029-general",
        "archiveNote": "When this election becomes historical, keep days-since visible in the current cycle, then archive it with the next higher-order election cycle."
      }
    },
    {
      "label": "2026 Secret Harbour by-election",
      "date": "2026-08-29T08:00:00+08:00",
      "kind": "Assembly by-election",
      "scope": "recent",
      "status": "Declared 9 September 2026",
      "note": "Luke Herdegen (One Nation) elected; final two-candidate preferred 57.19% against Georgia Tree 42.81%. This is separate from the March 2025 general election.",
      "source": "https://www.elections.wa.gov.au/about-us/media/releases/2627",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": false,
        "archiveDaysSince": true,
        "cycleKey": "wa-2026-secret-harbour-by-election",
        "archiveNote": "Preserve this event separately from the ordinary general-election cycle."
      }
    },
    {
      "label": "December 2026 council extraordinary elections — postal receipt deadline",
      "date": "2026-12-03T18:00:00+08:00",
      "kind": "Council extraordinary elections",
      "scope": "local-government",
      "status": "Nominations closed; postal election scheduled",
      "note": "Carnarvon President/Town/Gascoyne-Minilya, Coolgardie and Esperance Town proceed to election. Ballot packages must be received by 6 pm Perth time. Carnarvon Coral Bay/Plantation candidates were elected unopposed; names and affected current rosters remain follow-up.",
      "source": "https://www.elections.wa.gov.au/about-us/media/whats-new/2640",
      "dayMetrics": {
        "displayDaysUntil": true,
        "displayDaysSince": false,
        "archiveDaysSince": true,
        "cycleKey": "wa-december-2026-council-extraordinary-elections-postal-receipt-deadline",
        "archiveNote": "Preserve this event separately from the ordinary general-election cycle."
      }
    }
  ],
  "chambers": [
    {
      "name": "Legislative Assembly",
      "type": "Lower house",
      "seats": 59,
      "majority": 30,
      "note": "Current composition retained from the 17 October official roster: Secret Harbour One Nation, Nedlands Independent. Fresh full Parliament roster access returned 403 on 23 October.",
      "source": "https://www.parliament.wa.gov.au/Parliament/memblist.nsf/screenLAMembersParty",
      "composition": [
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 45
        },
        {
          "party": "Liberal Party",
          "short": "LIB",
          "seats": 6
        },
        {
          "party": "The Nationals WA",
          "short": "NAT",
          "seats": 6
        },
        {
          "party": "Jonathan Huston",
          "short": "1 MLA",
          "seats": 1,
          "members": [
            {
              "name": "Jonathan Huston",
              "seat": "Nedlands"
            }
          ],
          "memberSource": "https://www.parliament.wa.gov.au/parliament/memblist.nsf/WebCurrentMembLA"
        },
        {
          "party": "Pauline Hanson's One Nation",
          "short": "ONP",
          "seats": 1
        }
      ]
    },
    {
      "name": "Legislative Council",
      "type": "Upper house",
      "seats": 37,
      "majority": 19,
      "note": "Whole-state 37-member chamber; current party totals retained from 17 October. Fresh full roster access was blocked on 23 October.",
      "source": "https://www.parliament.wa.gov.au/parliament/memblist.nsf/WParty?Count=100&Expand=1&OpenForm=&Seq=8&Start=1",
      "composition": [
        {
          "party": "Australian Labor Party",
          "short": "ALP",
          "seats": 16
        },
        {
          "party": "Liberal Party",
          "short": "LIB",
          "seats": 10
        },
        {
          "party": "Greens (WA)",
          "short": "GRN",
          "seats": 4
        },
        {
          "party": "The Nationals WA",
          "short": "NAT",
          "seats": 2
        },
        {
          "party": "One Nation Party",
          "short": "ONP",
          "seats": 2
        },
        {
          "party": "Animal Justice Party",
          "short": "AJP",
          "seats": 1
        },
        {
          "party": "Australian Christian Party",
          "short": "ACP",
          "seats": 1
        },
        {
          "party": "Legalise Cannabis WA",
          "short": "LCW",
          "seats": 1
        }
      ]
    }
  ],
  "strategyNotes": [
    "WA is a strong-majority Labor jurisdiction with a newly whole-of-state upper house.",
    "The upper house is the more plural chamber and the better early place for simulator examples.",
    "The next fixed election sits well inside the pre-2032 build window."
  ],
  "sources": [
    {
      "label": "WA Legislative Assembly members by party",
      "url": "https://www.parliament.wa.gov.au/Parliament/memblist.nsf/screenLAMembersParty"
    },
    {
      "label": "WA current members by political party",
      "url": "https://www.parliament.wa.gov.au/parliament/memblist.nsf/WParty?Count=100&Expand=1&OpenForm=&Seq=8&Start=1"
    },
    {
      "label": "WAEC state elections",
      "url": "https://www.elections.wa.gov.au/elections/state"
    },
    {
      "label": "WAEC voting in a state election",
      "url": "https://www.elections.wa.gov.au/vote/voting-state-election"
    },
    {
      "label": "wa secret harbour declaration 2026",
      "url": "https://www.elections.wa.gov.au/about-us/media/releases/2627"
    },
    {
      "label": "wa secret harbour ballot 2026",
      "url": "https://www.elections.wa.gov.au/about-us/media/whats-new/2610"
    },
    {
      "label": "wa fixed date rule",
      "url": "https://www.elections.wa.gov.au/about-us/media/releases/1892"
    },
    {
      "label": "wa government current",
      "url": "https://www.wa.gov.au/government/media-statements/Cook%20Labor%20Government/New-laws-to-protect-more-Western-Australians-from-discrimination-20261020"
    },
    {
      "label": "wa december lg notice",
      "url": "https://www.elections.wa.gov.au/about-us/media/whats-new/2640"
    },
    {
      "label": "wa december lg hub",
      "url": "https://www.elections.wa.gov.au/elections/local-government-elections/2026-december-local-government-extraordinary-elections"
    },
    {
      "label": "wa september lg declaration",
      "url": "https://www.elections.wa.gov.au/about-us/media/whats-new/2633"
    },
    {
      "label": "wa september lg hub",
      "url": "https://www.elections.wa.gov.au/2026-september-local-government-extraordinary-elections"
    },
    {
      "label": "wa june lg hub",
      "url": "https://www.elections.wa.gov.au/2026-june-local-government-extraordinary-elections"
    },
    {
      "label": "Bridgetown-Greenbushes resignation notice, 9 October 2026",
      "url": "https://www.bridgetown.wa.gov.au/news/resignation-of-cr-simon-robinson/10700"
    },
    {
      "label": "Esperance Town Ward vacancy and postal election",
      "url": "https://www.esperance.wa.gov.au/news/postal-election-confirmed-for-town-ward-vacancy/550"
    }
  ],
  "previousResearchRun": "2026-10-23",
  "researchReview": {
    "checked": "2026-10-29",
    "timezone": "Australia/Brisbane",
    "scope": "Scoped election and council-vacancy review only. Parliament composition and unrelated records retain their previous dated checks; progressive counts do not establish final results or new officeholders.",
    "previousResearchRun": "2026-10-23",
    "sourceDatesPreserved": true
  }
}
```
