# New South Wales history

This markdown file powers the generated P4A history page for New South Wales. Edit the JSON block, then rerun `tools/build-state-sites.ps1`.

```json history-data
{
  "order": 1,
  "slug": "nsw",
  "stateName": "New South Wales",
  "shortName": "NSW",
  "stateType": "State",
  "researchRun": "2026-05-08",
  "researchTimezone": "Australia/Brisbane",
  "researchStatus": "Historical outline checked against NSW Parliament, Parliament of Australia and AIATSIS sources. Treat as a research snapshot for authorised agents to refresh.",
  "summary": "NSW is the oldest colonial parliament line in Australia: autocratic government, early Legislative Council, responsible government, Federation leadership and a modern lower house that can sit close to the majority line.",
  "differenceHint": "NSW is the long trunk of the colonial system. Many later state and territory stories branch from land once governed from Sydney.",
  "basicThesis": "The basic NSW story is the shift from colony to responsible government to Federation state, with Sydney as the institutional starting point for much of eastern Australia.",
  "advancedThesis": "The advanced NSW story is how executive power, bicameralism, the Legislative Council and a large lower house created one of the key templates for Australian parliamentary government.",
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
      "id": "contemporary",
      "label": "Contemporary politics"
    }
  ],
  "events": [
    {
      "id": "nsw-first-peoples",
      "sortYear": -60000,
      "dateLabel": "Before 1788",
      "period": "Deep time",
      "level": "basic",
      "themes": [
        "first-peoples"
      ],
      "title": "First Peoples govern Country",
      "summary": "The lands now called NSW were and remain Country for many Aboriginal nations with their own law, language, diplomacy and custodial responsibilities.",
      "advanced": "A history portal should treat colonisation as a disruption of existing governance, not the beginning of governance itself.",
      "difference": "NSW contains the Sydney invasion point, so the national colonial story starts here more visibly than in any other jurisdiction.",
      "sources": [
        {
          "label": "AIATSIS Map of Indigenous Australia",
          "url": "https://aiatsis.gov.au/explore/map-indigenous-australia"
        }
      ]
    },
    {
      "id": "nsw-1788-colony",
      "sortYear": 1788,
      "dateLabel": "1788",
      "period": "Colonial formation",
      "level": "basic",
      "themes": [
        "colonial-formation"
      ],
      "title": "British colonisation begins at Sydney Cove",
      "summary": "The colony of New South Wales began under British military and gubernatorial authority.",
      "advanced": "Early NSW government was executive and military in character. Representative checks arrived later and unevenly.",
      "difference": "Because NSW once covered large parts of eastern Australia, its early institutions became the parent layer for later colonies.",
      "sources": [
        {
          "label": "NSW Parliament - History of the Legislative Assembly",
          "url": "https://www.parliament.nsw.gov.au/la/roleandhistory/Pages/The-history-of-the-Legislative-Assembly.aspx"
        }
      ]
    },
    {
      "id": "nsw-1823-council",
      "sortYear": 1823,
      "dateLabel": "1823 to 1824",
      "period": "Colonial formation",
      "level": "advanced",
      "themes": [
        "parliament",
        "colonial-formation"
      ],
      "title": "Legislative Council is authorised and first sits",
      "summary": "British legislation in 1823 allowed a Legislative Council, which first met in 1824.",
      "advanced": "The early Council was appointed and weak by modern standards, but it marks the first legislative body in Australia.",
      "difference": "NSW can claim the oldest continuous parliamentary line in the country, even though early representation was narrow.",
      "sources": [
        {
          "label": "NSW Parliament - History of the Legislative Assembly",
          "url": "https://www.parliament.nsw.gov.au/la/roleandhistory/Pages/The-history-of-the-Legislative-Assembly.aspx"
        },
        {
          "label": "NSW Parliament - Legislative Council history",
          "url": "https://www.parliament.nsw.gov.au/lc/roleandhistory/pages/role-and-history-of-the-council.aspx"
        }
      ]
    },
    {
      "id": "nsw-1856-responsible",
      "sortYear": 1856,
      "dateLabel": "22 May 1856",
      "period": "Responsible government",
      "level": "basic",
      "themes": [
        "parliament"
      ],
      "title": "Responsible government opens a bicameral Parliament",
      "summary": "NSW opened a bicameral Parliament with a Legislative Assembly and Legislative Council under responsible government.",
      "advanced": "The executive became connected to parliamentary confidence, but franchise, property and plural voting limits still shaped who could participate.",
      "difference": "This is one of the core Westminster templates later Australians inherited and modified.",
      "sources": [
        {
          "label": "NSW Parliament - 1856 to 1889 responsible government",
          "url": "https://www.parliament.nsw.gov.au/about/Pages/1856-to-1889-Responsible-Government-and-Colonial-.aspx"
        }
      ]
    },
    {
      "id": "nsw-1901-federation",
      "sortYear": 1901,
      "dateLabel": "1 January 1901",
      "period": "Federation",
      "level": "basic",
      "themes": [
        "federation"
      ],
      "title": "NSW becomes a state in the Commonwealth",
      "summary": "At Federation, NSW moved from colony to state while sharing sovereignty with the new Commonwealth Parliament.",
      "advanced": "Federation narrowed some state responsibilities while preserving state constitutions, parliaments and domestic law-making power.",
      "difference": "NSW matters nationally because the largest colony had to be inside the bargain for Federation to work.",
      "sources": [
        {
          "label": "Parliament of Australia democracy chronology",
          "url": "https://www.aph.gov.au/About_Parliament/Parliamentary_departments/Parliamentary_Library/pubs/rp/rp1920/ChronologyAustralianDemocracy"
        },
        {
          "label": "NSW Parliament - History of the Legislative Assembly",
          "url": "https://www.parliament.nsw.gov.au/la/roleandhistory/Pages/The-history-of-the-Legislative-Assembly.aspx"
        }
      ]
    },
    {
      "id": "nsw-council-reform",
      "sortYear": 1978,
      "dateLabel": "Late twentieth century",
      "period": "Modern reform",
      "level": "advanced",
      "themes": [
        "parliament",
        "electoral-system",
        "reform"
      ],
      "title": "Legislative Council reform modernises the upper house",
      "summary": "Late twentieth-century reforms changed the NSW upper house towards direct election and proportional representation.",
      "advanced": "This made the Council a more party-proportional negotiation chamber rather than a chamber dominated by appointment or older elite structures.",
      "difference": "For P4A simulation, NSW shows how upper houses can become bargaining spaces rather than simple government mirrors.",
      "sources": [
        {
          "label": "NSW Parliament - Legislative Council history",
          "url": "https://www.parliament.nsw.gov.au/lc/roleandhistory/pages/role-and-history-of-the-council.aspx"
        }
      ]
    },
    {
      "id": "nsw-fixed-terms",
      "sortYear": 1995,
      "dateLabel": "1995",
      "period": "Modern reform",
      "level": "advanced",
      "themes": [
        "electoral-system",
        "reform"
      ],
      "title": "Fixed four-year terms enter the system",
      "summary": "NSW moved towards fixed four-year parliamentary terms, making election timing more predictable.",
      "advanced": "Predictable cycles are useful for civic preparation because campaigns, data refreshes and public deliberation can be scheduled around known dates.",
      "difference": "NSW is one of the cleanest large-state countdowns for the portal because the next election date is scheduled well ahead.",
      "sources": [
        {
          "label": "NSW Parliament - History of the Legislative Assembly",
          "url": "https://www.parliament.nsw.gov.au/la/roleandhistory/Pages/The-history-of-the-Legislative-Assembly.aspx"
        }
      ]
    },
    {
      "id": "nsw-modern-crossbench",
      "sortYear": 2023,
      "dateLabel": "2023",
      "period": "Contemporary politics",
      "level": "basic",
      "themes": [
        "contemporary",
        "parliament"
      ],
      "title": "A close lower house puts crossbench trust in view",
      "summary": "The 2023 Parliament shows why named independents and crossbench relationships matter in plain language.",
      "advanced": "A chamber one seat short of majority turns public trust, confidence and supply, and named local MPs into practical governance details.",
      "difference": "NSW is a good simulator case for explaining minority government without making it sound exotic or broken.",
      "sources": [
        {
          "label": "NSW Parliament party representation",
          "url": "https://www.parliament.nsw.gov.au/members/pages/party-representation.aspx"
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
      "label": "NSW Parliament - History of the Legislative Assembly",
      "url": "https://www.parliament.nsw.gov.au/la/roleandhistory/Pages/The-history-of-the-Legislative-Assembly.aspx"
    },
    {
      "label": "NSW Parliament - Legislative Council history",
      "url": "https://www.parliament.nsw.gov.au/lc/roleandhistory/pages/role-and-history-of-the-council.aspx"
    },
    {
      "label": "NSW Parliament - 1856 to 1889 responsible government",
      "url": "https://www.parliament.nsw.gov.au/about/Pages/1856-to-1889-Responsible-Government-and-Colonial-.aspx"
    },
    {
      "label": "Parliament of Australia democracy chronology",
      "url": "https://www.aph.gov.au/About_Parliament/Parliamentary_departments/Parliamentary_Library/pubs/rp/rp1920/ChronologyAustralianDemocracy"
    },
    {
      "label": "NSW Parliament party representation",
      "url": "https://www.parliament.nsw.gov.au/members/pages/party-representation.aspx"
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
