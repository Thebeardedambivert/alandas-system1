import os

# We will read generate_tiered_presentation.py, insert Slide 8 in HTML and PPTX, update all indices and footers, and save.
with open("scripts/generate_tiered_presentation.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. HTML UPDATES
# Replace slide footers for 1..7:
for i in range(1, 8):
    text = text.replace(f"SLIDE {i:02d} / 18", f"SLIDE {i:02d} / 19")

# Replace slides 8..18 with 9..19 in reverse order
for i in range(18, 7, -1):
    text = text.replace(f'data-slide="{i}"', f'data-slide="{i+1}"')
    text = text.replace(f"SLIDE {i:02d} / 18", f"SLIDE {i+1:02d} / 19")
    text = text.replace(f"<!-- SLIDE {i}:", f"<!-- SLIDE {i+1}:")

# Update slide counter display in HTML
text = text.replace('1 / 18</span>', '1 / 19</span>')

# HTML Slide 8 content
html_slide_8 = """    <!-- =================================================================== -->
    <!-- SLIDE 8: Waterfall Enrichment Engine -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="8">
      <div class="slide-header">
        <div class="kicker">Tier 1 Lead Intelligence // Waterfall Architecture</div>
        <h2 class="slide-title">Waterfall Enrichment: "Cheapest Tool First"</h2>
        <p class="slide-subtitle">
          Each tool only gets what the last one missed. How Alandas achieves a ~92% decision-maker find rate with direct WhatsApp numbers at an 87% data cost reduction.
        </p>
      </div>

      <div class="slide-body">
        <!-- 5-Stage Waterfall Cards -->
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 20px;">
          <!-- Stage 0 -->
          <div class="card accent-olive" style="padding: 20px 18px;">
            <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--forest);">STAGE 0 // €0.00 (FREE)</div>
            <h4 style="font-family: var(--font-display); font-size: 18px; font-weight: 700; margin: 6px 0 8px 0;">§ 5 TMG Impressum</h4>
            <p style="font-size: 13px; color: var(--text-muted); line-height: 1.4; margin-bottom: 10px;">Scrapes German legal notice (/impressum) for managing director & email.</p>
            <div style="background: var(--olive-light); padding: 8px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; color: var(--forest);">
              Finds 48% (480/1k)<br><span style="font-weight: 400; color: var(--text-muted);">520 Misses Passed Down ➔</span>
            </div>
          </div>

          <!-- Stage 1 -->
          <div class="card" style="padding: 20px 18px; border-top: 4px solid var(--olive);">
            <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--olive);">STAGE 1 // €0.005 / LOOKUP</div>
            <h4 style="font-family: var(--font-display); font-size: 18px; font-weight: 700; margin: 6px 0 8px 0;">GitLeads / Apollo</h4>
            <p style="font-size: 13px; color: var(--text-muted); line-height: 1.4; margin-bottom: 10px;">Queries cheap bulk database only for the 520 missed venues.</p>
            <div style="background: var(--card-alt); padding: 8px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; color: var(--olive);">
              Finds 24% (+240)<br><span style="font-weight: 400; color: var(--text-muted);">280 Misses Passed Down ➔</span>
            </div>
          </div>

          <!-- Stage 2 -->
          <div class="card" style="padding: 20px 18px; border-top: 4px solid var(--ochre);">
            <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--ochre);">STAGE 2 // €0.02 / LOOKUP</div>
            <h4 style="font-family: var(--font-display); font-size: 18px; font-weight: 700; margin: 6px 0 8px 0;">Prospeo / Origami</h4>
            <p style="font-size: 13px; color: var(--text-muted); line-height: 1.4; margin-bottom: 10px;">Deep email scraper & social MX permutation for stubborn misses.</p>
            <div style="background: var(--ochre-light); padding: 8px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; color: var(--ochre-dark);">
              Finds 18% (+180)<br><span style="font-weight: 700;">~90% Total Email Find Rate</span>
            </div>
          </div>

          <!-- Stage 3 -->
          <div class="card accent-ochre" style="padding: 20px 18px;">
            <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--ochre-dark);">STAGE 3 // €0.05 / MATCH</div>
            <h4 style="font-family: var(--font-display); font-size: 18px; font-weight: 700; margin: 6px 0 8px 0;">LeadMagic Mobile</h4>
            <p style="font-size: 13px; color: var(--text-muted); line-height: 1.4; margin-bottom: 10px;">Direct mobile & WhatsApp lookup on top of found decision-makers.</p>
            <div style="background: var(--card-alt); padding: 8px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; color: var(--ochre-dark);">
              Finds 650 Mobiles<br><span style="font-weight: 400; color: var(--text-muted);">Enables WhatsApp B2B Sales</span>
            </div>
          </div>

          <!-- Stage 4 -->
          <div class="card accent-forest" style="padding: 20px 18px;">
            <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--forest);">VALIDATE // €0.002 / CHECK</div>
            <h4 style="font-family: var(--font-display); font-size: 18px; font-weight: 700; margin: 6px 0 8px 0;">MillionVerifier</h4>
            <p style="font-size: 13px; color: var(--text-muted); line-height: 1.4; margin-bottom: 10px;">Strict deliverability gate. Risky / Catch-All filtered out.</p>
            <div style="background: var(--forest-light); padding: 8px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; color: var(--forest);">
              &lt; 1.5% Bounce Rate<br><span style="font-weight: 400; color: var(--forest);">100% Inbound Reputation Safe</span>
            </div>
          </div>
        </div>

        <!-- Comparison Bar & Unit Economics -->
        <div class="grid-2">
          <div class="card" style="padding: 20px 24px;">
            <div style="font-family: var(--font-mono); font-size: 12px; color: var(--text-subtle); font-weight: 700;">UNIT ECONOMICS COMPARISON (PER 1,000 LEADS)</div>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14.5px;">
              <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 8px 0; font-weight: 600;">Naive Flat Scraping (Run Premium on all 1,000)</td>
                <td style="text-align: right; color: #D9534F; font-weight: 700; font-family: var(--font-mono);">€80.00</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 8px 0; font-weight: 600;">Waterfall Enrichment (Impressum ➔ GitLeads ➔ Prospeo ➔ Verifier)</td>
                <td style="text-align: right; color: var(--forest); font-weight: 700; font-family: var(--font-mono);">€10.00</td>
              </tr>
              <tr>
                <td style="padding: 8px 0; font-weight: 700; color: var(--olive);">Client Net Savings with Waterfall</td>
                <td style="text-align: right; color: var(--forest); font-weight: 800; font-family: var(--font-mono);">87% REDUCTION</td>
              </tr>
            </table>
          </div>

          <div class="card accent-olive" style="padding: 20px 24px;">
            <div style="font-family: var(--font-mono); font-size: 12px; color: var(--olive); font-weight: 700;">THE GERMAN § 5 TMG ADVANTAGE & TEMPORAL RESILIENCE</div>
            <p style="font-size: 14.5px; line-height: 1.5; margin-top: 8px; color: var(--text-main);">
              Under German law (§ 5 TMG), every commercial site must maintain an Impressum with the legal owner's full name, address, and official email. By making Stage 0 a free scraper, <strong>Alandas resolves half of all leads for €0</strong>. Each waterfall step runs as an isolated Temporal Activity with retry policies, ensuring zero dropped leads if an API times out.
            </p>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 08 / 19</div>
      </div>
    </div>
"""

target_html_anchor = "    <!-- =================================================================== -->\n    <!-- SLIDE 9: Tier 2 Architecture -->"
text = text.replace(target_html_anchor, html_slide_8 + "\n" + target_html_anchor)

# 2. PPTX UPDATES
# Update total_slides=18 default:
text = text.replace("total_slides=18", "total_slides=19")

# Update footer calls for s1 to s7:
for i in range(1, 8):
    text = text.replace(f"add_footer(s{i}, {i})", f"add_footer(s{i}, {i}, total_slides=19)")

# Now let's handle the PPTX slides from slide 8 to 18 (which will become s9 to s19).
# Let's inspect the exact PPTX section replacement:
old_pptx_section_start = "    # Slide 8: Tier 2 Architecture"

new_pptx_slides = """    # Slide 8: Waterfall Enrichment Engine
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "07 // Tier 1 Lead Intelligence", "Waterfall Enrichment: Cheapest Tool First",
               "Each tool only gets what the last one missed: How Alandas achieves ~92% contact find rates with verified WhatsApp numbers at an 87% data cost reduction.")
    add_footer(s8, 8, total_slides=19)

    # 5 Waterfall Stage Cards across the top
    wf_stages = [
        ("STAGE 0 // €0.00", "§ 5 TMG Impressum", "Scrapes German legal notice (/impressum) for managing director & email.", "Finds 48% (480/1k)\\n520 Passed Down ➔", COLOR_FOREST),
        ("STAGE 1 // €0.005", "GitLeads / Apollo", "Bulk database query applied only to the 520 missed cafe records.", "Finds 24% (+240)\\n280 Passed Down ➔", COLOR_OLIVE),
        ("STAGE 2 // €0.02", "Prospeo / Origami", "Deep email scraper & social MX permutation for stubborn misses.", "Finds 18% (+180)\\n~90% Total Email Find", COLOR_OCHRE),
        ("STAGE 3 // €0.05", "LeadMagic Mobile", "Direct mobile & WhatsApp lookup for found cafe owners and baristas.", "Finds 650 Mobiles\\nEnables WhatsApp B2B", COLOR_OCHRE),
        ("VALIDATE // €0.002", "MillionVerifier", "Strict deliverability gate. Risky / Catch-All filtered out before outreach.", "< 1.5% Bounce Rate\\nInbound Domain Safe", COLOR_FOREST)
    ]
    w_wf = Inches(2.20)
    gap_wf = Inches(0.18)
    for i, (tag, name, desc, stat, col) in enumerate(wf_stages):
        left_c = Inches(0.8) + i * (w_wf + gap_wf)
        create_card(s8, left_c, Inches(2.0), w_wf, Inches(2.6), bg_color=COLOR_CARD_BG)
        tb = s8.shapes.add_textbox(left_c + Inches(0.15), Inches(2.15), w_wf - Inches(0.30), Inches(2.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p0 = tf.paragraphs[0]
        p0.text = tag.upper()
        p0.font.name = FONT_BODY
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(3)
        p1 = tf.add_paragraph()
        p1.text = name
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(5)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.space_after = Pt(6)
        p3 = tf.add_paragraph()
        p3.text = stat
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10)
        p3.font.bold = True
        p3.font.color.rgb = col

    # Bottom 2 Cards: Unit Economics & German Legal Advantage
    add_formatted_card(s8, Inches(0.8), Inches(4.85), Inches(5.68), Inches(1.95), "UNIT ECONOMICS", "87% Data Acquisition Cost Reduction", [
        "Naive Flat Approach: $0.08 × 1,000 = $80.00 (High bounce risk & wasted spend).",
        "Waterfall Pipeline: €0 + €2.60 + €5.60 + €1.80 = €10.00 per 1,000 enriched leads.",
        "Net Result: 87% lower customer data cost while achieving ~92% verified contact rate."
    ], tag_color=COLOR_OLIVE, title_size=17, bullet_size=11)

    add_formatted_card(s8, Inches(6.85), Inches(4.85), Inches(5.68), Inches(1.95), "ARCHITECTURAL ADVANTAGE", "German § 5 TMG & Temporal Activity Isolation", [
        "§ 5 TMG Legal Impressum: German law requires commercial sites to publish owner name & email. Stage 0 resolves 48% of leads for €0.",
        "Temporal Durability: Each stage runs as an isolated activity with exponential backoff. If Apollo times out, workflow cascades to Prospeo.",
        "Reputation Defense: MillionVerifier keeps sender bounce rate < 1.5%, protecting sending domains from Google Workspace blacklisting."
    ], tag_color=COLOR_OCHRE, title_size=17, bullet_size=11)

    # Slide 9: Tier 2 Architecture
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "08 // Tier 2 Architecture", "Professional Revenue Intelligence Blueprint",
               "Introducing durable domain workflows, structured Policy Engines, Decision Contracts, and audit trails.")
    add_footer(s9, 9, total_slides=19)
    add_formatted_card(s9, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "SYSTEM BLUEPRINT", "The Governed Architecture", [
        "Temporal Domain Workflows: Explicit services for Acquisition, Marketing & RevOps.",
        "Domain Logic Layer: Decouples business rules from external transport APIs.",
        "Policy Engine: Mathematical verification of budgets, pricing, and messaging limits.",
        "Decision Contracts: Typed JSON contracts required for all AI recommendations.",
        "Post-Action Verification: System re-queries external APIs to verify state change.",
        "PostgreSQL + Audit Traces: Full OpenTelemetry tracing across all operations."
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)
    add_formatted_card(s9, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "THE ARCHITECTURAL LEAP", "From Automation to Governed Intelligence", [
        "In Tier 1, Temporal executes commands. In Tier 2, the system must justify decisions before execution.",
        "Policy Engine: Independent rules governing budget, pricing, discounts, and cadence.",
        "Decision Contracts: Every AI recommendation is validated against schemas before execution.",
        "Selective LangGraph: Bounded reasoning graphs used strictly for complex evaluations (e.g. ad creative analysis), never for the whole app.",
        "Auditability: In any dispute, the customer has an exact chronological record of every AI decision."
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # Slide 10: Tier 2 in Action
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "09 // Tier 2 Governance in Action", "The Decision Contract Walkthrough",
               "Example: AI recommends a 30% Meta Ad budget increase. How the system governs this safely.")
    add_footer(s10, 10, total_slides=19)
    add_formatted_card(s10, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "8-STAGE GOVERNANCE GATE", "Executing +30% Ad Budget Increase", [
        "1. AI Recommendation: 'Increase Berlin Brunch Ad budget from €30 to €39/day (+30%).'",
        "2. Validity Check: Is campaign ID active? Does the ad set exist?",
        "3. Eligibility Check: Has campaign run > 7 days? Is ROAS > 3.0x? (Yes: 4.2x).",
        "4. Policy Evaluation: Does €39 exceed the daily ceiling (€50)? (Compliant).",
        "5. Approval Threshold: Does budget delta > €5 require human sign-off? (Policy: YES).",
        "6. Human Approval: Sidy receives 1-tap notification: [Approve +€9/day].",
        "7. Execute & Verify: Meta API called; system re-queries Meta to confirm new budget = €39.00.",
        "8. Audit Logging: Immutable record written with reasoning, timestamp, and Sidy's ID."
    ], tag_color=COLOR_OCHRE, title_size=18, bullet_size=11.5)
    add_formatted_card(s10, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "COMMERCIAL VALUE", "What the Customer Is Actually Paying For", [
        "Zero Runaway Spend: An AI bug or hallucination can never drain the customer's bank account or ad budget.",
        "Zero Pricing Leaks: B2B wholesale volume discounts follow strict mathematical tables, not model whims.",
        "Regulatory Compliance: Strict policy checks guarantee botanical and organic labeling compliance under German food regulations.",
        "Complete Auditability: Exact chronological record of every AI decision for investors and accountants."
    ], tag_color=COLOR_OLIVE, title_size=18, bullet_size=12)

    # Slide 11: Tier 3 Architecture
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10 // Tier 3 Architecture", "Autonomous Revenue Platform Blueprint",
               "When commercial scale reaches 100+ accounts, the system transitions into an autonomous closed-loop revenue engine.")
    add_footer(s11, 11, total_slides=19)
    add_formatted_card(s11, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "SYSTEM BLUEPRINT", "The Autonomous Platform", [
        "Temporal Runtime & Event Bus: Durable event backbone coordinating all domain agents.",
        "Domain Specialist Agents: Dedicated agents for Acquisition, Creative/Ads, and RevOps.",
        "Shared Revenue State: Central real-time graph of customer accounts, consumption & LTV.",
        "Policy Engine & Enterprise RAG: Ingestion of blend sensory sheets, cafe notes & market trends.",
        "MCP Capability Layer: Standardized protocol boundaries for tool invocation across services.",
        "Closed-Loop Learning: Automated feedback connecting customer refills back into ad bidding."
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)
    add_formatted_card(s11, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "EARNED COMPLEXITY", "When Is Tier 3 Justified?", [
        "Cross-Domain Signals: Cafe reorder frequency directly triggers creative testing on Meta Ads without human intervention.",
        "MCP Dynamic Capabilities: Agents dynamically discover tools and query inventory, CRM, and logistics via standardized protocol boundaries.",
        "Continuous Experimentation: System formulates hypotheses, executes test campaigns, and measures LTV impact.",
        "True Scale: Operates 200+ partner accounts across multiple countries with zero additional administrative personnel."
    ], tag_color=COLOR_FOREST, title_size=20, bullet_size=12.5)

    # Slide 12: Tier 3 Flywheel
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "11 // Tier 3 Operational Flywheel", "The Closed-Loop Commercial Flywheel",
               "Connecting top-of-funnel acquisition directly to post-purchase retention and lifetime value in a continuous feedback loop.")
    add_footer(s12, 12, total_slides=19)
    flywheel = [
        ("STAGE 01", "Market Signals", ["Scrapes German dining clusters", "Tracks Instagram engagement", "Identifies active beverage buyers"]),
        ("STAGE 02", "€19 Trial Box", ["Automated qualification routes heavy borosilicate teapot", "Verified cafe baristas receive kit", "100% credited against Starter Crate"]),
        ("STAGE 03", "Starter Crate", ["€249 Starter Crate deployed", "Turnkey counter Teebar installed", "Barista brewing cheat sheets automated"]),
        ("STAGE 04", "Predictive Refills", ["Day-25 consumption alerts", "1-click WhatsApp reorders", "Automated Dolibarr PDF invoicing"])
    ]
    w_fw = Inches(2.72)
    gap_fw = Inches(0.28)
    for i, (tag, title, bullets) in enumerate(flywheel):
        add_formatted_card(s12, Inches(0.8) + i * (w_fw + gap_fw), Inches(2.0), w_fw, Inches(3.2), tag, title, bullets, title_size=16, bullet_size=11)

    create_card(s12, Inches(0.8), Inches(5.4), Inches(11.733), Inches(1.4), bg_color=COLOR_LIGHT_BG)
    tb = s12.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.333), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "THE AUTONOMOUS FEEDBACK LOOP // WHAT MAKES IT FLYWHEEL"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_OLIVE
    p1 = tf.add_paragraph()
    p1.text = "Actual cafe replenishment rates feed back into the Ads Agent. If brunch cafes in Munich reorder Earl Grey 2x faster than average, the system automatically writes new ad copy, allocates budget to Munich brunch clusters, and tests new creative hypotheses without human intervention."
    p1.font.name = FONT_BODY
    p1.font.size = Pt(12)
    p1.font.color.rgb = COLOR_TEXT_MAIN

    # Slide 13: Framework Comparison Matrix
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "12 // System Design Benchmark", "Master Architectural Comparison Matrix",
               "Clear component separation across tiers: Customer capability scales without unnecessary infrastructure bloat.")
    add_footer(s13, 13, total_slides=19)
    add_formatted_card(s13, Inches(0.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 1 // ESSENTIAL", "Durable Automation", [
        "Runtime: Temporal + Python/TS",
        "Orchestration: Temporal Workflows",
        "Intelligence: Direct LLM API",
        "Safety: Human Approval Gate",
        "Integrations: Direct REST APIs",
        "Database: PostgreSQL Core",
        "Caching / Bus: None (Zero Bloat)",
        "Audit: PostgreSQL Ledgers",
        "Commercial Value: Saves 15h/week"
    ], tag_color=COLOR_OLIVE, title_size=17, bullet_size=11.5)
    add_formatted_card(s13, Inches(4.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 2 // PROFESSIONAL", "Governed Intelligence", [
        "Runtime: Temporal Runtime",
        "Orchestration: Temporal + Selective LangGraph",
        "Intelligence: Policy Engines + Schemas",
        "Safety: Decision Contracts + Human Gate",
        "Integrations: Direct APIs + Verifiers",
        "Database: PostgreSQL + Audit Store",
        "Caching / Bus: None needed at this scale",
        "Audit: OpenTelemetry Traces",
        "Commercial Value: Churn prevention"
    ], tag_color=COLOR_OCHRE, title_size=17, bullet_size=11.5)
    add_formatted_card(s13, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 3 // AUTONOMOUS", "Autonomous Platform", [
        "Runtime: Temporal Platform",
        "Orchestration: Domain Agents + Temporal",
        "Intelligence: Enterprise RAG + Learning",
        "Safety: Automated Circuit Breakers",
        "Integrations: Model Context Protocol (MCP)",
        "Database: PostgreSQL + Shared State Graph",
        "Caching / Bus: Event PubSub Layer",
        "Audit: Comprehensive System Telemetry",
        "Commercial Value: Enterprise autonomy"
    ], tag_color=COLOR_FOREST, title_size=17, bullet_size=11.5)

    # Slide 14: Autonomy Spectrum
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "13 // Operational Governance", "The Autonomy Spectrum & Blast Radius Containment",
               "The difference between tiers is not merely more code. It is the structured management of risk and blast radius across the business.")
    add_footer(s14, 14, total_slides=19)
    add_formatted_card(s14, Inches(0.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 1 // ZERO BLAST RADIUS", "Human-Directed", [
        "Machine only reads public data & gathers facts.",
        "Every prospect message, sample box dispatch, and proposal requires human click.",
        "Zero risk of bot hallucinating botanical claims or unauthorized pricing.",
        "Safe for early-stage founders and fragile brand trust."
    ], tag_color=COLOR_OLIVE, title_size=17, bullet_size=12)
    add_formatted_card(s14, Inches(4.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 2 // STRICT BOUNDS", "Human-Governed", [
        "Standard repetitive tasks execute autonomously (e.g. Day-20 refill check-in).",
        "High-risk actions (pricing, discounts, budget delta > €5) trigger Decision Contracts.",
        "Human approval required for any action outside policy bounds.",
        "High leverage with guaranteed safety nets."
    ], tag_color=COLOR_OCHRE, title_size=17, bullet_size=12)
    add_formatted_card(s14, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 3 // MATHEMATICALLY BOUND", "Policy-Governed", [
        "Machine autonomously shifts ad spend, rotates blends, and optimizes schedules.",
        "Protected by automated circuit breakers: any sudden metric spike halts system.",
        "Human executive acts as supervisor reviewing weekly performance digests.",
        "Massive operational scale with automated anomaly defense."
    ], tag_color=COLOR_FOREST, title_size=17, bullet_size=12)

    # Slide 15: Instagram Architecture
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "14 // Omnichannel Acquisition", "Instagram as a First-Class Architecture Channel",
               "Instagram is an essential acquisition channel and signal source across all three tiers — not an afterthought.")
    add_footer(s15, 15, total_slides=19)
    ig_roles = [
        ("ROLE 01", "Outbound Prospecting", ["Identifies specialty brunch cafes", "Analyzes feed interior aesthetic", "Pre-qualifies tea menu fit"]),
        ("ROLE 02", "OpenReply Inbound", ["Barista comments 'TEABAR' on reel", "Triggers instant qualification DM", "Sends €19 trial kit link in 60s"]),
        ("ROLE 03", "Marketing Signals", ["Tracks likes & comments on tea reels", "Identifies active beverage directors", "Enriches intent in Dolibarr CRM"]),
        ("ROLE 04", "Paid Acquisition", ["Meta Ads target cafe owners directly", "Drives to 1-tap WhatsApp chat", "Captures pre-paid sample orders"])
    ]
    w_ig = Inches(2.72)
    gap_ig = Inches(0.28)
    for i, (tag, title, bullets) in enumerate(ig_roles):
        add_formatted_card(s15, Inches(0.8) + i * (w_ig + gap_ig), Inches(2.0), w_ig, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE if i%2==0 else COLOR_OCHRE, title_size=17, bullet_size=12)

    # Slide 16: Instagram Across Tiers
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "15 // Channel Evolution", "How Instagram Matures Across Tiers",
               "Tier 1 has a complete, working comment-to-DM loop. Higher tiers add intelligence, governance, and cross-channel optimization.")
    add_footer(s16, 16, total_slides=19)
    table_shape = s16.shapes.add_table(6, 4, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(2.844)
    table.columns[2].width = Inches(2.844)
    table.columns[3].width = Inches(2.844)

    ig_matrix = [
        ["Dimension", "Tier 1 // Essential", "Tier 2 // Professional", "Tier 3 // Autonomous"],
        ["Comment ➔ DM", "OpenReply Keyword Triggers", "OpenReply + Context Routing", "Dynamic Intent Extraction"],
        ["Lead Qualification", "Standard 60-Sec Form", "Dynamic Gated Qualification", "Real-Time Venue Scoring"],
        ["Dolibarr CRM Sync", "Immediate Lead Card", "Lead Card + Social Score", "Full Omnichannel Identity"],
        ["Outreach Messaging", "AI-Drafted ➔ Human Approves", "Pre-Approved Policy Templates", "Autonomous Dynamic Copy"],
        ["Ad Spend Feedback", "Manual Ad Optimization", "Policy Engine Budgets (±20%)", "Closed-Loop Attribution"]
    ]
    for row_idx, row_data in enumerate(ig_matrix):
        for col_idx, cell_value in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = cell_value
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(11.5 if row_idx > 0 else 12)
            p.font.bold = (row_idx == 0 or col_idx == 0)
            if row_idx == 0:
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_OLIVE
            else:
                p.font.color.rgb = COLOR_TEXT_MAIN
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if row_idx % 2 == 1 else COLOR_LIGHT_BG

    # Slide 17: Tech Stack Evolution
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "16 // Lifecycle Engineering", "Evolving the Architecture Without Rewriting",
               "Every tier is additive: Higher tiers wrap around lower tiers rather than replacing them.")
    add_footer(s17, 17, total_slides=19)
    w_up = Inches(3.7)
    gap_up = Inches(0.316)
    upgrade_layers = [
        ("LAYER 1 // TIER 1 FOUNDATION", "Essential Automation Core", [
            "Temporal Workflow Engine",
            "Application Logic (Python / TS)",
            "PostgreSQL Database",
            "Dolibarr CRM API Client",
            "Shopify Store REST Client",
            "Meta / Instagram API Client",
            "Direct LLM API Wrapper",
            "Status: Remains untouched in Tier 2."
        ]),
        ("LAYER 2 // TIER 2 ADDITIONS", "Governed Intelligence Layer", [
            "Policy Engine Framework",
            "Decision Contract Validator",
            "OpenTelemetry Tracing Exporter",
            "Selective LangGraph Engine",
            "Post-Action Verification Engine",
            "Audit Trail Storage & Ledger",
            "Status: Wraps around Tier 1 without altering database models."
        ]),
        ("LAYER 3 // TIER 3 ADDITIONS", "The Autonomous Flywheel", [
            "Domain Specialist Agents",
            "Model Context Protocol (MCP) Tools",
            "Shared Revenue State & Event PubSub",
            "Cross-Domain Feedback Engine",
            "Continuous Experimentation Harness",
            "Status: Adds autonomous loops over Tier 2 governance."
        ])
    ]
    for i, (tag, title, bullets) in enumerate(upgrade_layers):
        add_formatted_card(s17, Inches(0.8) + i * (w_up + gap_up), Inches(2.0), w_up, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST), title_size=18, bullet_size=12)

    # Slide 18: Deep-Dive Tradeoffs
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "17 // Engineering Defense", "System Design Tradeoff Analysis: The 'Why'",
               "Every decision has a cost. A senior engineer is defined by the tradeoffs they can explicitly defend.")
    add_footer(s18, 18, total_slides=19)
    add_formatted_card(s18, Inches(0.8), Inches(2.0), Inches(5.68), Inches(2.3), "DECISION 01", "Temporal vs. n8n", [
        "Tradeoff: Temporal requires writing code; n8n has a visual UI.",
        "Defense: Revenue operations require true durability. An unhandled error in n8n drops state. Temporal's append-only event log guarantees zero lost invoices and deterministic replay."
    ], tag_color=COLOR_OLIVE, title_size=16, bullet_size=11)
    add_formatted_card(s18, Inches(6.85), Inches(2.0), Inches(5.68), Inches(2.3), "DECISION 02", "Direct APIs vs. MCP in Tiers 1–2", [
        "Tradeoff: Direct API clients are tightly coupled; MCP standardizes tool protocols.",
        "Defense: Direct APIs have zero protocol overhead, simpler debugging, and strict type safety. MCP adds value in Tier 3 dynamic discovery, but is unnecessary overhead in Tier 1."
    ], tag_color=COLOR_OCHRE, title_size=16, bullet_size=11)
    add_formatted_card(s18, Inches(0.8), Inches(4.5), Inches(5.68), Inches(2.3), "DECISION 03", "PostgreSQL vs. Event Streaming (Kafka)", [
        "Tradeoff: Postgres is relational; Kafka handles massive distributed streaming.",
        "Defense: Alandas' target is 100 accounts (~500 transactions/mo). PostgreSQL ACID transactions and JSONB state easily scale to 50,000 accounts without distributed Kafka complexity."
    ], tag_color=COLOR_FOREST, title_size=16, bullet_size=11)
    add_formatted_card(s18, Inches(6.85), Inches(4.5), Inches(5.68), Inches(2.3), "DECISION 04", "Selective LangGraph vs. Whole-App Graphs", [
        "Tradeoff: LangGraph gives cyclic graph control; Temporal gives durable execution.",
        "Defense: LangGraph is brilliant for bounded multi-turn reflection (e.g., evaluating an ad draft). Temporal acts as the parent orchestrator; LangGraph runs inside an Activity."
    ], tag_color=COLOR_OLIVE, title_size=16, bullet_size=11)

    # Slide 19: Strategic Roadmap
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "18 // Execution Roadmap", "The Alandas Roadmap: Starting Tier 1 Today",
               "Stabilize operations at Tier 1 immediately, scale to 50 accounts with Tier 2, and unlock 100 accounts full-time freedom with Tier 3.")
    add_footer(s19, 19, total_slides=19)
    roadmap = [
        ("MONTHS 1–3 // START TODAY", "Sprint 1: Tier 1 Launch", [
            "Target: 25 ➔ 40 Active Accounts (€5k/mo)",
            "Stabilize Dolibarr CRM with automated daily cloud backups.",
            "Restore Hermes AI WhatsApp order parsing with deterministic rules.",
            "Deploy OpenReply Instagram comment-to-DM loop on B2B page.",
            "Standardize €19 discovery kit featuring shatter-resistant teapot.",
            "Sidy handles 10–20 WhatsApp chats daily with AI drafting."
        ]),
        ("MONTHS 4–6 // SCALING UP", "Sprint 2: Tier 2 Governance", [
            "Target: 40 ➔ 70 Active Accounts (€12k/mo)",
            "Deploy Policy Engine & Decision Contracts for Meta ad spend.",
            "Automate Day-25 predictive refills via Dolibarr WhatsApp alerts.",
            "Add OpenTelemetry tracing & audit log for all AI decisions.",
            "Deploy barista table talkers and QR counter refill portals.",
            "Sidy reduces administrative hours to < 4 hours/week."
        ]),
        ("MONTHS 7–12 // FULL FREEDOM", "Sprint 3: Tier 3 Platform", [
            "Target: 100 Active Accounts (€20k–€30k/mo)",
            "Closed-loop revenue flywheel: LTV data drives Meta ad creative.",
            "MCP capability layer connects multi-city logistics and warehouse.",
            "Multi-agent coordination across Germany, Austria & Switzerland.",
            "Predictable recurring gross margin of €15,000–€30,000/month.",
            "Sidy quits Swiss job to be his own boss 100% full-time."
        ])
    ]
    for i, (tag, title, bullets) in enumerate(roadmap):
        add_formatted_card(s19, Inches(0.8) + i * (w_up + gap_up), Inches(2.0), w_up, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST), title_size=18, bullet_size=11.5)
"""

# Replace from old_pptx_section_start to before prs.save
split_point = text.find(old_pptx_section_start)
end_point = text.find("    prs.save(output_pptx_path)")

if split_point == -1 or end_point == -1:
    raise Exception(f"Could not find PPTX section markers: split={split_point}, end={end_point}")

text = text[:split_point] + new_pptx_slides + "\n" + text[end_point:]

with open("scripts/generate_tiered_presentation.py", "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] generate_tiered_presentation.py rebuilt successfully with 19 slides!")
