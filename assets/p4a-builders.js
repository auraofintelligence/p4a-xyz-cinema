(() => {
  const form = document.querySelector("[data-p4a-builder]");
  if (!form) return;

  const requestedTool = new URLSearchParams(window.location.search).get("tool");
  const retiredTools = {
    "private-twin-context": "aura-genesis.html"
  };
  if (requestedTool && retiredTools[requestedTool]) {
    window.location.replace(retiredTools[requestedTool]);
    return;
  }
  if (requestedTool && form.hasAttribute("data-p4a-dynamic-builder")) {
    form.dataset.p4aBuilder = requestedTool;
  }

  const builderId = form.dataset.p4aBuilder;
  const output = document.querySelector("[data-builder-output]");
  const status = document.querySelector("[data-builder-status]");
  const copyButton = document.querySelector("[data-copy-builder]");
  const downloadButton = document.querySelector("[data-download-builder]");
  const clearButton = document.querySelector("[data-clear-builder]");
  const today = new Date().toISOString().slice(0, 10);
  const storageKey = `p4a-builder:${builderId}`;

  function setStatus(message) {
    if (status) status.textContent = message;
  }

  function readForm() {
    return new FormData(form);
  }

  function getValue(data, name, fallback = "") {
    const value = data.get(name);
    const text = value === null ? "" : String(value).trim();
    return text || fallback;
  }

  function getAll(data, name) {
    return data.getAll(name).map((value) => String(value).trim()).filter(Boolean);
  }

  function yamlScalar(value) {
    const text = value === undefined || value === null ? "" : String(value);
    if (text === "") return '""';
    if (/^[A-Za-z0-9_.:-]+$/.test(text)) return text;
    return JSON.stringify(text);
  }

  function frontmatter(meta) {
    const lines = ["---"];
    Object.entries(meta).forEach(([key, value]) => {
      if (Array.isArray(value)) {
        lines.push(`${key}:`);
        value.forEach((item) => lines.push(`  - ${yamlScalar(item)}`));
      } else {
        lines.push(`${key}: ${yamlScalar(value)}`);
      }
    });
    lines.push("---");
    return lines.join("\n");
  }

  function paragraph(value, fallback = "Left open.") {
    return value && value.trim() ? value.trim() : fallback;
  }

  function bulletList(items, fallback = "Left open.") {
    const cleanItems = items.map((item) => item.trim()).filter(Boolean);
    if (!cleanItems.length) return fallback;
    return cleanItems.map((item) => `- ${item}`).join("\n");
  }

  function splitLines(value) {
    return String(value || "")
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean);
  }

  function buildPrivateProfile(data) {
    const name = getValue(data, "civic_name", "Untitled civic twin");
    const place = getValue(data, "place_boundary", "Left open.");
    const consentScope = getValue(data, "consent_scope", "No sharing scope recorded in this draft.");
    const correctionPath = getValue(data, "correction_path", "No review or correction path recorded in this draft.");

    const meta = {
      schema: "p4a.private_civic_profile.v0",
      status: "exploratory_draft",
      primary_layer: "L0",
      layers: ["L0", "L1"],
      default_starting_layer: "L0",
      scale_path: "L0 private profile -> optional L1 public profile -> L2 ledger reference",
      boundary_kind: "person_home_private_node",
      capability_kind: "identity_consent_profile",
      capability_scope: "private_record_with_optional_public_summary",
      implementation_status: "browser_local_static_builder",
      visibility: "private",
      created: today,
      updated: today,
      review_status: getValue(data, "review_status", "needs_human_review"),
      source_repo: "p4a_xyz",
      source_builder: "pages/private-civic-profile-builder.html",
      purple_translation: "Purple-ified from profile starter and local profile-kit patterns for P4A civic twins.",
      consent_scope: consentScope,
      consent_model: getValue(data, "consent_model", "opt_in"),
      correction_path: correctionPath,
      confidence: getValue(data, "confidence", "draft")
    };

    return [
      frontmatter(meta),
      "",
      `# ${name}`,
      "",
      "## L0 Boundary",
      paragraph(place),
      "",
      "## Public Roles And Offers",
      paragraph(getValue(data, "public_roles")),
      "",
      "## Skills, Tools And Useful Capacities",
      bulletList(splitLines(getValue(data, "public_skills"))),
      "",
      "## Private Boundary",
      paragraph(getValue(data, "private_boundary"), "Private notes, identity material, care details, home context and sensitive files stay outside public lanes by default."),
      "",
      "## Consent Scope",
      paragraph(consentScope),
      "",
      "## Agent Use Or Handoff",
      paragraph(getValue(data, "handoff")),
      "",
      "## Owner Review Or Correction Path",
      paragraph(correctionPath),
      "",
      "## Agent Use Notes",
      "Agents may use this private L0 starting file for approved actions. Publishing, editing, merging into a leaderboard, or connecting it to a public ledger needs explicit review and consent."
    ].join("\n");
  }

  function buildNoticeboard(data) {
    const group = getValue(data, "group_name", "Untitled noticeboard");
    const boundary = getValue(data, "boundary_label", "Left open.");
    const noticeTypes = getAll(data, "notice_types");
    const consentScope = getValue(data, "consent_scope", "No sharing scope recorded in this draft.");
    const correctionPath = getValue(data, "correction_path", "No correction path recorded in this draft.");

    const meta = {
      schema: "p4a.public_noticeboard.v0",
      status: "exploratory_draft",
      primary_layer: "fractal",
      layers: ["L0", "L1", "L2", "L3+"],
      default_starting_layer: "context_dependent",
      scale_path: "L0 private noticeboard -> L1 local mesh -> L2 council or electorate front -> L3+ macro summary",
      boundary_kind: getValue(data, "boundary_kind", "community"),
      capability_kind: "public_noticeboard",
      capability_scope: "local_public_information_with_private_exclusions",
      implementation_status: "browser_local_static_builder",
      visibility: "public_draft",
      created: today,
      updated: today,
      review_status: getValue(data, "review_status", "needs_human_review"),
      source_repo: "p4a_xyz",
      source_builder: "pages/noticeboard-contract-builder.html",
      purple_translation: "Purple-ified from Straddie noticeboard network public_noticeboard.md patterns for P4A local civic noticeboards.",
      consent_scope: consentScope,
      consent_model: getValue(data, "consent_model", "public_after_review"),
      correction_path: correctionPath,
      confidence: getValue(data, "confidence", "draft")
    };

    return [
      frontmatter(meta),
      "",
      `# ${group} Public Noticeboard`,
      "",
      "## Local Boundary",
      paragraph(boundary),
      "",
      "## Notice Types",
      bulletList(noticeTypes),
      "",
      "## Public Offer",
      paragraph(getValue(data, "public_offer")),
      "",
      "## Reviewer Or Steward",
      paragraph(getValue(data, "reviewer")),
      "",
      "## Private Or Excluded Material",
      paragraph(getValue(data, "private_exclusions")),
      "",
      "## Review Rhythm",
      paragraph(getValue(data, "review_rhythm")),
      "",
      "## Consent Scope",
      paragraph(consentScope),
      "",
      "## Correction Path",
      paragraph(correctionPath),
      "",
      "## Notes For Future Agents",
      "Keep the public noticeboard boringly clear: source-linked, date-stamped, correctable, and separated from private support records."
    ].join("\n");
  }

  const moduleConfigs = {
    "contributor-card": {
      title: "Contributor Card Builder",
      eyebrow: "L0/L1 public summary",
      filename: "contributor-card.md",
      schema: "p4a.contributor_card.v0",
      primaryLayer: "L1",
      layers: ["L0", "L1", "L2"],
      defaultStartingLayer: "L0",
      scalePath: "L0 private profile -> L1 opt-in contributor card -> L2 public ledger reference",
      boundaryKind: "person_or_group",
      capabilityKind: "public_contributor_profile",
      capabilityScope: "local",
      visibility: "permissioned",
      sourceRepo: "sbt_profile_starter; stradbroke-grants-lab profile-kit",
      sourceBuilder: "pages/p4a-builder.html?tool=contributor-card",
      purpleTranslation: "Purple-ified from public profile, grant profile-kit and contributor summary patterns.",
      guardrail: "A contributor card is an opt-in public summary. Keep identity checks, private care context, home details and unreviewed contribution claims out of the public card.",
      prev: ["Private noticeboard", "p4a-builder.html?tool=private-noticeboard"],
      next: ["Local crew", "p4a-builder.html?tool=local-crew-onboarding"],
      focusOptions: ["public_identity", "roles", "skills", "offers", "limits", "ledger_refs"]
    },
    "private-noticeboard": {
      title: "Private Noticeboard Builder",
      eyebrow: "L0 self-management board",
      filename: "private-noticeboard.md",
      schema: "p4a.private_noticeboard.v0",
      primaryLayer: "L0",
      layers: ["L0", "L1"],
      defaultStartingLayer: "L0",
      scalePath: "L0 private noticeboard -> optional L1 trusted support mesh",
      boundaryKind: "private-home",
      capabilityKind: "private_noticeboard",
      capabilityScope: "fractal",
      visibility: "private",
      sourceRepo: "sbt_profile_starter; straddie-noticeboard-network pattern adapted for private use",
      sourceBuilder: "pages/p4a-builder.html?tool=private-noticeboard",
      purpleTranslation: "Purple-ified from noticeboard patterns for private self, home, health, study, care or life-improvement boards.",
      guardrail: "A private noticeboard is for the owner first. Agents may use it for approved reminders, drafting, planning or actions, but editing the record needs explicit permission.",
      prev: ["Private profile", "private-civic-profile-builder.html"],
      next: ["Contributor card", "p4a-builder.html?tool=contributor-card"],
      focusOptions: ["personal_priorities", "habits", "care_tasks", "home_tasks", "learning", "agent_actions"]
    },
    "local-crew-onboarding": {
      title: "Local Crew Onboarding Builder",
      eyebrow: "L1 field crew record",
      filename: "local-crew-onboarding.md",
      schema: "p4a.local_crew_onboarding.v0",
      primaryLayer: "L1",
      layers: ["L0", "L1", "L2"],
      defaultStartingLayer: "L1",
      scalePath: "L0 organiser note -> L1 crew handover -> L2 civic front roster",
      boundaryKind: "project_or_event",
      capabilityKind: "field_crew_onboarding",
      capabilityScope: "local",
      visibility: "permissioned",
      sourceRepo: "straddie-night-market-lab; p4a_xyz starter field kit",
      sourceBuilder: "pages/p4a-builder.html?tool=local-crew-onboarding",
      purpleTranslation: "Purple-ified from Straddie night-market onboarding and P4A field-kit patterns.",
      guardrail: "Keep private contact details, home details, vulnerable-person notes and unreviewed claims out of the public lane.",
      prev: ["Contributor card", "p4a-builder.html?tool=contributor-card"],
      next: ["Public noticeboard", "noticeboard-contract-builder.html"],
      focusOptions: ["stall_table", "roles", "safety", "follow_up", "public_notices", "handover"]
    },
    "project-readiness": {
      title: "Project Readiness Builder",
      eyebrow: "L1/L2 project profile",
      filename: "project-readiness.md",
      schema: "p4a.project_readiness.v0",
      primaryLayer: "L1",
      layers: ["L0", "L1", "L2"],
      defaultStartingLayer: "L1",
      scalePath: "L0 idea note -> L1 project readiness -> L2 public benefit register",
      boundaryKind: "community",
      capabilityKind: "project_readiness",
      capabilityScope: "local",
      visibility: "permissioned",
      sourceRepo: "stradbroke-grants-lab; straddie-content-assets-kit",
      sourceBuilder: "pages/p4a-builder.html?tool=project-readiness",
      purpleTranslation: "Purple-ified from grant-readiness, business-profile and content-assets builder patterns.",
      guardrail: "This is preparation evidence, not a grant approval, policy commitment or public endorsement.",
      prev: ["Public noticeboard", "noticeboard-contract-builder.html"],
      next: ["Legal source trail", "p4a-builder.html?tool=legal-source-trail"],
      focusOptions: ["applicant_truth", "eligibility", "budget", "evidence", "permissions", "community_benefit"]
    },
    "milestone-report": {
      title: "Milestone Report Builder",
      eyebrow: "L1/L2 public benefit evidence",
      filename: "milestone-report.md",
      schema: "p4a.milestone_report.v0",
      primaryLayer: "L2",
      layers: ["L1", "L2"],
      defaultStartingLayer: "L1",
      scalePath: "L1 project update -> L2 public benefit milestone -> ledger summary",
      boundaryKind: "project_or_event",
      capabilityKind: "milestone_report",
      capabilityScope: "local",
      visibility: "permissioned",
      sourceRepo: "stradbroke-grants-lab",
      sourceBuilder: "pages/p4a-builder.html?tool=milestone-report",
      purpleTranslation: "Purple-ified from milestone-report.md grant acquittal and project evidence patterns.",
      guardrail: "Do not turn progress notes into public claims until sources, permissions and reviewer notes are clear.",
      prev: ["Media assets", "p4a-builder.html?tool=media-assets"],
      next: ["Ledger summary", "p4a-builder.html?tool=contribution-ledger-summary"],
      focusOptions: ["progress", "budget_use", "public_benefit", "blocked_items", "photos_or_receipts", "next_steps"]
    },
    "contribution-ledger-summary": {
      title: "Contribution Ledger Summary Builder",
      eyebrow: "L0-L3 fractal ledger",
      filename: "contribution-ledger-summary.md",
      schema: "p4a.contribution_ledger_summary.v0",
      primaryLayer: "fractal",
      layers: ["L0", "L1", "L2", "L3+"],
      defaultStartingLayer: "context_dependent",
      scalePath: "L0 private contribution note -> L1 shared project ledger -> L2 public-good ledger -> L3+ macro rollup",
      boundaryKind: "fractal",
      capabilityKind: "contribution_ledger_summary",
      capabilityScope: "fractal",
      visibility: "permissioned",
      sourceRepo: "amity-outdoor-fitness-grant; stradbroke-grants-lab; p4a_xyz civic-ledger",
      sourceBuilder: "pages/p4a-builder.html?tool=contribution-ledger-summary",
      purpleTranslation: "Purple-ified from honour-board, proposal-response, public-good milestone and ledger summary patterns.",
      guardrail: "A ledger can be private, shared or public. This summary can describe reviewed contribution evidence, but it cannot mint C-Hours, promise rewards or expose private evidence. C-Hour receipts need an authorised agent pipeline with human checkpoints.",
      prev: ["Milestone report", "p4a-builder.html?tool=milestone-report"],
      next: ["C-Hour pipeline", "c-hour-receipt-builder.html"],
      focusOptions: ["private_progress", "shared_project", "public_benefit", "money_receipts", "time_contributed", "source_links", "review_status", "corrections"]
    },
    "legal-source-trail": {
      title: "Legal Source Trail Builder",
      eyebrow: "L0/L1 Legal RAG primer",
      filename: "legal-source-trail.md",
      schema: "p4a.legal_source_trail.v0",
      primaryLayer: "L0",
      layers: ["L0", "L1", "L2"],
      defaultStartingLayer: "L0",
      scalePath: "L0 source literacy -> L1 project risk questions -> L2 reviewed legal memory",
      boundaryKind: "jurisdiction_or_project",
      capabilityKind: "legal-rag",
      capabilityScope: "fractal",
      visibility: "private",
      sourceRepo: "legal-memory-workbench",
      sourceUrl: "https://auraofintelligence.github.io/legal-memory-workbench/",
      sourceBuilder: "pages/p4a-builder.html?tool=legal-source-trail",
      purpleTranslation: "Purple-ified from legal-memory, source-list, risk-map, evidence-checklist and agent-instruction patterns.",
      guardrail: "Legal RAG starts as legal information preparation, source literacy and question framing. It is not legal advice.",
      prev: ["Project readiness", "p4a-builder.html?tool=project-readiness"],
      next: ["Media assets", "p4a-builder.html?tool=media-assets"],
      focusOptions: ["source_list", "jurisdiction", "risk_questions", "evidence", "human_review", "agent_handoff"]
    },
    "media-assets": {
      title: "Media Assets Builder",
      eyebrow: "L1/L2 culture and provenance",
      filename: "media-provenance.md",
      schema: "p4a.media_provenance.v0",
      primaryLayer: "L1",
      layers: ["L1", "L2"],
      defaultStartingLayer: "L1",
      scalePath: "L1 crew asset list -> L2 public campaign provenance -> culture ledger",
      boundaryKind: "project_or_event",
      capabilityKind: "media",
      capabilityScope: "local",
      visibility: "permissioned",
      sourceRepo: "straddie-content-assets-kit; ai-native-indie-distribution",
      sourceBuilder: "pages/p4a-builder.html?tool=media-assets",
      purpleTranslation: "Purple-ified from content asset, shared gear, equipment wishlist, release provenance and agent brief workflows.",
      guardrail: "Keep permissions, licences, people shown in media, AI provenance and source files clear before public release.",
      prev: ["Legal source trail", "p4a-builder.html?tool=legal-source-trail"],
      next: ["Milestone report", "p4a-builder.html?tool=milestone-report"],
      focusOptions: ["asset_list", "shared_gear", "equipment_wishlist", "release_notes", "ai_provenance", "approval"]
    },
    "sovereign-space-node": {
      title: "Sovereign Space Node Builder",
      eyebrow: "L0 sensorium starter",
      filename: "sovereign-space-node.md",
      schema: "p4a.sovereign_space_node.v0",
      primaryLayer: "L0",
      layers: ["L0", "L1", "L2"],
      defaultStartingLayer: "L0",
      scalePath: "L0 private node -> L1 place mesh -> L2 living-boundary digital twin",
      boundaryKind: "private-home",
      capabilityKind: "sensorium",
      capabilityScope: "fractal",
      visibility: "private",
      sourceRepo: "Sovereign Space Builder source notes; p4a_xyz sovereignty stack",
      sourceBuilder: "pages/p4a-builder.html?tool=sovereign-space-node",
      purpleTranslation: "Purple-ified from Sovereign Space Builder notes: Human Digital Twin, Environmental Digital Twin and local-first Sovereign Node.",
      guardrail: "This is a prototype planning record. Treat tool capability, model availability, Web3 claims and public sensorium claims as unverified until checked from current sources.",
      prev: ["Builder suite", "civic-twin-builders.html#lane-place"],
      next: ["Sensorium place pack", "p4a-builder.html?tool=sensorium-place-pack"],
      focusOptions: ["home_cell", "environmental_context", "consent_rules", "offline_first", "mesh_sync", "public_summary"]
    },
    "sensorium-place-pack": {
      title: "Sensorium Place Pack Builder",
      eyebrow: "L1/L2 place twin",
      filename: "sensorium-place-pack.md",
      schema: "p4a.sensorium_place_pack.v0",
      primaryLayer: "L1",
      layers: ["L0", "L1", "L2"],
      defaultStartingLayer: "L1",
      scalePath: "L0 place note -> L1 local mesh place pack -> L2 living-boundary digital twin",
      boundaryKind: "bioregion_or_catchment",
      capabilityKind: "sensorium",
      capabilityScope: "fractal",
      visibility: "permissioned",
      sourceRepo: "Sovereign Space Builder source notes; Web3 Sensorium; Straddie Digital Twin Builders; Moreton Bay digital twin patterns",
      sourceBuilder: "pages/p4a-builder.html?tool=sensorium-place-pack",
      purpleTranslation: "Purple-ified from sensorium, Straddie digital twin and living-boundary source notes for place-based civic memory.",
      guardrail: "Place data can become collective data. Cultural, ecological, household and vulnerable-location material needs proper authority before public use.",
      prev: ["Sovereign node", "p4a-builder.html?tool=sovereign-space-node"],
      next: ["Living boundary map", "p4a-builder.html?tool=living-boundary-map"],
      focusOptions: ["place_sources", "ecology", "infrastructure", "risks", "local_knowledge", "public_summary"]
    },
    "living-boundary-map": {
      title: "Living Boundary Map Builder",
      eyebrow: "L1/L2 civic boundary",
      filename: "living-boundary-map.md",
      schema: "p4a.living_boundary_map.v0",
      primaryLayer: "L2",
      layers: ["L1", "L2"],
      defaultStartingLayer: "L1",
      scalePath: "L1 local knowledge -> L2 bioregion/catchment/island civic front -> state/national context",
      boundaryKind: "living_boundary",
      capabilityKind: "civic_map",
      capabilityScope: "local",
      visibility: "permissioned",
      sourceRepo: "p4a_xyz architecture; Sovereign Space Builder source notes; Straddie local systems",
      sourceBuilder: "pages/p4a-builder.html?tool=living-boundary-map",
      purpleTranslation: "Purple-ified from P4A architecture and living-boundary layer notes.",
      guardrail: "Living boundaries are useful civic boundaries, not decorative overlays. Use sources, local knowledge, Indigenous protocol where relevant and clear correction paths.",
      prev: ["Sensorium place pack", "p4a-builder.html?tool=sensorium-place-pack"],
      next: ["Local civic front", "p4a-builder.html?tool=local-civic-front"],
      focusOptions: ["bioregion", "catchment", "island_or_coast", "food_system", "disaster_corridor", "cultural_protocol"]
    },
    "local-civic-front": {
      title: "Local Civic Front Builder",
      eyebrow: "L2 public front",
      filename: "local-civic-front.md",
      schema: "p4a.local_civic_front.v0",
      primaryLayer: "L2",
      layers: ["L1", "L2"],
      defaultStartingLayer: "L2",
      scalePath: "L1 crew/project mesh -> L2 council/electorate/living-boundary front -> state portal evidence",
      boundaryKind: "council_or_electorate",
      capabilityKind: "local_civic_front",
      capabilityScope: "local",
      visibility: "public_draft",
      sourceRepo: "sbt_profile_starter; stradbroke-grants-lab; straddie-noticeboard-network; p4a_xyz",
      sourceBuilder: "pages/p4a-builder.html?tool=local-civic-front",
      purpleTranslation: "Purple-ified from profile, project, noticeboard and local field-kit patterns.",
      guardrail: "A local civic front is a public draft until sources, consent, role authority, legal limits and correction pathways are reviewed.",
      prev: ["Convergence", "civic-twin-builders.html#builder-convergence"],
      next: ["Builder suite", "civic-twin-builders.html"],
      focusOptions: ["local_offer", "public_noticeboard", "projects", "ledger_summary", "legal_sources", "human_review"]
    }
  };

  const builderFieldText = {
    "contributor-card": {
      guidance: "This is an opt-in public summary. It should not import private aura or proof material by default.",
      focusLegend: "Contributor card parts",
      fields: {
        record_title: { label: "Public card name", placeholder: "What chosen name, group name or public role should this card use?" },
        boundary_label: { label: "Public participation boundary", placeholder: "What community, project, campaign, event or public lane does this card belong to?" },
        boundary_kind: { label: "Card owner type" },
        purpose: { label: "Why this card exists", placeholder: "What should this card help people understand, invite or coordinate?" },
        public_summary: { label: "Public-facing summary", placeholder: "What roles, offers, skills or interests are safe and useful to show?" },
        private_boundary: { label: "Keep out of the public card", placeholder: "What proof, identity checks, home details, care context or private notes must stay elsewhere?" },
        evidence_notes: { label: "Reference hints", placeholder: "What public links, reviewed references or contribution pointers could be attached later?" },
        reviewer: { label: "Reviewer before publishing", placeholder: "Who has permission to check the card before it becomes public?" },
        next_handoff: { label: "Allowed follow-up", placeholder: "What can an agent or organiser do from this card, and what needs a human checkpoint?" },
        consent_scope: { label: "Public consent scope", placeholder: "What is okay to show, for which purpose, and when should this card be refreshed or withdrawn?" },
        correction_path: { label: "Public card correction path", placeholder: "If the card is shared, how can the owner or authorised steward correct or withdraw it?" }
      },
      sections: {
        boundary: "Public Participation Boundary",
        purpose: "Why This Card Exists",
        focus: "Contributor Card Parts",
        public: "Public-Facing Summary",
        private: "Keep Out Of The Public Card",
        evidence: "Reference Hints",
        reviewer: "Reviewer Before Publishing",
        handoff: "Allowed Follow-Up",
        consent: "Public Consent Scope",
        correction: "Public Card Correction Path"
      }
    },
    "private-noticeboard": {
      guidance: "This board can be only for the owner. Sharing it with a helper or agent is a separate permission choice.",
      focusLegend: "Private board lanes",
      fields: {
        record_title: { label: "Private board name", placeholder: "What life area, project, routine or private board needs a name?" },
        boundary_label: { label: "Private board boundary", placeholder: "Is this about self, home, study, health, care, repairs, admin, habits or another life area?" },
        boundary_kind: { label: "Board boundary type" },
        purpose: { label: "What the board helps with", placeholder: "What should this board help you notice, sort, remember, plan or ask an agent to do?" },
        public_summary: { label: "Optional shareable summary", placeholder: "If a trusted helper saw only one safe summary, what could it say?" },
        private_boundary: { label: "Private board limits", placeholder: "What should stay private, off-limits to agents, or separate from any shared support lane?" },
        evidence_notes: { label: "Signals and reminders", placeholder: "What dates, recurring signals, receipts, notes or context might help the board stay useful?" },
        reviewer: { label: "Trusted helper, if any", placeholder: "Who, if anyone, is allowed to help review this private board?" },
        next_handoff: { label: "Agent actions from board", placeholder: "What can an agent remind, draft, organise or prepare, and what needs approval first?" },
        consent_scope: { label: "Sharing rules", placeholder: "What stays private, what could be shared with a helper, and what needs fresh permission?" },
        correction_path: { label: "Owner cleanup path", placeholder: "How should stale items, wrong notes, withdrawals or changed priorities be cleaned up?" }
      },
      sections: {
        boundary: "Private Board Boundary",
        purpose: "What The Board Helps With",
        focus: "Private Board Lanes",
        public: "Optional Shareable Summary",
        private: "Private Board Limits",
        evidence: "Signals And Reminders",
        reviewer: "Trusted Helper, If Any",
        handoff: "Agent Actions From Board",
        consent: "Sharing Rules",
        correction: "Owner Cleanup Path"
      }
    },
    "local-crew-onboarding": {
      guidance: "This is a handover file for a local crew, not a private profile or public manifesto.",
      focusLegend: "Crew handover lanes",
      fields: {
        record_title: { label: "Crew or event name", placeholder: "What table, crew, event, market, circle or local activity is being handed over?" },
        boundary_label: { label: "Where and when", placeholder: "What place, date range, local boundary or operating context matters?" },
        boundary_kind: { label: "Crew boundary type" },
        purpose: { label: "Crew purpose", placeholder: "What is the crew trying to do, and what would count as a useful handover?" },
        public_summary: { label: "Public-facing offer", placeholder: "What can visitors, locals or participants safely know or ask for?" },
        private_boundary: { label: "Crew privacy limits", placeholder: "What contact details, vulnerable-person notes, logistics or support context should not go public?" },
        evidence_notes: { label: "Logistics and source notes", placeholder: "What rosters, maps, permits, stock lists, links, contacts or checklists might be relevant?" },
        reviewer: { label: "Crew steward", placeholder: "Who checks the handover before it is used by the next person or agent?" },
        next_handoff: { label: "Next handover actions", placeholder: "What should the next human or authorised agent prepare, confirm, draft or chase?" },
        consent_scope: { label: "Crew consent scope", placeholder: "What crew information can be shared, with whom, and what needs fresh permission?" },
        correction_path: { label: "Crew correction path", placeholder: "How should roster errors, outdated logistics or withdrawal requests be handled?" }
      },
      sections: {
        boundary: "Where And When",
        purpose: "Crew Purpose",
        focus: "Crew Handover Lanes",
        public: "Public-Facing Offer",
        private: "Crew Privacy Limits",
        evidence: "Logistics And Source Notes",
        reviewer: "Crew Steward",
        handoff: "Next Handover Actions",
        consent: "Crew Consent Scope",
        correction: "Crew Correction Path"
      }
    },
    "project-readiness": {
      guidance: "This captures readiness before a project asks for support, money, authority or public attention.",
      focusLegend: "Readiness checks",
      fields: {
        record_title: { label: "Project name", placeholder: "What project, grant idea, event, repair, build or local proposal is being prepared?" },
        boundary_label: { label: "Eligibility boundary", placeholder: "What place, group, applicant, site or funding boundary matters?" },
        boundary_kind: { label: "Project boundary type" },
        purpose: { label: "Project purpose", placeholder: "What problem, opportunity or public benefit is this project trying to address?" },
        public_summary: { label: "Community benefit summary", placeholder: "What benefit could be explained publicly after review?" },
        private_boundary: { label: "Not for public application yet", placeholder: "What budget assumptions, private notes, risks, contacts or uncertainties need review first?" },
        evidence_notes: { label: "Eligibility and evidence", placeholder: "What rules, quotes, receipts, source links, photos, approvals or proof might be needed?" },
        reviewer: { label: "Readiness reviewer", placeholder: "Who can check eligibility, evidence, budget notes or permissions?" },
        next_handoff: { label: "Readiness next steps", placeholder: "What should a human or authorised agent verify, draft, price, request or collect next?" },
        consent_scope: { label: "Project consent scope", placeholder: "What can be shared with funders, partners or community, and what needs permission first?" },
        correction_path: { label: "Project correction path", placeholder: "How should wrong assumptions, withdrawn support or changed eligibility be corrected?" }
      },
      sections: {
        boundary: "Eligibility Boundary",
        purpose: "Project Purpose",
        focus: "Readiness Checks",
        public: "Community Benefit Summary",
        private: "Not For Public Application Yet",
        evidence: "Eligibility And Evidence",
        reviewer: "Readiness Reviewer",
        handoff: "Readiness Next Steps",
        consent: "Project Consent Scope",
        correction: "Project Correction Path"
      }
    },
    "milestone-report": {
      guidance: "This is a reviewed progress receipt, not a victory lap or funding acquittal by itself.",
      focusLegend: "Milestone evidence",
      fields: {
        record_title: { label: "Milestone name", placeholder: "What milestone, delivery step, event, repair, purchase or public benefit is being reported?" },
        boundary_label: { label: "Project and period", placeholder: "Which project, place, team and reporting period does this milestone cover?" },
        boundary_kind: { label: "Milestone boundary type" },
        purpose: { label: "What changed", placeholder: "What progress, blocker, delivery, learning or public-good change should be recorded?" },
        public_summary: { label: "Public benefit note", placeholder: "What can be safely said about community benefit after source and consent review?" },
        private_boundary: { label: "Hold back from public note", placeholder: "What private receipts, names, issues, disputes or unreviewed claims should stay out?" },
        evidence_notes: { label: "Receipts and proof trail", placeholder: "What receipts, photos, dates, links, source files or reviewer notes support the milestone?" },
        reviewer: { label: "Milestone reviewer", placeholder: "Who checks the milestone before it informs a ledger, update or public report?" },
        next_handoff: { label: "Next project steps", placeholder: "What should happen next, and what can an agent prepare from this milestone?" },
        consent_scope: { label: "Milestone consent scope", placeholder: "What can be cited publicly, what is internal, and what needs fresh permission?" },
        correction_path: { label: "Milestone correction path", placeholder: "How should errors, missing receipts, disputes or withdrawn claims be corrected?" }
      },
      sections: {
        boundary: "Project And Period",
        purpose: "What Changed",
        focus: "Milestone Evidence",
        public: "Public Benefit Note",
        private: "Hold Back From Public Note",
        evidence: "Receipts And Proof Trail",
        reviewer: "Milestone Reviewer",
        handoff: "Next Project Steps",
        consent: "Milestone Consent Scope",
        correction: "Milestone Correction Path"
      }
    },
    "contribution-ledger-summary": {
      guidance: "This can be L0, L1, L2 or L3+. It summarises reviewed contribution evidence but does not mint C-Hours.",
      focusLegend: "Ledger lenses",
      fields: {
        record_title: { label: "Ledger summary name", placeholder: "What private, shared or public contribution summary is this?" },
        boundary_label: { label: "Ledger scale", placeholder: "Is this for self, household, crew, project, community, council, region or macro rollup?" },
        boundary_kind: { label: "Ledger boundary type" },
        purpose: { label: "Why summarise it", placeholder: "What should this summary help the owner, group, public or agent understand or do?" },
        public_summary: { label: "Shareable contribution summary", placeholder: "What can safely be said about contribution without exposing private proof?" },
        private_boundary: { label: "Evidence kept out", placeholder: "What names, receipts, private proof, financial details or sensitive work should not be exposed?" },
        evidence_notes: { label: "Contribution evidence trail", placeholder: "What money, time, receipts, source links, reviewer notes or pipeline hints support this summary?" },
        reviewer: { label: "Ledger reviewer", placeholder: "Who is allowed to check evidence before this summary is trusted more widely?" },
        next_handoff: { label: "Ledger use", placeholder: "What can agents do with this summary, and what must wait for HITL or authority checks?" },
        consent_scope: { label: "Ledger consent scope", placeholder: "What can be private, shared, public or aggregated, and when can consent be withdrawn?" },
        correction_path: { label: "Ledger correction path", placeholder: "How should disputed evidence, privacy withdrawals or wrong totals be corrected?" }
      },
      sections: {
        boundary: "Ledger Scale",
        purpose: "Why Summarise It",
        focus: "Ledger Lenses",
        public: "Shareable Contribution Summary",
        private: "Evidence Kept Out",
        evidence: "Contribution Evidence Trail",
        reviewer: "Ledger Reviewer",
        handoff: "Ledger Use",
        consent: "Ledger Consent Scope",
        correction: "Ledger Correction Path"
      }
    },
    "legal-source-trail": {
      guidance: "This is legal source sorting for agents and humans. It is not legal advice.",
      focusLegend: "Legal trail parts",
      fields: {
        record_title: { label: "Legal question or source set", placeholder: "What legal topic, source bundle, jurisdiction or risk question is being sorted?" },
        boundary_label: { label: "Jurisdiction and context", placeholder: "Which law, place, level of government, project or decision context matters?" },
        boundary_kind: { label: "Legal boundary type" },
        purpose: { label: "Research purpose", placeholder: "What should a human or agent be able to check, compare or ask after reading this?" },
        public_summary: { label: "Plain-language issue", placeholder: "What is the public-safe issue or question, without pretending to give advice?" },
        private_boundary: { label: "Legal limits and exclusions", placeholder: "What is private, privileged, uncertain, risky, culturally governed or outside this source trail?" },
        evidence_notes: { label: "Sources to check", placeholder: "What Acts, regulations, cases, policies, submissions, URLs, dates or excerpts should be checked?" },
        reviewer: { label: "Human legal reviewer", placeholder: "Who should review this before it informs advice-like claims or public action?" },
        next_handoff: { label: "Agent research handoff", placeholder: "What can an agent retrieve, compare, summarise or flag, and where must it stop?" },
        consent_scope: { label: "Source-use scope", placeholder: "What can be quoted, summarised, kept private or escalated for professional review?" },
        correction_path: { label: "Source correction path", placeholder: "How should stale law, bad citations, doubts or new sources be corrected?" }
      },
      sections: {
        boundary: "Jurisdiction And Context",
        purpose: "Research Purpose",
        focus: "Legal Trail Parts",
        public: "Plain-Language Issue",
        private: "Legal Limits And Exclusions",
        evidence: "Sources To Check",
        reviewer: "Human Legal Reviewer",
        handoff: "Agent Research Handoff",
        consent: "Source-Use Scope",
        correction: "Source Correction Path"
      }
    },
    "media-assets": {
      guidance: "This is provenance for assets, releases, gear and approvals, not a generic project note.",
      focusLegend: "Media asset lanes",
      fields: {
        record_title: { label: "Asset set or release name", placeholder: "What media bundle, shoot, design set, gear list, release or campaign asset is this?" },
        boundary_label: { label: "Project and release boundary", placeholder: "Which project, event, crew, channel, release window or shared gear boundary matters?" },
        boundary_kind: { label: "Asset boundary type" },
        purpose: { label: "Asset purpose", placeholder: "What should these assets help create, publish, archive, coordinate or prove?" },
        public_summary: { label: "Release-ready summary", placeholder: "What can be safely said or published about this asset set after approval?" },
        private_boundary: { label: "Do not release", placeholder: "What source files, people, licences, locations, drafts, prompts or private notes must not go public?" },
        evidence_notes: { label: "Provenance and licence notes", placeholder: "What files, owners, licences, AI-use notes, consent notes, dates or gear records support this asset?" },
        reviewer: { label: "Approval steward", placeholder: "Who can clear the asset for use, publication, edit, remix or archive?" },
        next_handoff: { label: "Production handoff", placeholder: "What can an agent resize, caption, catalogue, draft or prepare, and what needs approval?" },
        consent_scope: { label: "Media consent scope", placeholder: "Where can this asset be used, by whom, under what licence or approval limit?" },
        correction_path: { label: "Asset correction path", placeholder: "How should takedowns, licence mistakes, credit fixes or consent withdrawals be handled?" }
      },
      sections: {
        boundary: "Project And Release Boundary",
        purpose: "Asset Purpose",
        focus: "Media Asset Lanes",
        public: "Release-Ready Summary",
        private: "Do Not Release",
        evidence: "Provenance And Licence Notes",
        reviewer: "Approval Steward",
        handoff: "Production Handoff",
        consent: "Media Consent Scope",
        correction: "Asset Correction Path"
      }
    },
    "sovereign-space-node": {
      guidance: "This starts as a private place-node for a human home or personal environment, not a public sensor map.",
      focusLegend: "Sovereign node layers",
      fields: {
        record_title: { label: "Private space node name", placeholder: "What home, room, studio, workspace, garden, vehicle or personal place-node is this?" },
        boundary_label: { label: "Private place boundary", placeholder: "What physical, digital, emotional or environmental boundary should this node respect?" },
        boundary_kind: { label: "Node boundary type" },
        purpose: { label: "Node purpose", placeholder: "What should this node help the owner sense, remember, automate, protect or coordinate?" },
        public_summary: { label: "Optional mesh summary", placeholder: "If this ever joins a mesh, what minimal non-sensitive summary could be shared?" },
        private_boundary: { label: "Private sensorium limits", placeholder: "What room, body, household, location, schedule, device or sensitive signal must stay private?" },
        evidence_notes: { label: "Environment and device hints", placeholder: "What maps, devices, routines, sensor hints, constraints or source notes might help later?" },
        reviewer: { label: "Owner or device steward", placeholder: "Who is allowed to review this node before any sync, automation or public summary?" },
        next_handoff: { label: "Local agent actions", placeholder: "What can an agent plan, remind, simulate or prepare locally, and what needs owner approval?" },
        consent_scope: { label: "Node consent scope", placeholder: "What can be used locally, shared to a mesh, kept offline or withdrawn?" },
        correction_path: { label: "Node review path", placeholder: "How should the owner correct, pause, disconnect, replace or delete node context?" }
      },
      sections: {
        boundary: "Private Place Boundary",
        purpose: "Node Purpose",
        focus: "Sovereign Node Layers",
        public: "Optional Mesh Summary",
        private: "Private Sensorium Limits",
        evidence: "Environment And Device Hints",
        reviewer: "Owner Or Device Steward",
        handoff: "Local Agent Actions",
        consent: "Node Consent Scope",
        correction: "Node Review Path"
      }
    },
    "sensorium-place-pack": {
      guidance: "This is for shared place memory and environmental context. It needs more care than a normal project note.",
      focusLegend: "Place pack layers",
      fields: {
        record_title: { label: "Place pack name", placeholder: "What place, street, beach, island, catchment, venue, route or local system is being packed?" },
        boundary_label: { label: "Place boundary", placeholder: "What physical, ecological, cultural or infrastructure boundary defines this place pack?" },
        boundary_kind: { label: "Place boundary type" },
        purpose: { label: "Place-pack purpose", placeholder: "What should humans or authorised agents understand about this place?" },
        public_summary: { label: "Public place summary", placeholder: "What can be safely shared about the place without exposing sensitive context?" },
        private_boundary: { label: "Sensitive place context", placeholder: "What household, cultural, ecological, vulnerable-location or private route context needs authority first?" },
        evidence_notes: { label: "Place sources and signals", placeholder: "What maps, photos, local observations, ecological notes, infrastructure records or source links matter?" },
        reviewer: { label: "Place steward", placeholder: "Who should review this place pack before wider use or mesh sync?" },
        next_handoff: { label: "Place-agent handoff", placeholder: "What can an agent summarise, map, monitor, draft or ask about next?" },
        consent_scope: { label: "Place consent scope", placeholder: "What can be local, shared, public, culturally governed, aggregated or withdrawn?" },
        correction_path: { label: "Place correction path", placeholder: "How should local corrections, cultural concerns, ecological updates or takedowns be handled?" }
      },
      sections: {
        boundary: "Place Boundary",
        purpose: "Place-Pack Purpose",
        focus: "Place Pack Layers",
        public: "Public Place Summary",
        private: "Sensitive Place Context",
        evidence: "Place Sources And Signals",
        reviewer: "Place Steward",
        handoff: "Place-Agent Handoff",
        consent: "Place Consent Scope",
        correction: "Place Correction Path"
      }
    },
    "living-boundary-map": {
      guidance: "This maps useful civic boundaries such as islands, catchments, food systems and disaster corridors.",
      focusLegend: "Boundary lenses",
      fields: {
        record_title: { label: "Living boundary name", placeholder: "What island, catchment, corridor, food bowl, bioregion or civic boundary is being mapped?" },
        boundary_label: { label: "Boundary description", placeholder: "What edges, overlaps, communities, waters, roads, institutions or systems define the boundary?" },
        boundary_kind: { label: "Boundary map type" },
        purpose: { label: "Why this boundary matters", placeholder: "What problem, planning need, care network, risk or opportunity does this boundary reveal?" },
        public_summary: { label: "Public boundary summary", placeholder: "What can residents or civic teams safely understand from the map?" },
        private_boundary: { label: "Sensitive map limits", placeholder: "What cultural, ecological, household, security or vulnerable-location data should not be exposed?" },
        evidence_notes: { label: "Boundary evidence", placeholder: "What maps, local knowledge, datasets, histories, sources or authority notes support the boundary?" },
        reviewer: { label: "Boundary reviewer", placeholder: "Who should check the boundary before it is used in public civic architecture?" },
        next_handoff: { label: "Map next steps", placeholder: "What can an agent compare, draft, map, source-check or prepare next?" },
        consent_scope: { label: "Boundary consent scope", placeholder: "What can be public, local-only, culturally governed, aggregated or revised?" },
        correction_path: { label: "Boundary correction path", placeholder: "How should disputed edges, missing sources, cultural concerns or new evidence be corrected?" }
      },
      sections: {
        boundary: "Boundary Description",
        purpose: "Why This Boundary Matters",
        focus: "Boundary Lenses",
        public: "Public Boundary Summary",
        private: "Sensitive Map Limits",
        evidence: "Boundary Evidence",
        reviewer: "Boundary Reviewer",
        handoff: "Map Next Steps",
        consent: "Boundary Consent Scope",
        correction: "Boundary Correction Path"
      }
    },
    "local-civic-front": {
      guidance: "This stitches a local public front together from profiles, projects, notices, legal sources and ledgers.",
      focusLegend: "Civic front modules",
      fields: {
        record_title: { label: "Civic front name", placeholder: "What council, electorate, island, suburb, ward, catchment or local front is being assembled?" },
        boundary_label: { label: "Public front boundary", placeholder: "What people, places, institutions, issues or local systems belong in this front?" },
        boundary_kind: { label: "Civic front boundary type" },
        purpose: { label: "Public front purpose", placeholder: "What should this civic front help residents, organisers, agents or reviewers coordinate?" },
        public_summary: { label: "Front-door public summary", placeholder: "What can a visitor safely understand about this local civic front?" },
        private_boundary: { label: "Private and permissioned layers", placeholder: "What records stay private, permissioned, culturally governed or behind human review?" },
        evidence_notes: { label: "Linked source modules", placeholder: "What profiles, noticeboards, project records, legal trails, ledgers or place packs support this front?" },
        reviewer: { label: "Front steward group", placeholder: "Who can review the front before public use or wider aggregation?" },
        next_handoff: { label: "Civic front handoff", placeholder: "What should agents prepare, compare, summarise, route or flag for the human team?" },
        consent_scope: { label: "Front consent scope", placeholder: "What can be public, local-only, permissioned or aggregated upward?" },
        correction_path: { label: "Front correction path", placeholder: "How should residents, stewards or record owners request corrections or withdrawals?" }
      },
      sections: {
        boundary: "Public Front Boundary",
        purpose: "Public Front Purpose",
        focus: "Civic Front Modules",
        public: "Front-Door Public Summary",
        private: "Private And Permissioned Layers",
        evidence: "Linked Source Modules",
        reviewer: "Front Steward Group",
        handoff: "Civic Front Handoff",
        consent: "Front Consent Scope",
        correction: "Front Correction Path"
      }
    }
  };

  function buildModuleRecord(data, module) {
    const title = getValue(data, "record_title", module.title);
    const consentScope = getValue(data, "consent_scope", "No sharing scope recorded in this draft.");
    const correctionPath = getValue(data, "correction_path", "No review or correction path recorded in this draft.");
    const visibility = getValue(data, "visibility", module.visibility);
    const focus = getAll(data, "focus_areas");

    const meta = {
      schema: module.schema,
      status: "exploratory_draft",
      primary_layer: module.primaryLayer,
      layers: module.layers,
      default_starting_layer: module.defaultStartingLayer,
      scale_path: module.scalePath,
      boundary_kind: getValue(data, "boundary_kind", module.boundaryKind),
      capability_kind: module.capabilityKind,
      capability_scope: module.capabilityScope,
      implementation_status: "browser_local_static_builder",
      visibility,
      created: today,
      updated: today,
      review_status: getValue(data, "review_status", "needs_human_review"),
      source_repo: module.sourceRepo,
      source_builder: module.sourceBuilder,
      purple_translation: module.purpleTranslation,
      consent_scope: consentScope,
      consent_model: getValue(data, "consent_model", "plain-language-purpose-bound-revocable"),
      correction_path: correctionPath,
      confidence: getValue(data, "confidence", "draft")
    };

    return [
      frontmatter(meta),
      "",
      `# ${title}`,
      "",
      `## ${module.fieldText?.sections?.boundary || "Boundary Or Place"}`,
      paragraph(getValue(data, "boundary_label")),
      "",
      `## ${module.fieldText?.sections?.purpose || "Purpose"}`,
      paragraph(getValue(data, "purpose")),
      "",
      `## ${module.fieldText?.sections?.focus || "Focus Areas"}`,
      bulletList(focus),
      "",
      `## ${module.fieldText?.sections?.public || "Public Summary"}`,
      paragraph(getValue(data, "public_summary")),
      "",
      `## ${module.fieldText?.sections?.private || "Private Or Permissioned Boundary"}`,
      paragraph(getValue(data, "private_boundary")),
      "",
      `## ${module.fieldText?.sections?.evidence || "Evidence Or Source Notes"}`,
      paragraph(getValue(data, "evidence_notes")),
      "",
      `## ${module.fieldText?.sections?.reviewer || "Reviewer Or Steward"}`,
      paragraph(getValue(data, "reviewer")),
      "",
      `## ${module.fieldText?.sections?.handoff || "Agent Use Or Handoff"}`,
      paragraph(getValue(data, "next_handoff")),
      "",
      `## ${module.fieldText?.sections?.consent || "Consent Scope"}`,
      paragraph(consentScope),
      "",
      `## ${module.fieldText?.sections?.correction || "Review Or Correction Path"}`,
      paragraph(correctionPath),
      "",
      "## Guardrail",
      module.guardrail
    ].join("\n");
  }

  const builders = {
    "private-profile": {
      filename: "profile.md",
      title: "Private Civic Profile Builder",
      prev: ["Builder suite", "civic-twin-builders.html"],
      next: ["Private noticeboard", "p4a-builder.html?tool=private-noticeboard"],
      build: buildPrivateProfile
    },
    "noticeboard-contract": {
      filename: "public_noticeboard.md",
      title: "Public Noticeboard Builder",
      prev: ["Local crew", "p4a-builder.html?tool=local-crew-onboarding"],
      next: ["Project readiness", "p4a-builder.html?tool=project-readiness"],
      build: buildNoticeboard
    }
  };

  Object.entries(moduleConfigs).forEach(([key, module]) => {
    module.fieldText = builderFieldText[key];
    builders[key] = {
      filename: module.filename,
      title: module.title,
      prev: module.prev,
      next: module.next,
      module,
      build: (data) => buildModuleRecord(data, module)
    };
  });

  const config = builders[builderId];
  if (!config || !output) return;

  function setLeadingLabelText(container, text) {
    if (!container || !text) return;
    const textNode = Array.from(container.childNodes).find((node) => node.nodeType === Node.TEXT_NODE && node.nodeValue.trim());
    if (textNode) {
      textNode.nodeValue = `${text}\n            `;
    } else {
      container.insertBefore(document.createTextNode(`${text} `), container.firstChild);
    }
  }

  function setDefaultValue(name, value) {
    if (!value) return;
    const field = form.querySelector(`[name="${name}"]`);
    if (!field || field.type === "checkbox") return;
    field.value = value;
  }

  function applyFieldText() {
    const fieldText = config.module?.fieldText;
    if (!fieldText) return;

    const guidance = document.querySelector("[data-builder-guidance]");
    if (guidance) {
      guidance.textContent = fieldText.guidance || "";
      guidance.hidden = !fieldText.guidance;
    }

    Object.entries(fieldText.fields || {}).forEach(([name, copy]) => {
      const wrapper = form.querySelector(`[data-builder-field="${name}"]`);
      if (wrapper && copy.label) setLeadingLabelText(wrapper, copy.label);
      if (wrapper) wrapper.hidden = Boolean(copy.hidden);
      const field = form.querySelector(`[name="${name}"]`);
      if (field && copy.placeholder !== undefined) {
        field.setAttribute("placeholder", copy.placeholder);
      }
      if (field && copy.options && field.tagName === "SELECT") {
        Array.from(field.options).forEach((option) => {
          if (copy.options[option.value]) option.textContent = copy.options[option.value];
        });
      }
    });

    const focusLegend = document.querySelector("[data-builder-legend='focus_areas']");
    if (focusLegend && fieldText.focusLegend) {
      focusLegend.textContent = fieldText.focusLegend;
    }

    setDefaultValue("boundary_kind", config.module.boundaryKind);
    setDefaultValue("visibility", config.module.visibility);
  }

  function applyPageMeta() {
    if (config.title) {
      document.title = `${config.title} | P4A`;
    }

    document.querySelectorAll("[data-builder-title]").forEach((element) => {
      element.textContent = config.title || config.module?.title || element.textContent;
    });
    document.querySelectorAll("[data-builder-eyebrow]").forEach((element) => {
      element.textContent = config.module?.eyebrow || element.textContent;
    });
    document.querySelectorAll("[data-builder-file]").forEach((element) => {
      element.textContent = config.filename;
    });
    document.querySelectorAll("[data-builder-source]").forEach((element) => {
      if (config.module?.sourceUrl) {
        element.textContent = "";
        const link = document.createElement("a");
        link.href = config.module.sourceUrl;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = config.module.sourceRepo;
        element.appendChild(link);
      } else {
        element.textContent = config.module?.sourceRepo || element.textContent;
      }
    });
    document.querySelectorAll("[data-builder-guardrail]").forEach((element) => {
      element.textContent = config.module?.guardrail || element.textContent;
    });

    applyFieldText();

    const focusList = document.querySelector("[data-builder-focus-options]");
    if (focusList && config.module?.focusOptions) {
      focusList.innerHTML = config.module.focusOptions.map((value) => {
        const label = value.replace(/_/g, " ");
        return `<label><input type="checkbox" name="focus_areas" value="${value}"> ${label}</label>`;
      }).join("");
    }

    const prevLinks = document.querySelectorAll("[data-builder-prev]");
    const nextLinks = document.querySelectorAll("[data-builder-next]");
    if (config.prev) {
      prevLinks.forEach((link) => {
        link.href = config.prev[1];
        link.textContent = `Previous: ${config.prev[0]}`;
      });
    }
    if (config.next) {
      nextLinks.forEach((link) => {
        link.href = config.next[1];
        link.textContent = `Next: ${config.next[0]}`;
      });
    }
  }

  function saveState() {
    const state = {};
    form.querySelectorAll("input, textarea, select").forEach((field) => {
      if (!field.name) return;
      if (field.type === "checkbox") {
        if (!Array.isArray(state[field.name])) state[field.name] = [];
        if (field.checked) state[field.name].push(field.value);
      } else {
        state[field.name] = field.value;
      }
    });
    sessionStorage.setItem(storageKey, JSON.stringify(state));
  }

  function restoreState() {
    const raw = sessionStorage.getItem(storageKey);
    if (!raw) return;
    try {
      const state = JSON.parse(raw);
      form.querySelectorAll("input, textarea, select").forEach((field) => {
        if (!field.name || state[field.name] === undefined) return;
        if (field.type === "checkbox") {
          field.checked = Array.isArray(state[field.name]) && state[field.name].includes(field.value);
        } else {
          field.value = state[field.name];
        }
      });
    } catch (error) {
      sessionStorage.removeItem(storageKey);
    }
  }

  function refresh(shouldSave = true) {
    const data = readForm();
    output.value = config.build(data);
    if (downloadButton) downloadButton.dataset.filename = config.filename;
    if (shouldSave) saveState();
  }

  async function copyMarkdown() {
    try {
      await navigator.clipboard.writeText(output.value);
      setStatus("Markdown copied to clipboard.");
    } catch (error) {
      output.focus();
      output.select();
      const copied = document.execCommand("copy");
      setStatus(copied ? "Markdown copied to clipboard." : "Copy did not work in this browser. Select the preview and copy it manually.");
    }
  }

  function downloadMarkdown() {
    const filename = downloadButton?.dataset.filename || config.filename;
    const blob = new Blob([output.value], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
    setStatus(`Downloaded ${filename}.`);
  }

  function clearBuilder() {
    form.reset();
    sessionStorage.removeItem(storageKey);
    refresh(false);
    setStatus("Cleared this browser session draft.");
  }

  applyPageMeta();
  restoreState();
  refresh(false);
  form.addEventListener("input", () => refresh(true));
  form.addEventListener("change", () => refresh(true));
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    refresh(true);
    setStatus("Markdown preview updated.");
  });
  copyButton?.addEventListener("click", copyMarkdown);
  downloadButton?.addEventListener("click", downloadMarkdown);
  clearButton?.addEventListener("click", clearBuilder);
})();
