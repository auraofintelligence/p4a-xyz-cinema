# Law Engine / Legal RAG

```json foundation-page
{
  "slug": "legal-rag",
  "title": "Law Engine / Legal RAG | P4A",
  "metaDescription": "A P4A workbench page for a Legal RAG or Law Engine: Acts, common law, state constitutions, council powers, version control, checks and balances.",
  "heroImage": "../assets/p4a-map-card.webp",
  "heroImageAlt": "P4A purple Australia map used as a legal memory reference",
  "eyebrow": "Legal memory",
  "heading": "Law Engine / Legal RAG",
  "heroCopy": "A future cyber republic cannot run on vibes. It needs a careful legal memory layer that can retrieve, cite, compare and explain the law without pretending to replace lawyers, courts, parliaments or community judgement.",
  "primaryCta": {
    "label": "Open the checks",
    "href": "#checks"
  },
  "secondaryCta": {
    "label": "Back to architecture",
    "href": "architecture.html"
  },
  "researchRun": "2026-05-08",
  "researchTimezone": "Australia/Brisbane",
  "researchStatus": "Foundation pass drafted from the P4A architecture direction and local government funding submission. Legal details require future source-by-source review.",
  "sourceMarkdown": "content/foundation/legal-rag.md",
  "sections": [
    {
      "id": "role",
      "eyebrow": "Role",
      "heading": "A translator, memory system and simulator - not a judge.",
      "paragraphs": [
        "The Law Engine is the civic legal memory layer for P4A. It should help people understand what law says, where powers come from, what changed between versions, and what legal risks a reform idea might trigger.",
        "It does not hand down law. It does not replace legal advice. It makes sources easier to inspect, and it makes uncertainty visible before political claims harden into slogans."
      ],
      "cards": [
        {
          "label": "Retrieve",
          "title": "Find the relevant law",
          "body": "Search Acts, regulations, constitutions, council instruments, cases, inquiry reports and explanatory material with citations attached."
        },
        {
          "label": "Explain",
          "title": "Translate into plain English",
          "body": "Turn dense legal text into readable summaries, with source links, uncertainty labels and a path back to the original wording."
        },
        {
          "label": "Compare",
          "title": "Show what changed",
          "body": "Track amendments, repeals, commencement dates, delegated powers, conflicts and old versions through public revision history."
        },
        {
          "label": "Simulate",
          "title": "Test reform pathways",
          "body": "Model what a proposed change touches: state law, Commonwealth law, local powers, constitutional limits, budgets and implementation steps."
        }
      ]
    },
    {
      "id": "sources",
      "eyebrow": "Source stack",
      "heading": "The law layer has to know where authority lives.",
      "paragraphs": [
        "Australia is legally layered. A council issue may touch local laws, planning schemes, state Acts, Commonwealth funding rules, court decisions, native title, procurement rules and the Constitution.",
        "Future agents should use this source stack by jurisdiction, and only refresh it through a permissioned review step that keeps each source visible."
      ],
      "cards": [
        {
          "label": "Constitutions",
          "title": "Commonwealth, states and territories",
          "body": "The Australian Constitution, state and territory constitution Acts, referendum rules and amendment procedures."
        },
        {
          "label": "Acts",
          "title": "Primary legislation",
          "body": "Commonwealth Acts, state Acts, territory laws, local government Acts, electoral Acts, planning Acts and administrative law."
        },
        {
          "label": "Instruments",
          "title": "Regulations and delegated law",
          "body": "Regulations, local laws, bylaws, planning instruments, standards, ministerial directions, procurement rules and codes."
        },
        {
          "label": "Cases",
          "title": "Common law and courts",
          "body": "Court decisions, tribunal decisions, precedent notes, judicial review pathways and legal principles that shape public power."
        },
        {
          "label": "Protocol",
          "title": "First Nations law and data sovereignty",
          "body": "Cultural authority, native title bodies, Indigenous Data Sovereignty, protocol notes and respectful limits on what a machine should claim."
        },
        {
          "label": "Evidence",
          "title": "Public reasoning material",
          "body": "Inquiry submissions, committee reports, explanatory memoranda, budget papers, audit reports and public consultation records."
        }
      ]
    },
    {
      "id": "checks",
      "eyebrow": "Checks and balances",
      "heading": "The engine needs brakes before it gets horsepower.",
      "paragraphs": [
        "A legal AI that sounds confident is dangerous if its uncertainty is hidden. The P4A version should be built around restraint: cite sources, mark assumptions, invite correction and separate law from strategy.",
        "The goal is not perfect automation. The goal is a better public memory system for humans who remain accountable."
      ],
      "cards": [
        {
          "label": "01",
          "title": "Citations first",
          "body": "Every serious claim points back to source text, source date, jurisdiction, version and retrieval run."
        },
        {
          "label": "02",
          "title": "Human review gates",
          "body": "Sensitive outputs need accountable review by humans, and legal outputs need appropriate legal expertise before adoption."
        },
        {
          "label": "03",
          "title": "Uncertainty labels",
          "body": "The system should clearly mark settled law, contested interpretation, policy preference, speculation and missing data."
        },
        {
          "label": "04",
          "title": "Conflict logging",
          "body": "Conflicts of interest, source gaps, model limitations, jurisdiction clashes and correction requests belong in the public trail."
        },
        {
          "label": "05",
          "title": "Version control",
          "body": "Acts, policies, summaries and model prompts should all have visible versions, diffs and rollback paths."
        },
        {
          "label": "06",
          "title": "Right of reply",
          "body": "People and organisations affected by a public claim need a correction path and a visible record of disputed points."
        }
      ],
      "tags": [
        "cite before claim",
        "human accountable",
        "uncertainty visible",
        "source dated",
        "revision trail",
        "correction path"
      ]
    },
    {
      "id": "fractal",
      "eyebrow": "Fractal deployment",
      "heading": "The same legal memory should work at every scale.",
      "paragraphs": [
        "The Law Engine becomes useful when it can answer the same class of question at different levels: what can a household do, what can a community group do, what can a council do, what can a state do, and what needs national change?",
        "That is where the fractal architecture becomes practical rather than poetic."
      ],
      "cards": [
        {
          "label": "Local",
          "title": "Council and community",
          "body": "Local laws, asset powers, rates, planning, public land, waste, libraries, parks, disaster readiness and community co-op models."
        },
        {
          "label": "State",
          "title": "State and territory",
          "body": "State constitutions, parliaments, upper houses, electoral law, planning powers, courts, health, education, police and infrastructure."
        },
        {
          "label": "National",
          "title": "Commonwealth",
          "body": "Constitutional powers, taxation, digital asset law, corporations law, national standards, public finance and referendum design."
        },
        {
          "label": "Bioregion",
          "title": "Living systems",
          "body": "Catchments, coasts, islands, food systems, climate risk, fire, flood and restoration work that does not fit neatly inside human borders."
        }
      ]
    },
    {
      "id": "workflow",
      "eyebrow": "Public workflow",
      "heading": "From question to civic source code.",
      "paragraphs": [
        "The Law Engine should eventually make law feel navigable without making it feel casual. A reform idea moves through question, retrieval, explanation, review, simulation, public comment, versioned decision and archive."
      ],
      "cards": [
        {
          "label": "1",
          "title": "Ask",
          "body": "A person asks a practical question: can this council do X, who has power, what law blocks it, what changed?"
        },
        {
          "label": "2",
          "title": "Retrieve",
          "body": "The system gathers relevant sources and shows what it used, what it ignored and what it could not find."
        },
        {
          "label": "3",
          "title": "Explain",
          "body": "The answer is written in plain English with direct citations and a confidence label."
        },
        {
          "label": "4",
          "title": "Review",
          "body": "Humans check it, challenge it, correct it and record open questions."
        },
        {
          "label": "5",
          "title": "Simulate",
          "body": "The reform is tested against budgets, powers, rights, institutions, local effects and likely implementation paths."
        },
        {
          "label": "6",
          "title": "Publish",
          "body": "The final public note includes source dates, reviewers, unresolved risks, version number and next review date."
        }
      ],
      "links": [
        {
          "label": "Truth Engine",
          "href": "truth-engine.html"
        },
        {
          "label": "Constitution workbench",
          "href": "constitution.html"
        },
        {
          "label": "Civic ledger",
          "href": "civic-ledger.html"
        },
        {
          "label": "Cyber-Republic simulator",
          "href": "cyber-republic.html"
        },
        {
          "label": "Example legal workbench",
          "href": "https://auraofintelligence.github.io/legal-memory-workbench/"
        }
      ]
    }
  ],
  "nextLinks": [
    {
      "label": "Open the Truth Engine",
      "href": "truth-engine.html",
      "style": "primary"
    },
    {
      "label": "Open the architecture workbench",
      "href": "architecture.html",
      "style": "secondary"
    }
  ]
}
```
