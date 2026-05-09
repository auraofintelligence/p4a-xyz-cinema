# Victoria history

This markdown file powers the generated P4A history page for Victoria. Edit the JSON block, then rerun `tools/build-state-sites.ps1`.

```json history-data
{
  "order": 2,
  "slug": "vic",
  "stateName": "Victoria",
  "shortName": "VIC",
  "stateType": "State",
  "researchRun": "2026-05-08",
  "researchTimezone": "Australia/Brisbane",
  "researchStatus": "Historical outline checked against Parliament of Victoria, National Museum of Australia, Parliament of Australia and AIATSIS sources. Treat as a research snapshot for authorised agents to refresh.",
  "summary": "Victoria is the reform pressure-cooker: Port Phillip separation, gold-rush democracy, the secret ballot, strong party government and modern upper-house proportional politics.",
  "differenceHint": "Victoria carries the secret ballot and Eureka as civic myths with real institutional consequences.",
  "basicThesis": "The basic Victorian story is separation from NSW, gold-rush pressure, responsible government and a strong identity around democratic reform.",
  "advancedThesis": "The advanced Victorian story is how electoral procedure, protest, party organisation and upper-house redesign changed the machinery of representation.",
  "themes": [
    {
      "id": "first-peoples",
      "label": "First Peoples"
    },
    {
      "id": "colonial-formation",
      "label": "Colonial formation"
    },
    {
      "id": "parliament",
      "label": "Parliament"
    },
    {
      "id": "franchise",
      "label": "Voting rights"
    },
    {
      "id": "federation",
      "label": "Federation"
    },
    {
      "id": "electoral-system",
      "label": "Electoral system"
    },
    {
      "id": "reform",
      "label": "Reform"
    },
    {
      "id": "crisis",
      "label": "Crisis"
    },
    {
      "id": "contemporary",
      "label": "Contemporary politics"
    }
  ],
  "events": [
    {
      "id": "vic-first-peoples",
      "sortYear": -60000,
      "dateLabel": "Before 1835",
      "period": "Deep time",
      "level": "basic",
      "themes": [
        "first-peoples"
      ],
      "title": "First Peoples govern the south-east",
      "summary": "The lands now called Victoria are Country for many First Peoples, including Kulin nations around Naarm/Melbourne.",
      "advanced": "Victorian civic history needs to acknowledge that colonial separation did not create the first political order on the land.",
      "difference": "Victoria has a compact geography but very dense layers of Country, treaty debate and urban colonial expansion.",
      "sources": [
        {
          "label": "AIATSIS Map of Indigenous Australia",
          "url": "https://aiatsis.gov.au/explore/map-indigenous-australia"
        }
      ]
    },
    {
      "id": "vic-1851-separation",
      "sortYear": 1851,
      "dateLabel": "1 July 1851",
      "period": "Colonial formation",
      "level": "basic",
      "themes": [
        "colonial-formation",
        "parliament"
      ],
      "title": "Victoria separates from NSW",
      "summary": "The Port Phillip District separated from NSW and became the colony of Victoria.",
      "advanced": "The first Victorian Legislative Council was unicameral, and it helped draft the Constitution that later created a two-house Parliament.",
      "difference": "Victoria begins as a breakaway from Sydney rule, which gives its state story a strong self-government tone.",
      "sources": [
        {
          "label": "Parliament of Victoria - Legislative Council 1851 to 1856",
          "url": "https://www.parliament.vic.gov.au/about/history-and-heritage/people-who-shaped-parliament/legislative-council-1851-1856/"
        }
      ]
    },
    {
      "id": "vic-1854-eureka",
      "sortYear": 1854,
      "dateLabel": "1854",
      "period": "Colonial formation",
      "level": "basic",
      "themes": [
        "crisis",
        "franchise"
      ],
      "title": "Eureka turns goldfields grievance into democratic pressure",
      "summary": "The Eureka Stockade became a defining conflict over licensing, representation and colonial authority.",
      "advanced": "Eureka is not the whole story of Victorian democracy, but it became a durable symbol of political accountability and resistance to arbitrary power.",
      "difference": "Victoria has one of Australia's strongest protest-to-democracy origin myths.",
      "sources": [
        {
          "label": "National Museum of Australia - Eureka Stockade",
          "url": "https://digital-classroom.nma.gov.au/defining-moments/eureka-stockade"
        }
      ]
    },
    {
      "id": "vic-1856-parliament",
      "sortYear": 1856,
      "dateLabel": "1856",
      "period": "Responsible government",
      "level": "basic",
      "themes": [
        "parliament",
        "electoral-system"
      ],
      "title": "Responsible government and the secret ballot arrive",
      "summary": "Victoria elected its first Parliament under the secret ballot in 1856.",
      "advanced": "The secret ballot reduced coercion and became known internationally as the Australian ballot, a procedural reform with global influence.",
      "difference": "Victoria is crucial in any cyber-republic simulator because ballot design itself is part of democratic architecture.",
      "sources": [
        {
          "label": "Parliament of Victoria - Legislative Council 1851 to 1856",
          "url": "https://www.parliament.vic.gov.au/about/history-and-heritage/people-who-shaped-parliament/legislative-council-1851-1856/"
        },
        {
          "label": "Parliament of Victoria - Victorian Constitution",
          "url": "https://www.parliament.vic.gov.au/about/how-parliament-works/constitution"
        }
      ]
    },
    {
      "id": "vic-1901-federation",
      "sortYear": 1901,
      "dateLabel": "1 January 1901",
      "period": "Federation",
      "level": "basic",
      "themes": [
        "federation"
      ],
      "title": "Victoria becomes a state",
      "summary": "Victoria entered the Commonwealth as a state at Federation.",
      "advanced": "Melbourne served as the temporary federal capital while Canberra was being built, keeping Victoria close to the early Commonwealth state.",
      "difference": "Victoria links state identity to the early national parliament more directly than most states.",
      "sources": [
        {
          "label": "Parliament of Australia democracy chronology",
          "url": "https://www.aph.gov.au/About_Parliament/Parliamentary_departments/Parliamentary_Library/pubs/rp/rp1920/ChronologyAustralianDemocracy"
        },
        {
          "label": "Parliament of Victoria - Victorian Constitution",
          "url": "https://www.parliament.vic.gov.au/about/how-parliament-works/constitution"
        }
      ]
    },
    {
      "id": "vic-1908-women",
      "sortYear": 1908,
      "dateLabel": "1908",
      "period": "Voting rights",
      "level": "advanced",
      "themes": [
        "franchise"
      ],
      "title": "Women win the state vote",
      "summary": "Victorian women gained the right to vote in state elections later than women in South Australia and Western Australia.",
      "advanced": "This timing matters because reform reputations are uneven: Victoria was early on the secret ballot but late on women's state suffrage.",
      "difference": "Victoria is a useful reminder that no state is simply progressive or conservative across every axis.",
      "sources": [
        {
          "label": "Parliament of Victoria - Victorian Constitution",
          "url": "https://www.parliament.vic.gov.au/about/how-parliament-works/constitution"
        }
      ]
    },
    {
      "id": "vic-upper-house-reform",
      "sortYear": 2003,
      "dateLabel": "2003 to 2006",
      "period": "Modern reform",
      "level": "advanced",
      "themes": [
        "parliament",
        "electoral-system",
        "reform"
      ],
      "title": "Upper-house reform reshapes accountability",
      "summary": "Reforms changed the Legislative Council into a proportional, region-based chamber from the 2006 election.",
      "advanced": "The change made the upper house less likely to be controlled automatically by the lower-house winner and more likely to review, bargain and amend.",
      "difference": "Victoria is a strong case for modelling bicameral checks under proportional representation.",
      "sources": [
        {
          "label": "Parliament of Victoria - Victorian Constitution",
          "url": "https://www.parliament.vic.gov.au/about/how-parliament-works/constitution"
        }
      ]
    },
    {
      "id": "vic-modern-split",
      "sortYear": 2022,
      "dateLabel": "2020s",
      "period": "Contemporary politics",
      "level": "basic",
      "themes": [
        "contemporary",
        "parliament"
      ],
      "title": "Strong executive government meets a plural upper house",
      "summary": "Modern Victorian politics shows how a strong lower-house government can still face a more plural upper house.",
      "advanced": "This split is important for explaining why one election result can produce two different negotiation environments.",
      "difference": "Victoria lets P4A compare executive strength with review-house complexity.",
      "sources": [
        {
          "label": "Parliament of Victoria - Victorian Constitution",
          "url": "https://www.parliament.vic.gov.au/about/how-parliament-works/constitution"
        }
      ]
    }
  ],
  "sources": [
    {
      "label": "AIATSIS Map of Indigenous Australia",
      "url": "https://aiatsis.gov.au/explore/map-indigenous-australia"
    },
    {
      "label": "Parliament of Victoria - Legislative Council 1851 to 1856",
      "url": "https://www.parliament.vic.gov.au/about/history-and-heritage/people-who-shaped-parliament/legislative-council-1851-1856/"
    },
    {
      "label": "National Museum of Australia - Eureka Stockade",
      "url": "https://digital-classroom.nma.gov.au/defining-moments/eureka-stockade"
    },
    {
      "label": "Parliament of Victoria - Victorian Constitution",
      "url": "https://www.parliament.vic.gov.au/about/how-parliament-works/constitution"
    },
    {
      "label": "Parliament of Australia democracy chronology",
      "url": "https://www.aph.gov.au/About_Parliament/Parliamentary_departments/Parliamentary_Library/pubs/rp/rp1920/ChronologyAustralianDemocracy"
    }
  ],
  "sortingNotes": [
    "sortYear is numeric so ancient, approximate and modern events can be sorted without parsing date labels.",
    "level basic is the plain public path. level advanced is for constitutional, electoral and institutional detail.",
    "themes allow the page controls and future agents to group history by topic.",
    "Every event should keep at least one source link."
  ]
}
```
