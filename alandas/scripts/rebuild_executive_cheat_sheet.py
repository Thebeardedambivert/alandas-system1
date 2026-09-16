"""
rebuild_executive_cheat_sheet.py
Creates an Executive-grade, visually stunning Cheat Sheet Deck for Sidy Sow.
Every slide is balanced with zero awkward whitespace voids.
Embeds high-resolution visual mockups of:
1. Alandas €19 Trial Teapot Starter Kit (editorial commercial photo)
2. WhatsApp 1-Tap Approval Screen (iPhone mockup)
3. Dolibarr CRM & Invoice Generator (desktop OCR mockup)
4. Tier 2 Decision Contract Gate Flowchart
5. Tier 3 Autonomous Commercial Flywheel Flowchart

Generates:
- Alandas_Sidy_Cheat_Sheet_Deck.pptx
- Alandas_Sidy_Cheat_Sheet_Deck.pdf (via PowerPoint COM ppSaveAsPDF)
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import win32com.client

def build_executive_deck(output_pptx, output_pdf):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")

    img_teapot = os.path.join(assets_dir, "alandas_trial_teapot_kit.jpg")
    img_whatsapp = os.path.join(assets_dir, "mockup_whatsapp_tier1.png")
    img_dolibarr = os.path.join(assets_dir, "mockup_dolibarr_crm.png")
    img_tier2 = os.path.join(assets_dir, "tier2_flowchart.png")
    img_tier3 = os.path.join(assets_dir, "tier3_flowchart.png")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    COLOR_BG = RGBColor(0xF9, 0xF7, 0xF2)
    COLOR_TEXT_MAIN = RGBColor(0x18, 0x19, 0x16)
    COLOR_TEXT_MUTED = RGBColor(0x54, 0x51, 0x48)
    COLOR_OLIVE = RGBColor(0x44, 0x4C, 0x32)
    COLOR_OLIVE_LIGHT = RGBColor(0xEE, 0xF2, 0xE8)
    COLOR_OLIVE_BORDER = RGBColor(0xD1, 0xD9, 0xC5)
    COLOR_OCHRE = RGBColor(0xC4, 0x87, 0x37)
    COLOR_OCHRE_LIGHT = RGBColor(0xFC, 0xF4, 0xE8)
    COLOR_OCHRE_BORDER = RGBColor(0xF0, 0xDF, 0xC2)
    COLOR_FOREST = RGBColor(0x2F, 0x53, 0x39)
    COLOR_FOREST_LIGHT = RGBColor(0xED, 0xF5, 0xEF)
    COLOR_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)
    COLOR_CARD_BORDER = RGBColor(0xE2, 0xDD, 0xD0)
    COLOR_CARD_ALT = RGBColor(0xF4, 0xEF, 0xE6)

    FONT_HEAD = "Georgia"
    FONT_BODY = "Calibri"

    def set_bg(slide):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG

    def add_header(slide, kicker, title, subtitle=None):
        set_bg(slide)
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = kicker.upper()
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(26)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(2)

        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.name = FONT_BODY
            p2.font.size = Pt(12.5)
            p2.font.color.rgb = COLOR_TEXT_MUTED

    def add_footer(slide, curr, total=11):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
        tf = tb.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET  |  SLIDE {curr:02d} OF {total:02d}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MUTED

    def create_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    def add_formatted_card(slide, left, top, width, height, tag, title, bullets, tag_color=COLOR_OLIVE, bg_color=COLOR_CARD_BG, title_size=17, bullet_size=12):
        create_card(slide, left, top, width, height, bg_color=bg_color)
        tb = slide.shapes.add_textbox(left + Inches(0.24), top + Inches(0.22), width - Inches(0.48), height - Inches(0.44))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = tag.upper()
        p0.font.name = FONT_BODY
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = tag_color
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(title_size)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(6)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(bullet_size)
            pb.font.color.rgb = COLOR_TEXT_MUTED
            pb.space_after = Pt(5)

    # =============================================================
    # Slide 1: Executive Title & Commercial Physical Product Showcase
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    
    # Left Hero Text Card
    create_card(s1, Inches(0.8), Inches(0.75), Inches(6.5), Inches(6.0))
    tb1 = s1.shapes.add_textbox(Inches(1.15), Inches(1.1), Inches(5.8), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p0 = tf1.paragraphs[0]
    p0.text = "ALANDAS TEA BERLIN // STRATEGIC ROADMAP"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(11.5)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_OLIVE
    p0.space_after = Pt(8)

    p1 = tf1.add_paragraph()
    p1.text = "The Path from 25 to 100 Cafes"
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "A plain-English strategic blueprint for Sidy Sow: How we automate sales grunt work, protect brand integrity, scale predictable wholesale reorders, and get you back to being your own boss full-time."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED

    # 3 Summary Highlight Badges in Left Card
    pills = [
        ("THE TARGET", "100 Partner Cafes", "€15k–€30k/mo predictable income so Sidy quits his Swiss job"),
        ("THE ENGINE", "24/7 Digital Copilot", "Scrapes cafe leads, drafts pitches, deciphers order note photos"),
        ("THE CONTROL", "3 Governed Tiers", "Sidy retains 100% authority via WhatsApp; zero brand risk")
    ]
    pill_w = Inches(1.8)
    for i, (ptag, ptitle, pdesc) in enumerate(pills):
        px = Inches(1.15) + i * (pill_w + Inches(0.2))
        create_card(s1, px, Inches(4.5), pill_w, Inches(1.9), bg_color=COLOR_CARD_ALT)
        tbp = s1.shapes.add_textbox(px + Inches(0.12), Inches(4.6), pill_w - Inches(0.24), Inches(1.7))
        tfe = tbp.text_frame
        tfe.word_wrap = True
        tfe.margin_left = tfe.margin_top = tfe.margin_right = tfe.margin_bottom = 0
        
        pp0 = tfe.paragraphs[0]
        pp0.text = ptag
        pp0.font.name = FONT_BODY
        pp0.font.size = Pt(9.5)
        pp0.font.bold = True
        pp0.font.color.rgb = COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST)
        pp0.space_after = Pt(2)

        pp1 = tfe.add_paragraph()
        pp1.text = ptitle
        pp1.font.name = FONT_HEAD
        pp1.font.size = Pt(12)
        pp1.font.bold = True
        pp1.font.color.rgb = COLOR_TEXT_MAIN
        pp1.space_after = Pt(3)

        pp2 = tfe.add_paragraph()
        pp2.text = pdesc
        pp2.font.name = FONT_BODY
        pp2.font.size = Pt(10)
        pp2.font.color.rgb = COLOR_TEXT_MUTED

    # Right Product Showcase Card
    create_card(s1, Inches(7.55), Inches(0.75), Inches(4.98), Inches(6.0))
    s1.shapes.add_picture(img_teapot, Inches(7.75), Inches(0.95), width=Inches(4.58))
    
    tbc = s1.shapes.add_textbox(Inches(7.75), Inches(4.55), Inches(4.58), Inches(1.9))
    tfc = tbc.text_frame
    tfc.word_wrap = True
    tfc.margin_left = tfc.margin_top = tfc.margin_right = tfc.margin_bottom = 0

    pc0 = tfc.paragraphs[0]
    pc0.text = "THE B2B CONVERSION WEAPON // €19 TRIAL KIT"
    pc0.font.name = FONT_BODY
    pc0.font.size = Pt(10.5)
    pc0.font.bold = True
    pc0.font.color.rgb = COLOR_OCHRE
    pc0.space_after = Pt(2)

    pc1 = tfc.add_paragraph()
    pc1.text = "Borosilicate Teapot + 4 Signature Blends"
    pc1.font.name = FONT_HEAD
    pc1.font.size = Pt(16)
    pc1.font.bold = True
    pc1.font.color.rgb = COLOR_TEXT_MAIN
    pc1.space_after = Pt(3)

    pc2 = tfc.add_paragraph()
    pc2.text = "The physical Trojan Horse that turns cold Berlin cafes into lifelong wholesale accounts. 100% of the €19 is credited back on their first commercial order."
    pc2.font.name = FONT_BODY
    pc2.font.size = Pt(11.5)
    pc2.font.color.rgb = COLOR_TEXT_MUTED

    # =============================================================
    # Slide 2: The Big Picture: Sidy's Reality vs The 100-Cafe Equation
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "01 // The Big Picture", "Why Are We Doing This? Sidy's Reality vs. The Goal",
               "Sidy imports exceptional organic tea, but current manual operations demand too much time for too little cashflow.")
    add_footer(s2, 2)

    add_formatted_card(s2, Inches(0.8), Inches(1.8), Inches(5.72), Inches(4.05),
                       "CURRENT REALITY // THE FOUNDER'S TRAP", "Why Sidy Is Stuck in a Day Job", [
                           "High Swiss Living Costs: Moved to Switzerland; tea business doesn't yet yield steady monthly cashflow to live on.",
                           "Exhausting Day Job: Working for a Norwegian firm: 'It's been a long walk... I'm tired. I want to become again my own boss.'",
                           "25 Happy Accounts Capped: Has ~25 great cafes buying regularly, but customer acquisition is stalled due to lack of time.",
                           "Manual Friction: Sidy spends evenings manually messaging cafes on Instagram and deciphering crumpled paper orders."
                       ], tag_color=COLOR_OCHRE, title_size=19, bullet_size=12.5)

    add_formatted_card(s2, Inches(6.81), Inches(1.8), Inches(5.72), Inches(4.05),
                       "THE TARGET // THE 100-CAFE EQUATION", "What 100 Accounts Actually Unlocks", [
                           "100 Cafes @ €200–€350 / Month: Generates €15,000 to €30,000 every month in predictable wholesale revenue.",
                           "90%+ Gross Margin: Premium tea carries extraordinary margins when shipped directly in wholesale volume.",
                           "Full-Time Freedom: Sidy hands in his notice in Switzerland and returns to Berlin as his own full-time boss.",
                           "Zero Additional Headcount: Operates the entire 100-cafe network without hiring expensive administrative staff."
                       ], tag_color=COLOR_OLIVE, title_size=19, bullet_size=12.5)

    # Bottom Full-Width Anchor Banner
    create_card(s2, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.85), bg_color=COLOR_OLIVE_LIGHT, border_color=COLOR_OLIVE_BORDER)
    tbb = s2.shapes.add_textbox(Inches(1.1), Inches(6.15), Inches(11.133), Inches(0.65))
    tfb = tbb.text_frame
    tfb.word_wrap = True
    pbb = tfb.paragraphs[0]
    pbb.text = "THE CORE METRIC: Every system and architecture tier Cyril designs serves ONE metric — Getting Sidy back to Berlin as his own full-time boss."
    pbb.font.name = FONT_BODY
    pbb.font.size = Pt(13)
    pbb.font.bold = True
    pbb.font.color.rgb = COLOR_OLIVE

    # =============================================================
    # Slide 3: The 5 Bottlenecks Holding Alandas Back Today
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "02 // Operational Diagnosis", "The 5 Bottlenecks Holding Alandas Back Today",
               "The exact friction points stopping Alandas from scaling from 25 to 100 cafes.")
    add_footer(s3, 3)

    bottlenecks = [
        ("BOTTLENECK 01", "Manual Scraping Sucks Time", ["Searching Google Maps & digging for cafe owners burns 20+ hours every week without leverage."]),
        ("BOTTLENECK 02", "Cafes Ignore Cold Emails", ["Baristas and cafe owners are busy on the floor. They run their entire business on WhatsApp."]),
        ("BOTTLENECK 03", "Order Processing Is Messy", ["Crumpled paper order photos texted late at night cause invoice errors and delayed delivery."]),
        ("BOTTLENECK 04", "Silent Cafe Churn", ["Cafes run out on Day 28. If Sidy doesn't text on Day 25, they panic-buy supermarket tea bags."]),
        ("BOTTLENECK 05", "Burned by Hermes AI", ["Previous low-code bot crashed and wiped memory. Sidy rightly refuses fragile toys."]),
        ("THE OPPORTUNITY", "The Durable Solution", ["Replace manual hustle with a crash-resilient revenue machine backed by solid code and clear rules."])
    ]
    w_b = Inches(3.72)
    h_b = Inches(2.35)
    gap_x = Inches(0.28)
    gap_y = Inches(0.25)
    for i, (tag, title, bullets) in enumerate(bottlenecks):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * (w_b + gap_x)
        y = Inches(1.8) + row * (h_b + gap_y)
        add_formatted_card(s3, x, y, w_b, h_b, tag, title, bullets,
                           tag_color=COLOR_OLIVE if i==5 else COLOR_OCHRE,
                           title_size=16, bullet_size=11.5)

    # =============================================================
    # Slide 4: What We Are Building — The 24/7 Digital Sales Assistant
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "03 // The Solution", "What We Are Building: Your 24/7 Digital Revenue Machine",
               "A tireless digital sales and operations assistant that handles the tedious grunt work while Sidy retains total authority.")
    add_footer(s4, 4)

    # Left Column: The 6 Stages
    create_card(s4, Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.0))
    tbs4 = s4.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(6.3), Inches(4.7))
    tfs4 = tbs4.text_frame
    tfs4.word_wrap = True
    tfs4.margin_left = tfs4.margin_top = tfs4.margin_right = tfs4.margin_bottom = 0

    p_hdr = tfs4.paragraphs[0]
    p_hdr.text = "THE 6-STAGE REVENUE PIPELINE"
    p_hdr.font.name = FONT_BODY
    p_hdr.font.size = Pt(11.5)
    p_hdr.font.bold = True
    p_hdr.font.color.rgb = COLOR_OLIVE
    p_hdr.space_after = Pt(8)

    stages_text = [
        ("01 // DISCOVER", "Scans Google Maps & IG for >30-seat specialty brunch cafes in Berlin & Munich."),
        ("02 // ENRICH", "Extracts verified owner WhatsApp numbers via German § 5 TMG Impressum for €0.00."),
        ("03 // OFFER", "Pitches the €19 Teapot Starter Kit (100% credited back on wholesale crate)."),
        ("04 // 1-TAP APPROVAL", "AI drafts warm message; Sidy reviews on his phone & taps 'Approve'."),
        ("05 // INVOICE OCR", "AI deciphers handwritten barista notes into draft Dolibarr CRM invoices."),
        ("06 // DAY-25 REFILL", "Automated WhatsApp refill alert before cafes run dry, ending silent churn.")
    ]
    for tag_s, desc_s in stages_text:
        ps = tfs4.add_paragraph()
        ps.text = f"{tag_s}: {desc_s}"
        ps.font.name = FONT_BODY
        ps.font.size = Pt(12)
        ps.font.color.rgb = COLOR_TEXT_MAIN
        ps.space_after = Pt(8)

    # Right Column: iPhone WhatsApp UI Mockup
    create_card(s4, Inches(7.85), Inches(1.8), Inches(4.68), Inches(5.0))
    s4.shapes.add_picture(img_whatsapp, Inches(8.5), Inches(1.9), width=Inches(3.38))
    
    tbw = s4.shapes.add_textbox(Inches(7.95), Inches(1.9), Inches(4.48), Inches(0.3))
    tfw = tbw.text_frame
    tfw.margin_left = tfw.margin_top = tfw.margin_right = tfw.margin_bottom = 0
    pw = tfw.paragraphs[0]
    pw.text = "WHAT SIDY SEES ON HIS IPHONE // 1-TAP APPROVAL"
    pw.font.name = FONT_BODY
    pw.font.size = Pt(9.5)
    pw.font.bold = True
    pw.font.color.rgb = COLOR_OCHRE

    # =============================================================
    # Slide 5: Why 3 Tiers? 'Don't Build a Spaceship on Day 1'
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "04 // Architectural Law", "Why 3 Tiers? 'Don't Build a Spaceship on Day 1'",
               "We do not give AI full control on Day 1. Each tier earns complexity based on proven business scale.")
    add_footer(s5, 5)

    tiers_ladder = [
        ("TIER 3 // AUTONOMOUS PLATFORM (100+ CAFES)", "The Self-Running Business Machine",
         ["Closed-loop commercial machine across Germany, Austria & Switzerland.",
          "Cafe reorder velocity automatically triggers and refines Meta Ad experiments.",
          "Sidy acts as Chairman reviewing weekly revenue digests while enjoying tea."]),
        ("TIER 2 // GOVERNED INTELLIGENCE (40–70 CAFES)", "The Smart Assistant with Guardrails",
         ["AI recommends smart moves (e.g. +30% ad budget), but strict Policy Engines enforce rules.",
          "Any budget delta > €5 requires Sidy's 1-tap WhatsApp sign-off.",
          "Mathematically impossible for an AI bug to drain bank accounts or leak pricing."]),
        ("TIER 1 // ESSENTIAL AUTOMATION (25–40 CAFES) — START HERE", "The Tireless Grunt Worker (Sidy is Pilot)",
         ["Machine scrapes cafes, gets WhatsApps, drafts pitches, and parses order notes.",
          "Sidy retains 100% approval authority on every outbound message and invoice.",
          "100% brand safe. Saves 15+ hours/week. Starts today with ZERO fragility."])
    ]
    h_ladder = Inches(1.55)
    gap_ladder = Inches(0.18)
    for i, (tag, title, bullets) in enumerate(tiers_ladder):
        y = Inches(1.8) + i * (h_ladder + gap_ladder)
        add_formatted_card(s5, Inches(0.8), y, Inches(11.733), h_ladder, tag, title, bullets,
                           tag_color=COLOR_FOREST if i==0 else (COLOR_OCHRE if i==1 else COLOR_OLIVE),
                           title_size=16, bullet_size=11.5)

    # =============================================================
    # Slide 6: Tier 1 Deep Dive — Sidy Is Pilot & Dolibarr Mockup
    # =============================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "05 // Tier 1 in Plain English", "Tier 1: 'The Tireless Assistant' (Sidy is Pilot)",
               "The machine gathers facts and proposes actions; Sidy taps Approve before anything is dispatched.")
    add_footer(s6, 6)

    # Left Column: 5-Stage Human-in-the-Loop Workflow
    add_formatted_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
                       "THE 5-STAGE WORKFLOW // 100% HUMAN-IN-THE-LOOP", "Read ➔ Analyze ➔ Propose ➔ Approve ➔ Execute", [
                           "1. Read: Scans Google Maps & Instagram for specialty brunch cafes with >30 seats.",
                           "2. Analyze: Evaluates menu pricing, specialty coffee aesthetic, and owner details.",
                           "3. Propose: Drafts personalized WhatsApp message pitching the €19 teapot kit.",
                           "4. Sidy Approves: Message appears on Sidy's phone. Sidy taps Approve or edits.",
                           "5. Execute: Temporal sends WhatsApp, creates Dolibarr card, schedules follow-up.",
                           "Zero Brand Risk: Sidy protects botanical integrity & tone; AI never sends alone.",
                           "Saves 15+ Hours/Week: No more late-night manual typing or deciphering notes.",
                           "Target: 25 ➔ 40 Cafes | ~€5,000/month steady wholesale revenue."
                       ], tag_color=COLOR_OLIVE, title_size=17, bullet_size=11.5)

    # Right Column: Dolibarr Desktop CRM Mockup
    create_card(s6, Inches(6.65), Inches(1.8), Inches(5.88), Inches(5.0))
    s6.shapes.add_picture(img_dolibarr, Inches(6.8), Inches(2.1), width=Inches(5.58))
    
    tbd = s6.shapes.add_textbox(Inches(6.8), Inches(1.85), Inches(5.58), Inches(0.3))
    tfd = tbd.text_frame
    tfd.margin_left = tfd.margin_top = tfd.margin_right = tfd.margin_bottom = 0
    pd = tfd.paragraphs[0]
    pd.text = "WHAT DOLIBARR LOOKS LIKE // HANDWRITTEN NOTE ➔ AUTO INVOICE"
    pd.font.name = FONT_BODY
    pd.font.size = Pt(9.5)
    pd.font.bold = True
    pd.font.color.rgb = COLOR_OLIVE

    # =============================================================
    # Slide 7: Tier 2 Deep Dive — Guardrails & Policy Engine Flowchart
    # =============================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "06 // Tier 2 in Plain English", "Tier 2: 'The Smart Assistant with Guardrails'",
               "AI suggests business optimizations, but unbreakable Policy Engines prevent errors or runaway spend.")
    add_footer(s7, 7)

    # Left Column: Policy Rules & Real-World Example
    add_formatted_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
                       "REAL-WORLD EXAMPLE", "Increasing Meta Ad Budget by +30%", [
                           "1. AI Observes: Berlin brunch ad has 4.2x ROAS. Suggests raising €30 ➔ €39/day.",
                           "2. Hard Ceiling Check: Is €39 under our maximum €50/day policy cap? (YES).",
                           "3. Threshold Check: Does delta (>€5) require human sign-off? (YES).",
                           "4. Sidy Signs Off: WhatsApp ping dings: [Approve +€9/day for Berlin Brunch Ad?].",
                           "5. Verify State: AI calls Meta API, then re-queries Meta to confirm €39.00 (NOT €390).",
                           "Zero Runaway Spend: Mathematically impossible for AI glitch to drain accounts.",
                           "Zero Pricing Leaks: Wholesale volume discounts follow strict tables, not whims.",
                           "Target: 40 ➔ 70 Cafes | ~€12,000/month recurring wholesale revenue."
                       ], tag_color=COLOR_OCHRE, title_size=17, bullet_size=11.5)

    # Right Column: Tier 2 Flowchart Diagram
    create_card(s7, Inches(6.65), Inches(1.8), Inches(5.88), Inches(5.0))
    s7.shapes.add_picture(img_tier2, Inches(7.45), Inches(1.9), height=Inches(4.8))
    
    tb7 = s7.shapes.add_textbox(Inches(6.8), Inches(1.85), Inches(5.58), Inches(0.3))
    tf7 = tb7.text_frame
    tf7.margin_left = tf7.margin_top = tf7.margin_right = tf7.margin_bottom = 0
    p7 = tf7.paragraphs[0]
    p7.text = "THE GOVERNED DECISION CONTRACT GATE // STRICT BOUNDARIES"
    p7.font.name = FONT_BODY
    p7.font.size = Pt(9.5)
    p7.font.bold = True
    p7.font.color.rgb = COLOR_OCHRE

    # =============================================================
    # Slide 8: Tier 3 Deep Dive — Autonomous Flywheel Flowchart
    # =============================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "07 // Tier 3 in Plain English", "Tier 3: 'The Self-Running Business Machine'",
               "Alandas runs like a multi-million-euro beverage brand with zero extra office staff.")
    add_footer(s8, 8)

    # Left Column: Munich Terrace Flywheel
    add_formatted_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
                       "THE CLOSED-LOOP FLYWHEEL", "Munich Terrace Summer Scenario", [
                           "1. Reorder Surge: In July, Munich cafes reorder Earl Grey 2x faster for iced tea.",
                           "2. Operations Alerts Marketing: System detects Munich terrace surge in real time.",
                           "3. Automated Ad Copy: Marketing Agent writes: 'Serving iced tea on your terrace? Try our €19 kit.'",
                           "4. Closed-Loop Optimization: Launches tests and scales ad spend without manual human effort.",
                           "Zero Linear Headcount: Operates across Germany, Austria & Switzerland.",
                           "Automated Circuit Breakers: Any anomaly halts the system instantly.",
                           "Sidy Acts as Chairman: Reviews weekly digests while enjoying tea.",
                           "Target: 100+ Cafes | €20k–€30k/month. Sidy is 100% his own boss."
                       ], tag_color=COLOR_FOREST, title_size=17, bullet_size=11.5)

    # Right Column: Tier 3 Flywheel Diagram
    create_card(s8, Inches(6.65), Inches(1.8), Inches(5.88), Inches(5.0))
    s8.shapes.add_picture(img_tier3, Inches(6.75), Inches(1.9), width=Inches(5.68))

    tb8 = s8.shapes.add_textbox(Inches(6.8), Inches(1.85), Inches(5.58), Inches(0.3))
    tf8 = tb8.text_frame
    tf8.margin_left = tf8.margin_top = tf8.margin_right = tf8.margin_bottom = 0
    p8 = tf8.paragraphs[0]
    p8.text = "THE AUTONOMOUS CLOSED-LOOP COMMERCIAL FLYWHEEL"
    p8.font.name = FONT_BODY
    p8.font.size = Pt(9.5)
    p8.font.bold = True
    p8.font.color.rgb = COLOR_FOREST

    # =============================================================
    # Slide 9: The 3 Technical Secret Weapons Made Simple
    # =============================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "08 // Technical Defense Made Simple", "The 3 Technical 'Secret Weapons' (In Plain English)",
               "Three simple metaphors to explain the architecture to Sidy or investors without confusing jargon.")
    add_footer(s9, 9)

    weapons = [
        ("SECRET WEAPON 01", "Temporal vs. n8n", "Carving in Stone vs. Sticky Notes", [
            "n8n writes orders on sticky notes. When the server crashes, notes blow away and data is lost.",
            "Temporal carves every step into solid rock. If the server reboots, it resumes at the exact line of code.",
            "Zero lost invoices, zero lost cafe leads. 100% durable code."
        ]),
        ("SECRET WEAPON 02", "Impressum Waterfall", "Cheapest Tool First (87% Savings)", [
            "Normal agencies waste €80 looking up 1,000 leads.",
            "Under German § 5 TMG law, every site publishes owner details. Our free scraper gets 48% of leads for €0.00.",
            "We only call paid tools for the missed few. Total cost: €10 instead of €80."
        ]),
        ("SECRET WEAPON 03", "Policy Engine Bouncer", "The Guardrail at the Bank Vault", [
            "No AI is ever handed Sidy's credit card or pricing authority.",
            "AI writes a typed proposal. The Policy Engine checks: Is discount allowed? Is budget safe?",
            "If unusual, it rings Sidy's phone for 1-tap confirmation."
        ])
    ]
    w_w = Inches(3.72)
    for i, (tag, title, sub, bullets) in enumerate(weapons):
        x = Inches(0.8) + i * (w_w + Inches(0.28))
        create_card(s9, x, Inches(1.8), w_w, Inches(4.05))
        tb = s9.shapes.add_textbox(x + Inches(0.24), Inches(1.95), w_w - Inches(0.48), Inches(3.75))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = tag
        p0.font.name = FONT_BODY
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST)
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(2)

        p1_sub = tf.add_paragraph()
        p1_sub.text = sub
        p1_sub.font.name = FONT_BODY
        p1_sub.font.size = Pt(11.5)
        p1_sub.font.bold = True
        p1_sub.font.color.rgb = COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST)
        p1_sub.space_after = Pt(8)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(12)
            pb.font.color.rgb = COLOR_TEXT_MUTED
            pb.space_after = Pt(5)

    # Bottom Banner for Slide 9
    create_card(s9, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.85), bg_color=COLOR_OCHRE_LIGHT, border_color=COLOR_OCHRE_BORDER)
    tb9 = s9.shapes.add_textbox(Inches(1.1), Inches(6.15), Inches(11.133), Inches(0.65))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    p9 = tf9.paragraphs[0]
    p9.text = "CORE ARCHITECTURAL DEFENSE: Zero low-code toys. Zero lost data via Temporal state durability. Zero runaway spend via deterministic Policy Engines."
    p9.font.name = FONT_BODY
    p9.font.size = Pt(12)
    p9.font.bold = True
    p9.font.color.rgb = COLOR_OCHRE

    # =============================================================
    # Slide 10: Choose Your Tier: Modular Revenue Architecture
    # =============================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "09 // Architecture Comparison & Selection", "Choose Your Tier: Modular Revenue Architecture",
               "Sidy chooses which tier fits his current stage and comfort. Every tier is modular—you never discard code.")
    add_footer(s10, 10)

    phases = [
        ("OPTION 01 // RECOMMENDED START", "Tier 1: Essential", [
            "The Tireless Assistant (Sidy is Pilot)",
            "What It Solves: Stops 20+ hours of manual Google Maps scraping & messaging.",
            "Core Engine: Legal Impressum § 5 TMG scraper, AI drafts, Dolibarr invoice OCR.",
            "Human Control: Sidy approves every outbound message on WhatsApp.",
            "Sidy's Routine: Spends just 30 mins/day on WhatsApp reviews.",
            "Target Scale: 25 ➔ 40 Cafes | ~€5,000 / month recurring cashflow."
        ]),
        ("OPTION 02 // GROWTH & PROTECTION", "Tier 2: Governed", [
            "Smart Assistant with Guardrails",
            "What It Solves: Eliminates silent cafe churn and prevents runaway ad spend.",
            "Core Engine: Policy Engine (+30% ad rules, hard caps), Day-25 refill alerts.",
            "Human Control: Any budget change >€5 requires Sidy's 1-tap WhatsApp sign-off.",
            "Sidy's Routine: Admin drops to < 4 hrs/week. Sidy prepares notice at Swiss firm.",
            "Target Scale: 40 ➔ 70 Cafes | ~€12,000 / month recurring cashflow."
        ]),
        ("OPTION 03 // ENTERPRISE SCALE", "Tier 3: Autonomous", [
            "Self-Running Multi-City Flywheel",
            "What It Solves: Scales across Germany, Austria & Switzerland without hiring reps.",
            "Core Engine: Closed-loop reorder-to-ad flywheel, multi-city warehouse sync.",
            "Human Control: Automatic circuit breakers halt anomalies; Sidy acts as Chairman.",
            "Sidy's Routine: 100% full-time independent founder & CEO (< 2 hrs/week oversight).",
            "Target Scale: 100+ Cafes | €20,000–€30,000 / month recurring."
        ])
    ]
    for i, (tag, title, bullets) in enumerate(phases):
        x = Inches(0.8) + i * (w_w + Inches(0.28))
        add_formatted_card(s10, x, Inches(1.8), w_w, Inches(4.05), tag, title, bullets,
                           tag_color=COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST),
                           title_size=17, bullet_size=11.5)

    # Bottom Banner for Slide 10
    create_card(s10, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.85), bg_color=COLOR_FOREST_LIGHT, border_color=COLOR_OLIVE_BORDER)
    tb10 = s10.shapes.add_textbox(Inches(1.1), Inches(6.15), Inches(11.133), Inches(0.65))
    tf10 = tb10.text_frame
    tf10.word_wrap = True
    p10 = tf10.paragraphs[0]
    p10.text = "THE FREEDOM PRINCIPLE: Sidy chooses where to begin. No fixed timeline. Tier 1 gives immediate relief on Day 1; higher tiers unlock whenever Sidy wants to scale."
    p10.font.name = FONT_BODY
    p10.font.size = Pt(12)
    p10.font.bold = True
    p10.font.color.rgb = COLOR_FOREST

    # =============================================================
    # Slide 11: Starting Sprint 1 Today & Tangible Product Deliverable
    # =============================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10 // Immediate Next Steps", "Starting Sprint 1 Today: The First 4 Concrete Steps",
               "We do not need months of planning. We kick off Tier 1 immediately with 4 clear deliverables.")
    add_footer(s11, 11)

    # Left Column: 4 Step Cards in 2x2 Grid
    steps_s11 = [
        ("STEP 01", "Stabilize Dolibarr CRM", ["Automate daily cloud backups", "Clean existing 25 cafe accounts", "Ensure order history is never lost"]),
        ("STEP 02", "Standardize €19 Trial Kit", ["Assemble borosilicate teapot kit", "Pack 4 signature tea blends", "Include 100% wholesale credit voucher"]),
        ("STEP 03", "Run § 5 TMG Scraper", ["Extract 200 brunch cafes in Berlin & Munich", "Resolve owner names & emails for €0.00", "Zero wasted lead spend"]),
        ("STEP 04", "1-Tap WhatsApp Pilot", ["Generate first 10 personalized drafts", "Send to Sidy's WhatsApp for review", "Sidy taps Approve with one click"])
    ]
    w_grid = Inches(3.05)
    h_grid = Inches(2.35)
    for i, (tag, title, bullets) in enumerate(steps_s11):
        col = i % 2
        row = i // 2
        x = Inches(0.8) + col * (w_grid + Inches(0.2))
        y = Inches(1.8) + row * (h_grid + Inches(0.25))
        add_formatted_card(s11, x, y, w_grid, h_grid, tag, title, bullets, tag_color=COLOR_OLIVE, title_size=15, bullet_size=11)

    # Right Column: Product Box Showcase
    create_card(s11, Inches(7.45), Inches(1.8), Inches(5.08), Inches(5.0))
    s11.shapes.add_picture(img_teapot, Inches(7.65), Inches(1.95), width=Inches(4.68))
    
    tbd11 = s11.shapes.add_textbox(Inches(7.65), Inches(5.55), Inches(4.68), Inches(1.15))
    tfd11 = tbd11.text_frame
    tfd11.word_wrap = True
    tfd11.margin_left = tfd11.margin_top = tfd11.margin_right = tfd11.margin_bottom = 0
    pd11_0 = tfd11.paragraphs[0]
    pd11_0.text = "SPRINT 1 TANGIBLE DELIVERABLE"
    pd11_0.font.name = FONT_BODY
    pd11_0.font.size = Pt(10)
    pd11_0.font.bold = True
    pd11_0.font.color.rgb = COLOR_OCHRE
    pd11_0.space_after = Pt(2)

    pd11_1 = tfd11.add_paragraph()
    pd11_1.text = "The €19 Trial Teapot Starter Kit is ready to dispatch to the first 10 Berlin cafes this week. Real, tangible progress on Day 1."
    pd11_1.font.name = FONT_BODY
    pd11_1.font.size = Pt(11.5)
    pd11_1.font.color.rgb = COLOR_TEXT_MAIN

    # Save PPTX
    prs.save(output_pptx)
    print(f"[SUCCESS] Executive PPTX created: {output_pptx}")

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pptx_path = os.path.join(base, "Alandas_Sidy_Cheat_Sheet_Deck.pptx")
    pdf_path = os.path.join(base, "Alandas_Sidy_Cheat_Sheet_Deck_from_pptx.pdf")
    build_executive_deck(pptx_path, pdf_path)
