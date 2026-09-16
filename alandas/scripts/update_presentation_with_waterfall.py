import re

def update_presentation():
    script_path = "scripts/generate_tiered_presentation.py"
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update HTML slides:
    # First, for slides 8 through 18, renumber them to 9 through 19:
    for n in range(18, 7, -1):
        # Update data-slide
        content = content.replace(f'data-slide="{n}"', f'data-slide="{n+1}"')
        # Update footer: e.g. SLIDE 08 / 18 -> SLIDE 09 / 19
        old_footer = f"SLIDE {n:02d} / 18"
        new_footer = f"SLIDE {n+1:02d} / 19"
        content = content.replace(old_footer, new_footer)
        old_comment = f"<!-- SLIDE {n}:"
        new_comment = f"<!-- SLIDE {n+1}:"
        content = content.replace(old_comment, new_comment)

    # For slides 1 to 7, update their footers to / 19:
    for n in range(1, 8):
        content = content.replace(f"SLIDE {n:02d} / 18", f"SLIDE {n:02d} / 19")

    # Update slide counter and total in HTML:
    content = content.replace('1 / 18</span>', '1 / 19</span>')

    # HTML code for Slide 8:
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

    # Insert HTML slide 8 right before <!-- =================================================================== -->\n    <!-- SLIDE 9: Tier 2 Architecture -->
    target_anchor = "    <!-- =================================================================== -->\n    <!-- SLIDE 9: Tier 2 Architecture -->"
    if target_anchor not in content:
        raise Exception("Target anchor for HTML slide insertion not found!")
    content = content.replace(target_anchor, html_slide_8 + "\n" + target_anchor)

    # 2. Update PPTX slides:
    # Update default total_slides in add_footer:
    content = content.replace("total_slides=18", "total_slides=19")

    # In PPTX section:
    # Rename s18 -> s19, s17 -> s18, ... down to s8 -> s9:
    # Let's inspect how the PPTX code is written:
    # It has:
    # # Slide 8: Tier 2 Architecture
    # s8 = prs.slides.add_slide(blank_layout)
    # add_header(s8, "07 // Tier 2 Architecture", ...
    # add_footer(s8, 8)
    
    # Let's replace each slide block from s18 down to s8:
    for n in range(18, 7, -1):
        old_pattern_header = f'# Slide {n}:'
        new_pattern_header = f'# Slide {n+1}:'
        content = content.replace(old_pattern_header, new_pattern_header)

        # variable s{n} -> s{n+1}
        # Be careful not to replace things like s1 in s10.
        # We can do exact word replacements or specific regexes.

    # Let's write the PPTX code for slide 8 cleanly:
    pptx_slide_8_code = """
    # Slide 8: Waterfall Enrichment Engine
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
"""

    # In PPTX, update the add_footer calls for slides 1 to 7:
    for n in range(1, 8):
        content = content.replace(f"add_footer(s{n}, {n})", f"add_footer(s{n}, {n}, total_slides=19)")

    # In PPTX, for slides 8 to 18, we can rewrite the PPTX generation section cleanly:
    # Let's check lines 1957 to end of file in generate_tiered_presentation.py.
    with open("scripts/generate_tiered_presentation.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Base content updated!")

if __name__ == "__main__":
    update_presentation()
