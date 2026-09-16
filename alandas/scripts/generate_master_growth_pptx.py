"""
Generate Executive PowerPoint Presentation: Alandas Master Growth & Customer System
28-Slide Comprehensive Strategic Blueprint for Sidy Sow / Alandas Tea Berlin
Matches the Master Growth & Customer System with luxury editorial styling, executive-grade typography,
and exact strategic synchronizations from the Sidy Sow discovery session.
"""

import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# DESIGN SYSTEM & PALETTE (Warm Linen, Botanical Olive, Rich Ochre, Charcoal)
# -----------------------------------------------------------------------------
COLOR_BG = RGBColor(0xF8, 0xF6, 0xF0)          # Warm Linen #F8F6F0
COLOR_TEXT_MAIN = RGBColor(0x18, 0x19, 0x16)   # Deep Charcoal #181916
COLOR_TEXT_MUTED = RGBColor(0x5C, 0x59, 0x50)  # Muted Earth #5C5950
COLOR_OLIVE = RGBColor(0x44, 0x4C, 0x32)       # Botanical Olive #444C32
COLOR_OCHRE = RGBColor(0xC4, 0x87, 0x37)       # Rich Ochre #C48737
COLOR_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)     # Pure White
COLOR_CARD_BORDER = RGBColor(0xE4, 0xDF, 0xD3) # Subtle Sandstone Border
COLOR_LIGHT_BG = RGBColor(0xF3, 0xEF, 0xE6)    # Accent Linen Fill
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_GREEN = RGBColor(0x2F, 0x53, 0x39)       # Sage / Forest Green

FONT_HEAD = "Georgia"
FONT_BODY = "Calibri"

def set_slide_bg(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

def add_header(slide, kicker_text, title_text, lead_text=None):
    set_slide_bg(slide)
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = kicker_text.upper()
    p0.font.name = FONT_BODY
    p0.font.size = Pt(11.5)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_OLIVE
    p0.space_after = Pt(4)
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p1.space_after = Pt(4)
    
    if lead_text:
        p2 = tf.add_paragraph()
        p2.text = lead_text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(13.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

def add_footer(slide, current_slide, total_slides=28):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"ALANDAS TEA BERLIN  •  MASTER COMMERCIAL OPERATING SYSTEM  |  SLIDE {current_slide:02d} OF {total_slides:02d}"
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
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_formatted_card(slide, left, top, width, height, tag, title, body_bullets, tag_color=COLOR_OLIVE, bg_color=COLOR_CARD_BG, title_size=16, bullet_size=12):
    create_card(slide, left, top, width, height, bg_color=bg_color)
    tb = slide.shapes.add_textbox(left + Inches(0.24), top + Inches(0.22), width - Inches(0.48), height - Inches(0.44))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = tag.upper()
    p0.font.name = FONT_BODY
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = tag_color
    p0.space_after = Pt(4)
    
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(title_size)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p1.space_after = Pt(8)
    
    for bullet in body_bullets:
        pb = tf.add_paragraph()
        pb.text = f"•  {bullet}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(bullet_size)
        pb.font.color.rgb = COLOR_TEXT_MUTED
        pb.space_after = Pt(5)

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # SLIDE 1
    print("Building Slide 1: Title...")
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)
    create_card(s1, Inches(0.8), Inches(0.75), Inches(11.733), Inches(6.0), bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    
    tb = s1.shapes.add_textbox(Inches(1.4), Inches(1.15), Inches(10.5), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "ALANDAS TEA // NATIONWIDE COMMERCIAL ARCHITECTURE"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_OLIVE
    p.space_after = Pt(12)
    
    p = tf.add_paragraph()
    p.text = "Master Commercial Growth &\nCustomer Operating System"
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_MAIN
    p.space_after = Pt(12)
    
    p = tf.add_paragraph()
    p.text = "Turning Alandas' verified hospitality proposition into a predictable nationwide B2B acquisition, qualification, and recurring-order revenue machine across Germany — Scaling from 25 to 100 Active Accounts."
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_TEXT_MUTED

    stages = [
        ("01", "VALIDATE", "Process, unit economics, Dolibarr CRM & founder workload audit"),
        ("02", "FOUNDATION", "Storefront triage, partner proof & €19 trial box sync"),
        ("03", "ACQUIRE", "Dual Instagram comment-to-DM & German venue blitz"),
        ("04", "CONVERT", "Intake qualification filter & Turnkey Starter Crate"),
        ("05", "SCALE", "Day-25 predictive refills & Dolibarr-Hermes order flow")
    ]
    card_w = Inches(2.14)
    gap = Inches(0.18)
    start_x = Inches(1.4)
    y = Inches(4.5)
    for idx, (num, label, desc) in enumerate(stages):
        x = start_x + idx * (card_w + gap)
        create_card(s1, x, y, card_w, Inches(1.8), bg_color=COLOR_LIGHT_BG, border_color=COLOR_CARD_BORDER)
        tb_c = s1.shapes.add_textbox(x + Inches(0.18), y + Inches(0.16), card_w - Inches(0.36), Inches(1.5))
        tfc = tb_c.text_frame
        tfc.word_wrap = True
        p0 = tfc.paragraphs[0]
        p0.text = f"Sprint {idx+1}"
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE
        p1 = tfc.add_paragraph()
        p1.text = f"{num} {label.title()}"
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(4)
        p2 = tfc.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # SLIDE 2
    print("Building Slide 2: What I See...")
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "01 // Executive Observation", "What I See in Alandas Tea Berlin", 
               "The product and proposition are already proven in the market. The opportunity is connecting them with an automated commercial system.")
    add_footer(s2, 2)
    
    cards_s2 = [
        ("ASSET 01", "Distinctive Luxury Brand", [
            "Whole-leaf organic positioning",
            "Editorial visual aesthetic",
            "Stands out clearly against commodity dust tea",
            "Strong culinary reputation across Berlin"
        ]),
        ("ASSET 02", "Proven B2B Proposition", [
            "Turnkey Teebar display concept",
            "Ultra-thick shatter-resistant teapot eliminates cafe breakage fear",
            "High-margin beverage category (96% cafe gross margin)",
            "Direct founder-tested presentation"
        ]),
        ("ASSET 03", "25 Live Partner Venues", [
            "Verified accounts across Germany (Berlin, Hamburg, Munich, Frankfurt, NRW)",
            "Includes Vesuvio, Melt, Café Friedrichs",
            "Solid proof of recurring wholesale demand",
            "Foundation to scale to 100 active accounts"
        ]),
        ("ASSET 04", "Omnichannel Infrastructure", [
            "Shopify storefront + custom domain",
            "Dual Instagram channels: @alandastea B2C + B2B wholesale",
            "Direct WhatsApp customer dialogue with cafe owners",
            "Dolibarr CRM for clients, inventory & PDF invoicing"
        ])
    ]
    w = Inches(2.72)
    gap = Inches(0.28)
    x0 = Inches(0.8)
    y0 = Inches(2.0)
    h0 = Inches(4.8)
    for i, (tag, title, bullets) in enumerate(cards_s2):
        add_formatted_card(s2, x0 + i * (w + gap), y0, w, h0, tag, title, bullets, title_size=16, bullet_size=12)

    # SLIDE 3
    print("Building Slide 3: The B2B Opportunity...")
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "02 // Wholesale Potential", "The B2B Opportunity: Why Wholesale Leads",
               "The catalog and customer base make a compelling case for treating B2B wholesale as the primary engine to reach 100 accounts across Germany.")
    add_footer(s3, 3)

    metrics = [
        ("25 → 100", "Growth Trajectory", "Phase 1: 25 active venues (€3k–€5k/mo) → Master Goal: 100 accounts (€15k–€30k/mo)"),
        ("18+", "Artisan Tea SKUs", "Covering black, green, herbal, fruit & wellness blends"),
        ("50%", "Organic Share", "Certified organic ingredients across blends"),
        ("€0.195", "Leaf Cost per Pot", "Enables 96% gross margin for cafes charging €5/pot")
    ]
    w_m = Inches(2.72)
    gap_m = Inches(0.28)
    for i, (num, title, desc) in enumerate(metrics):
        create_card(s3, x0 + i*(w_m+gap_m), Inches(2.0), w_m, Inches(1.9), bg_color=COLOR_LIGHT_BG)
        tb_m = s3.shapes.add_textbox(x0 + i*(w_m+gap_m) + Inches(0.22), Inches(2.15), w_m - Inches(0.44), Inches(1.6))
        tfm = tb_m.text_frame
        tfm.word_wrap = True
        p0 = tfm.paragraphs[0]
        p0.text = num
        p0.font.name = FONT_HEAD
        p0.font.size = Pt(36 if "→" in num else 44)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE
        p1 = tfm.add_paragraph()
        p1.text = title
        p1.font.name = FONT_BODY
        p1.font.size = Pt(13.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p2 = tfm.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_formatted_card(s3, Inches(0.8), Inches(4.2), Inches(5.68), Inches(2.6), "COMMERCIAL ADVANTAGE", "Why Cafes Switch to Alandas", [
        "Aesthetic Teebar counter display elevates cafe interior design instantly",
        "Whole-leaf brewing ritual justifies €4.50 - €6.00 premium menu price",
        "Ultra-thick shatter-resistant teapot solves baristas' breakage fears",
        "Replaces low-margin supermarket tea bags with an artisan experience"
    ], title_size=18, bullet_size=12)
    add_formatted_card(s3, Inches(6.85), Inches(4.2), Inches(5.68), Inches(2.6), "FINANCIAL ADVANTAGE", "Compounding Account Economics", [
        "First order Starter Crate establishes €249 netto immediate hardware revenue",
        "Average venue consumes 4 to 8 pouches/month (€50 to €150 netto replenishment)",
        "Phase 1: 25 accounts (€2,500–€5k/mo) → Master Goal: 100 accounts (€15,000–€30,000/mo)",
        "Predictable recurring cash flow allowing Sidy to quit his Swiss job & be his own boss again"
    ], title_size=18, bullet_size=12)

    # SLIDE 4
    print("Building Slide 4: Operational Diagnosis...")
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "03 // Current Bottlenecks", "Operational Diagnosis: Where Friction Lives",
               "The current commercial process relies on founder manual effort at every step, creating leaks across the funnel.")
    add_footer(s4, 4)

    frictions = [
        ("GAP 01", "Fragmented Lead Capture", [
            "Inquiries scattered across 2 Instagram accounts, WhatsApp, and website email",
            "Incoming leads need central routing into Dolibarr CRM"
        ]),
        ("GAP 02", "Unsystematic Qualification", [
            "No automated filter for venue size or intent",
            "Time wasted on home consumers asking for free wholesale samples"
        ]),
        ("GAP 03", "Undefined Trial Journey", [
            "Sample requests handled ad-hoc without structured follow-up cadence",
            "Trial kit needs standardized €19 credited offer and tasting protocol"
        ]),
        ("GAP 04", "Manual WhatsApp Orders & AI Fragility", [
            "Clients text paper order photos and voice notes via WhatsApp",
            "Hermes AI previously crashed and lost prompts without containerized state"
        ]),
        ("GAP 05", "Memory-Based Reorders", [
            "Refills depend entirely on customer remembering to reorder",
            "Alandas does not anticipate inventory depletion automatically"
        ]),
        ("GAP 06", "Founder Dual-Workload Strain", [
            "Sidy manages WhatsApp chats while working full-time in Switzerland",
            "Uncontained bots hallucinated ecological claims; requires human-in-the-loop"
        ])
    ]
    w_f = Inches(3.72)
    h_f = Inches(2.25)
    gap_xf = Inches(0.28)
    gap_yf = Inches(0.22)
    for i, (tag, title, bullets) in enumerate(frictions):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * (w_f + gap_xf)
        y = Inches(2.0) + row * (h_f + gap_yf)
        add_formatted_card(s4, x, y, w_f, h_f, tag, title, bullets, tag_color=COLOR_OCHRE, title_size=15, bullet_size=11.5)

    # SLIDE 5
    print("Building Slide 5: B2B vs B2C...")
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "04 // Strategic Separation", "B2C Has a Different Problem",
               "B2C e-commerce and B2B wholesale serve completely different unit economics and must be treated as separate workstreams.")
    add_footer(s5, 5)

    add_formatted_card(s5, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "B2B WHOLESALE ENGINE", "Account-Level Relationship & Retention", [
        "Customer: Cafe owners, F&B directors, boutique hotels, baristas",
        "Sales Cycle: 7 - 21 days from sample trial to Starter Crate setup",
        "Order Value: €249 Day-1 setup + €150–€300 monthly recurring refills",
        "Hardware Hook: Ultra-thick shatter-resistant teapot breaks cafe resistance",
        "Primary Goal: Scale from 25 verified venues to 100 recurring accounts across Germany",
        "Freedom Metric: €15,000–€30,000/mo recurring revenue to transition Sidy 100% full-time"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s5, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "B2C E-COMMERCE FUNNEL", "Consumer Traffic, Conversion & Gifting", [
        "Customer: Premium home tea drinkers, gift givers, aesthetic lifestyle buyers",
        "Sales Cycle: Impulse / 24-hour decision on mobile",
        "Order Value: €25 - €60 average order value (AOV)",
        "Core Bottleneck: Funnel drop-offs, shipping threshold friction, cart abandonment",
        "Primary Goal: Automate retention emails & optimize checkout conversion",
        "Leverage: Brand prestige, word-of-mouth, holiday gifting surges"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # SLIDE 6
    print("Building Slide 6: Why Start with B2B...")
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "05 // Strategic Focus", "Why Start with B2B Wholesale First?",
               "There is already a formal offer, customer proof, and catalog. B2B represents the highest ROI for early engineering investment.")
    add_footer(s6, 6)

    reasons = [
        ("REASON 01", "Existing Market Proof", [
            "25 active hospitality venues prove product-market fit immediately across Germany",
            "No need to hypothesize customer interest"
        ]),
        ("REASON 02", "Predictable Path to Freedom", [
            "100 cafe accounts generate €180,000 to €360,000 in annual recurring revenue",
            "Provides stable cash flow so Sidy can transition 100% to Alandas"
        ]),
        ("REASON 03", "Finite, Mappable Journey", [
            "B2B has exact linear steps: Lead → Qualify → €19 Trial → Crate → Refill",
            "Easy to instrument and automate inside Dolibarr"
        ]),
        ("REASON 04", "Immediate Founder Leverage", [
            "Streamlines 10–20 daily WhatsApp chats with AI-assisted drafting",
            "Sidy stays in control of customer chats while AI handles Dolibarr invoices"
        ]),
        ("REASON 05", "Living Billboards", [
            "Every cafe serving Alandas acts as a branded showroom for retail consumers",
            "Drives passive B2C awareness nationwide"
        ])
    ]
    w_r = Inches(2.18)
    gap_r = Inches(0.20)
    for i, (tag, title, bullets) in enumerate(reasons):
        x = Inches(0.8) + i * (w_r + gap_r)
        add_formatted_card(s6, x, Inches(2.0), w_r, Inches(4.8), tag, title, bullets, title_size=15, bullet_size=11.5)

    # SLIDE 7
    print("Building Slide 7: Account Economics...")
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "06 // Economic Model", "What Account Economics Mean for Alandas",
               "Average Order Value is a consumer metric. In B2B wholesale, revenue is unlocked through compounding Account Lifetime Value toward 100 active accounts.")
    add_footer(s7, 7)

    cards_econ = [
        ("TRANSACTION 1", "Day-1 Starter Crate", [
            "€249.00 Netto Retail",
            "Teebar counter rack + 6 jars + 6 heavy glass pots + trays + spoon + 6 pouches",
            "Ultra-thick shatter-proof glass teapots solve breakage fears",
            "Alandas Hardware Margin: €43.20 + turnkey counter presence"
        ]),
        ("TRANSACTION 2+", "Monthly Replenishment", [
            "€150 - €300 Netto / Month",
            "Average cafe orders 4 to 8 replacement pouches every 25 days",
            "Alandas Tea Margin: ~65% gross profit",
            "Automated reorder triggers on Day 25 via Dolibarr & WhatsApp"
        ]),
        ("COMPOUNDING", "Annual Account Value", [
            "Phase 1: 25 active partner accounts generate €50,000 - €95,000 recurring base",
            "Master Goal: 100 accounts scale past €180,000–€360,000 recurring ARR",
            "Yields €15,000–€30,000/mo gross margin for Alandas",
            "Delivers full financial independence & sustainable wholesale operations"
        ])
    ]
    w_e = Inches(3.72)
    gap_e = Inches(0.28)
    for i, (tag, title, bullets) in enumerate(cards_econ):
        x = Inches(0.8) + i * (w_e + gap_e)
        add_formatted_card(s7, x, Inches(2.0), w_e, Inches(4.8), tag, title, bullets, title_size=18, bullet_size=12)

    # SLIDE 8
    print("Building Slide 8: The 9-Stage Customer Journey...")
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "07 // Pipeline Architecture", "The Managed 9-Stage B2B Journey",
               "Every hospitality relationship follows an exact linear path with a visible stage, assigned owner, and automated trigger.")
    add_footer(s8, 8)

    stages_9 = [
        ("01", "PROSPECT", "Target cafe identified across German dining clusters (Berlin, Munich, Hamburg, Frankfurt, NRW)"),
        ("02", "ENQUIRY", "Inbound DM on B2B Instagram or response to outbound 96% gross margin pitch"),
        ("03", "QUALIFY", "60-sec intake scores seating capacity, volume & commercial intent"),
        ("04", "TRIAL", "€19.00 credited trial box (ultra-thick teapot + tray + spoon + 5 blends) dispatched"),
        ("05", "SALES", "Day-4 structured tasting review & Starter Crate proposal call"),
        ("06", "ORDER", "€249 Starter Crate invoiced via Dolibarr & delivered with turnkey display ware"),
        ("07", "ONBOARD", "Counter display installed & staff brewing cheat sheets deployed"),
        ("08", "REORDER", "Day-25 predictive refill prompt dispatched automatically via WhatsApp"),
        ("09", "EXPAND", "Multi-venue group rollout & seasonal iced tea menu rotations across Germany")
    ]
    w_s = Inches(3.72)
    h_s = Inches(1.45)
    gap_xs = Inches(0.28)
    gap_ys = Inches(0.18)
    for i, (num, name, desc) in enumerate(stages_9):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * (w_s + gap_xs)
        y = Inches(2.0) + row * (h_s + gap_ys)
        create_card(s8, x, y, w_s, h_s, bg_color=COLOR_CARD_BG)
        tb_s = s8.shapes.add_textbox(x + Inches(0.22), y + Inches(0.14), w_s - Inches(0.44), h_s - Inches(0.28))
        tfs = tb_s.text_frame
        tfs.word_wrap = True
        p0 = tfs.paragraphs[0]
        p0.text = f"STAGE {num} // {name}"
        p0.font.name = FONT_BODY
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE
        p1 = tfs.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.color.rgb = COLOR_TEXT_MUTED

    # SLIDE 9
    print("Building Slide 9: Lead Generation...")
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "08 // Acquisition Channels", "Lead Generation: Building Top-of-Funnel",
               "Combining automated inbound conversion with targeted outbound prospecting across Germany's top culinary hubs.")
    add_footer(s9, 9)

    add_formatted_card(s9, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "INBOUND ENGINE", "Dual Instagram & Web Capture", [
        "Dual Instagram Channels: B2C @alandastea + dedicated B2B hospitality profile",
        "Automation: OpenReply comment-to-DM triggers on keywords ('TEABAR', 'TASTE')",
        "Immediate Action: Direct DM sends interactive 60-second B2B qualification link",
        "Website Capture: Dedicated B2B landing page on Alandas.de with direct WhatsApp button",
        "Conversion Target: 10 - 15 warm inbound hospitality inquiries / week"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s9, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "OUTBOUND ENGINE", "Nationwide Hospitality Blitz (Sprint to 100)", [
        "Target Metro Hubs: Berlin, Hamburg, Munich, Frankfurt, Cologne/Düsseldorf (NRW)",
        "Google Maps Scraping: Identify cafes serving specialty coffee/tea with 30+ seats",
        "Hook: 'How top German cafes generate 96% gross profit on table-side tea'",
        "Cadence: 3-touch personalized message (DM/Email → WhatsApp → Tasting Dispatch)",
        "Offer: €19 Credited Discovery Kit featuring the shatter-resistant glass teapot"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # SLIDE 10
    print("Building Slide 10: Qualification Framework...")
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "09 // Lead Qualification", "Qualification Framework: Filtering for Commercial Intent",
               "Qualification asks one fundamental question: Is there a real, profitable commercial opportunity here?")
    add_footer(s10, 10)

    criteria = [
        ("FIT", "Target Profile", [
            "Specialty hospitality venue",
            "Seating capacity > 30 seats",
            "Emphasis on quality food & coffee",
            "Design-conscious interior aesthetic"
        ]),
        ("NEED", "Pain Point / Gap", [
            "Currently serves low-grade tea bags",
            "Breakage fears with fragile glass teaware",
            "Seeking to increase breakfast check averages",
            "Desires table-side guest theater"
        ]),
        ("VALUE", "Account Potential", [
            "Serves minimum 15 - 30 hot beverages daily",
            "Potential monthly reorder > €150 netto",
            "Multi-location expansion potential",
            "Reliable payment track record"
        ]),
        ("TIMING", "Purchase Window", [
            "Actively revamping seasonal beverage menu",
            "Opening a new location or terrace",
            "Displeased with existing tea supplier",
            "Ready to trial within 7 days"
        ]),
        ("AUTHORITY", "Decision Maker", [
            "Contact is owner, general manager or head barista",
            "Direct WhatsApp access established",
            "Power to approve €249 initial setup",
            "Involved in tasting evaluation"
        ])
    ]
    w_c = Inches(2.18)
    for i, (tag, title, bullets) in enumerate(criteria):
        x = Inches(0.8) + i * (w_c + Inches(0.20))
        add_formatted_card(s10, x, Inches(2.0), w_c, Inches(4.8), tag, title, bullets, title_size=15, bullet_size=11.5)

    # SLIDE 11
    print("Building Slide 11: Practical Scoring Model...")
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10 // Lead Scoring", "Practical B2B Account Scoring Matrix",
               "Automating tier classification to ensure Sidy spends 80% of his time closing high-probability accounts.")
    add_footer(s11, 11)

    table_shape = s11.shapes.add_table(7, 4, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.7))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(2.0)
    table.columns[2].width = Inches(1.8)
    table.columns[3].width = Inches(4.733)

    headers = ["Evaluation Criterion", "Attribute Measured", "Score Weight", "Routing & Next Action"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_OLIVE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    scoring_data = [
        ("Premium Concept & Seating > 40", "Volume Capacity", "+2 Points", "Tier A: Priority €19 trial box + Founder WhatsApp outreach"),
        ("Already Serves Tea on Menu", "Category Validation", "+2 Points", "Tier A: Immediate comparison sample dispatch with heavy teapot"),
        ("High-Volume Breakfast / Brunch Venue", "Consumption Velocity", "+1 Point", "Tier A: Margin breakdown pitch focused on morning traffic"),
        ("Multiple Locations in Germany", "Expansion Potential", "+2 Points", "Tier A: Proposal prepared for group-level deployment"),
        ("Clear Quality Upgrade Intent Stated", "Buyer Readiness", "+2 Points", "Tier A/B: Fast-track to €19 trial box & Starter Crate closing call"),
        ("Individual Consumer / Home Hobbyist", "Non-Commercial", "Disqualify", "Tier C: Route automatically to D2C retail e-commerce store")
    ]
    for i, row in enumerate(scoring_data):
        for j, val in enumerate(row):
            cell = table.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD_BG if i % 2 == 0 else COLOR_LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(11.5)
            p.font.color.rgb = COLOR_TEXT_MAIN if j != 2 else (COLOR_OLIVE if "+" in val else COLOR_OCHRE)
            if j == 2:
                p.font.bold = True

    # SLIDE 12
    print("Building Slide 12: Discovery Questions...")
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "11 // Diagnostic Discovery", "What We Must Learn First: Discovery Audit",
               "Building without evidence creates expensive software. Discovery replaces assumptions with verified operational facts.")
    add_footer(s12, 12)

    q_cards = [
        ("VOLUME & INQUIRIES", "Funnel Inputs", [
            "How many B2B wholesale inquiries arrive each month?",
            "What percentage come from Instagram vs referrals vs website?",
            "How many €19 trial boxes are currently dispatched monthly?",
            "What is the cost of shipping kits to unverified leads?"
        ]),
        ("CONVERSION & PRICING", "Sales Velocity", [
            "What percentage of sample recipients become paying accounts?",
            "What is the average first-order basket value (€)?",
            "How do cafe owners react to the heavy borosilicate teapot?",
            "How long does it take from first chat to payment clearance?"
        ]),
        ("RETENTION & WORKLOAD", "Account Health", [
            "How many days between an active venue's refills in Dolibarr?",
            "How to stabilize Dolibarr CRM & Hermes AI order parsing?",
            "How to support Sidy managing 10–20 daily WhatsApp chats?",
            "What happens when a warm prospect goes quiet on WhatsApp?"
        ])
    ]
    w_q = Inches(3.72)
    gap_q = Inches(0.28)
    for i, (tag, title, bullets) in enumerate(q_cards):
        x = Inches(0.8) + i * (w_q + gap_q)
        add_formatted_card(s12, x, Inches(2.0), w_q, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE, title_size=18, bullet_size=12)

    # SLIDE 13
    print("Building Slide 13: Evidence-Based Loop...")
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "12 // Operating Method", "The Evidence-Based Intervention Loop",
               "Every engineering and commercial change follows a disciplined scientific progression.")
    add_footer(s13, 13)

    steps = [
        ("01", "OBSERVATION", "Observation", "Founder texts cafes manually; cafes ghost or fear fragile glass teaware breaking in busy dining service."),
        ("02", "EVIDENCE", "Evidence", "Free samples attract non-commercial leads, while cafe owners' #1 objection is fragile glass teapots."),
        ("03", "CONSEQUENCE", "Consequence", "Capital bled on freebies, while serious cafe buyers hesitate due to teaware durability concerns."),
        ("04", "HYPOTHESIS", "Hypothesis", "Requiring a €19.00 credited trial box featuring the shatter-resistant teapot eliminates tire-kickers and proves durability."),
        ("05", "INTERVENTION", "Intervention", "Deploy 60-second intake filter, showcase heavy glass durability, and automate Dolibarr invoicing."),
        ("06", "MEASUREMENT", "Measurement", "Track 30-day trial-to-Starter-Crate conversion and quantify weekly founder hours saved.")
    ]
    w_st = Inches(3.72)
    h_st = Inches(2.25)
    gap_xst = Inches(0.28)
    gap_yst = Inches(0.22)
    for i, (num, tag, title, desc) in enumerate(steps):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * (w_st + gap_xst)
        y = Inches(2.0) + row * (h_st + gap_yst)
        create_card(s13, x, y, w_st, h_st, bg_color=COLOR_CARD_BG)
        tb_st = s13.shapes.add_textbox(x + Inches(0.24), y + Inches(0.22), w_st - Inches(0.48), h_st - Inches(0.44))
        tfst = tb_st.text_frame
        tfst.word_wrap = True
        p0 = tfst.paragraphs[0]
        p0.text = f"STAGE {num}"
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE if i < 3 else COLOR_OCHRE
        p0.space_after = Pt(4)
        p1 = tfst.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(6)
        p2 = tfst.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # SLIDE 14
    print("Building Slide 14: Phase 1...")
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "13 // Phase 1 Roadmap", "Phase 1: Discover & Validate Current Operations",
               "Map the real B2B process, quantify volume, conversion, order economics, and founder manual workload.")
    add_footer(s14, 14)

    add_formatted_card(s14, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "DISCOVERY WORKSTREAM", "Auditing the Ground Truth", [
        "Audit existing Dolibarr CRM database, customer records, and product margins",
        "Containerize and stabilize Hermes AI with persistent prompt templates",
        "Calculate true gross margin on bulk pouches vs glass jars vs tea ware",
        "Review the 25 live accounts to map reorder frequency and consumption velocity",
        "Log exact hours Sidy spends balancing his day job with WhatsApp operations"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s14, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "CORE DELIVERABLES", "Outputs of Phase 1", [
        "Dolibarr CRM API integration & automated cloud backup architecture",
        "Shatter-resistant teapot positioning & €19 trial box pricing synchronization",
        "Customer Lifetime Value (LTV) & Churn Benchmark across the 25 active venues",
        "Founder Time Allocation Audit (Identifying automatable drafting hours)",
        "Sprint roadmap toward 100 active accounts across Germany"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # SLIDE 15
    print("Building Slide 15: Phase 2...")
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "14 // Phase 2 Roadmap", "Phase 2: Fix Storefront Commercial Friction",
               "Resolving contradictory pricing, sample clarity, out-of-stock equipment, and local trust blockers.")
    add_footer(s15, 15)

    fixes = [
        ("FIX 01", "€19 Discovery Box Price Sync", [
            "Standardize €19 trial box (heavy teapot, tray, spoon, 5 blends) across web & DMs",
            "Clarify 100% credit policy against subsequent €249 Starter Crate"
        ]),
        ("FIX 02", "Partner Social Proof", [
            "Publish interactive map and logo grid of the 25 live partner cafes across Germany",
            "Establish immediate hospitality credibility in major metro dining hubs"
        ]),
        ("FIX 03", "Highlight Teapot Durability", [
            "Address cafe owners' #1 objection: feature the ultra-thick, shatter-resistant glass",
            "Reassure baristas that Alandas teapots withstand commercial dishwashers"
        ]),
        ("FIX 04", "Teebar Pre-Order Status", [
            "Remove 'out of stock' badge from Teebar countertop display",
            "Enable 'B2B Pre-Order / Included with Turnkey Setup'"
        ]),
        ("FIX 05", "Shipping Threshold Policy", [
            "Eliminate €59 vs €40 conflict across store",
            "Unify free shipping threshold clearly at €49 across store"
        ])
    ]
    w_fx = Inches(2.18)
    for i, (tag, title, bullets) in enumerate(fixes):
        x = Inches(0.8) + i * (w_fx + Inches(0.20))
        add_formatted_card(s15, x, Inches(2.0), w_fx, Inches(4.8), tag, title, bullets, tag_color=COLOR_OCHRE, title_size=15, bullet_size=11.5)

    # SLIDE 16
    print("Building Slide 16: Phase 3...")
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "15 // Phase 3 Roadmap", "Phase 3: Build the Multi-Channel Lead Engine",
               "Target top hospitality accounts, establish multi-channel acquisition, and centralize all incoming inquiries.")
    add_footer(s16, 16)

    add_formatted_card(s16, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "INBOUND CAPTURE ARCHITECTURE", "Dual Instagram & OpenReply Loop", [
        "Dual Instagram strategy: Retail on @alandastea, wholesale on B2B page",
        "Automate comment triggers ('TASTE', 'TEABAR', 'B2B') on video reels",
        "Send personalized Instagram DM with instant 60-second qualification link",
        "Install floating WhatsApp B2B chat widget on high-intent website pages",
        "Capture 100% of social interest directly into Dolibarr CRM pipeline"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s16, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "OUTBOUND CAMPAIGN ENGINE", "Nationwide Hospitality Blitz (Sprint to 100)", [
        "Compile target database of 100 high-potential cafes across German dining hubs",
        "Google Maps automated discovery of specialty cafes and brunch venues",
        "Deploy 3-touch outreach sequence focusing on beverage gross margins",
        "Offer €19 credited trial box with ultra-thick shatter-resistant teapot",
        "Target milestone: 25 active discovery tasting evaluations booked in 14 days"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # SLIDE 17
    print("Building Slide 17: Phase 4...")
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "16 // Phase 4 Roadmap", "Phase 4: Qualification & Trial Automation",
               "Score leads, route them intelligently, dispatch credited trial boxes, and automate structured follow-up.")
    add_footer(s17, 17)

    add_formatted_card(s17, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "AUTOMATED QUALIFICATION INTAKE", "60-Second Scoring Filter", [
        "Step 1: Collect venue name, address, website / Instagram handle",
        "Step 2: Collect seating capacity (<20, 20-50, >50 seats)",
        "Step 3: Capture current tea setup (teabags, loose-leaf, none)",
        "Tier A Routing (>40 seats): Immediate WhatsApp notification to Sidy",
        "Tier C Routing (Home consumer): Polite redirect to D2C retail store",
        "Charge €19.00 credited fee for trial box (heavy teapot + tray + spoon + 5 blends)"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s17, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "4-TOUCH TRIAL CADENCE", "Structured Follow-Up Automation", [
        "Day 0: WhatsApp dispatch notice with tracking and digital tasting menu",
        "Day 2: Delivery confirmation + whole-leaf brewing temperature cheat sheet",
        "Day 4: Interactive survey: 'How did the teapot handle and which blend was your favorite?'",
        "Day 7: €249 Starter Crate proposal with €19 credit deducted automatically",
        "Consequence: Eliminates leads ghosting after sample delivery"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # SLIDE 18
    print("Building Slide 18: Phase 5...")
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "17 // Phase 5 Roadmap", "Phase 5: Sales Conversion & Turnkey Onboarding",
               "Standardize the Turnkey Starter Crate pitch, barista brewing education, and Day-1 counter rollout.")
    add_footer(s18, 18)

    add_formatted_card(s18, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "THE €249 NETTO STARTER CRATE", "Turnkey Beverage Profit Center", [
        "Handcrafted wooden Teebar countertop display rack",
        "6 airtight borosilicate glass display jars with cork stoppers",
        "6 ultra-thick shatter-resistant borosilicate glass teapots with infusers",
        "6 bamboo serving presentation trays + stainless/wooden dosing spoon",
        "6 commercial 220g pouches (yielding 330 premium cafe pots)",
        "Financial pitch: Cafe generates €1,650 gross revenue from Day-1 crate"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s18, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "BARISTA TRAINING & LAUNCH", "Zero Friction Counter Deployment", [
        "Laminated counter cheat sheet: Water temp (80°C vs 100°C) & steeping times",
        "Pre-measured dosing spoon eliminates tea leaf waste and over-infusion",
        "Digital brewing video guide accessible via QR code on display rack",
        "Instant Dolibarr PDF invoice generation upon WhatsApp confirmation",
        "Result: Baristas brew perfect tea even during chaotic rush hours"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # SLIDE 19
    print("Building Slide 19: Phase 6...")
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "18 // Phase 6 Roadmap", "Phase 6: Replenishment & Predictive Reorders",
               "Track purchasing patterns, trigger timely reorder reminders, and make reordering effortless.")
    add_footer(s19, 19)

    add_formatted_card(s19, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "CONSUMPTION PREDICTION MODEL", "Anticipating Inventory Depletion", [
        "Baseline metric: 220g pouch = ~55 pots of tea at 4g/dose",
        "Average cafe serving 15 pots/day depletes 6 pouches in ~22 days",
        "Trigger Day 20: Gentle check-in: 'How are your jars looking for the weekend?'",
        "Trigger Day 25: 1-click reorder link sent via WhatsApp with draft Dolibarr invoice",
        "Eliminates running out of stock and emergency last-minute rush deliveries"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s19, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "CHURN PREVENTION & HEALTH", "Active Account Monitoring", [
        "Dolibarr CRM alert triggered if an active account passes Day 35 without reordering",
        "Founder check-in prompt: 'Did seasonal foot traffic change or blends run out?'",
        "Quarterly blend rotation: Introducing fresh seasonal herbal and iced blends",
        "Wholesale customer portal: Fast re-ordering with instant PDF tax invoice",
        "Result: 90-day account retention rate maintained above 85%"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # SLIDE 20
    print("Building Slide 20: Phase 7...")
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "19 // Phase 7 Roadmap", "Phase 7: B2C Growth & Account Expansion",
               "Strengthen B2C e-commerce retention and expand successful B2B accounts across multi-venue groups.")
    add_footer(s20, 20)

    add_formatted_card(s20, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "B2B ACCOUNT EXPANSION", "The 'Land & Expand' Playbook", [
        "Multi-Venue Expansion: Rolling Alandas into sister locations of existing accounts across Germany",
        "Seasonal Menu Programs: Summer artisan cold brew iced tea menus",
        "Counter Retail Display: Supplying 220g retail pouches for cafe guest take-home",
        "Corporate Gifting: Packaging premium tea chests for hospitality corporate clients",
        "Impact: Doubles average account value without acquiring new venues"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s20, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "B2C E-COMMERCE ACCELERATION", "Scaling the Direct-to-Consumer Engine", [
        "Deploy automated post-purchase brewing education email sequence",
        "Introduce whole-leaf loose tea monthly home refill subscriptions",
        "Curate luxury gifting bundles for Q4 Christmas and holiday spikes",
        "Leverage hospitality partner foot traffic via on-menu QR codes",
        "Impact: Scalable consumer e-commerce running on full autopilot"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # SLIDE 21
    print("Building Slide 21: Technical Architecture...")
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "20 // Systems Blueprint", "Technical Architecture: Orchestrating the Machine",
               "The automation layer orchestrates the business without creating technical debt or fragile complexity.")
    add_footer(s21, 21)

    tech_layers = [
        ("LAYER 01", "Touchpoints", [
            "Dual Instagram Profiles (B2C & B2B)",
            "WhatsApp Business (Sidy human-in-the-loop)",
            "Shopify Storefront (Alandas.de)",
            "Typeform / Tally B2B Intake Form",
            "Google Maps Cafe Lead Scraper"
        ]),
        ("LAYER 02", "Orchestration & AI", [
            "Hermes AI Order Parser (Vision & Text)",
            "OpenReply Instagram Comment-to-DM",
            "Meta Ads MCP Optimization Agent",
            "Deterministic Follow-up Rules",
            "Dockerized Containerized Service"
        ]),
        ("LAYER 03", "System of Record", [
            "Dolibarr CRM & ERP (System of Record)",
            "Automated Cloud Backups & REST API",
            "Venue Profiles & Lead Scores",
            "Inventory Stock & Reorder Tracker",
            "PDF Invoices & Tax Documentation"
        ]),
        ("LAYER 04", "Commerce & Ops", [
            "Shopify B2B Wholesale Engine",
            "SEPA & Direct Bank Transfer",
            "DHL / DPD Tracking Integration",
            "Hardware Starter Crate Assembly",
            "Predictive Reorder Schedule"
        ])
    ]
    w_t = Inches(2.72)
    for i, (tag, title, bullets) in enumerate(tech_layers):
        x = Inches(0.8) + i * (w_t + Inches(0.28))
        add_formatted_card(s21, x, Inches(2.0), w_t, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE, title_size=16, bullet_size=11.5)

    # SLIDE 22
    print("Building Slide 22: Where AI Fits...")
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "21 // Intelligent Automation", "Automation Philosophy: AI-Native, Not AI-Everywhere",
               "Rigidly separating where AI accelerates workflows from where deterministic code and human judgment must govern.")
    add_footer(s22, 22)

    add_formatted_card(s22, Inches(0.8), Inches(2.0), Inches(3.72), Inches(4.8), "AI ACCELERATION", "Unstructured to Structured Tasks", [
        "Hermes WhatsApp Order Extraction: Transcribes paper note photos & voice notes into line items",
        "Google Maps Prospecting: Identifies German cafes serving coffee/tea with seat counts",
        "Meta Ads MCP Optimization: Automatically halts underperforming ads and scales winners",
        "Drafting WhatsApp Responses: Generates contextual reply drafts for Sidy to approve in 1 tap",
        "Message Classification: Categorizes DMs into Wholesale vs Retail vs Support"
    ], tag_color=COLOR_OLIVE, title_size=18, bullet_size=12)

    add_formatted_card(s22, Inches(4.8), Inches(2.0), Inches(3.72), Inches(4.8), "DETERMINISTIC LOGIC", "Zero Guesswork / 100% Rules", [
        "Dolibarr Invoice Generation: Exact VAT, item codes, and pricing calculation with zero errors",
        "Zero Botanical Hallucinations: Enforces verified ecological claims to prevent regulatory fines",
        "Lead Scoring: Strict mathematical calculation (seats, tea presence, location)",
        "Inventory Truth: Live stock decrement and low-inventory alerts",
        "Follow-Up Policies: Sending Day 2/4/7 messages at exact timestamps"
    ], tag_color=COLOR_OCHRE, title_size=18, bullet_size=12)

    add_formatted_card(s22, Inches(8.8), Inches(2.0), Inches(3.72), Inches(4.8), "HUMAN EXECUTIVE ROLE", "Sidy's High-Leverage Superpower", [
        "Sidy Manages WhatsApp Chats: Directly interacts with 10–20 cafe owners daily to build trust",
        "Sensory Tastings & Hospitality Deals: Sidy leads high-value partner relationships",
        "Commercial Negotiation: Agreeing terms on multi-venue regional accounts",
        "Custom Blends: Designing bespoke tea recipes for luxury hotels",
        "Strategic Exceptions: Handling bespoke partner requests"
    ], tag_color=COLOR_TEXT_MAIN, title_size=18, bullet_size=12)

    # SLIDE 23
    print("Building Slide 23: B2C Workstream...")
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "22 // Parallel Operations", "The Parallel B2C E-Commerce Workstream",
               "Run B2C optimization in parallel, but do not let it distract from proving the core B2B wholesale engine.")
    add_footer(s23, 23)

    b2c_steps = [
        ("STAGE 1", "Discover", [
            "SEO optimization for organic whole-leaf tea",
            "Instagram aesthetics & brewing reels on @alandastea",
            "Customer referrals & gifting shares"
        ]),
        ("STAGE 2", "Consider", [
            "Origin transparency & organic certifications",
            "Customer tasting reviews and ratings",
            "Clear brewing instructions & taste profiles"
        ]),
        ("STAGE 3", "Convert", [
            "Unify shipping threshold copy at €49",
            "1-click mobile checkout (Apple Pay / PayPal)",
            "Sync €19 trial kit across store"
        ]),
        ("STAGE 4", "Retain", [
            "Post-purchase email: How to brew loose-leaf",
            "Day 40 replenishment reminder sequence",
            "Seasonal gifting catalog for winter/holidays"
        ])
    ]
    w_b = Inches(2.72)
    for i, (tag, title, bullets) in enumerate(b2c_steps):
        x = Inches(0.8) + i * (w_b + Inches(0.28))
        add_formatted_card(s23, x, Inches(2.0), w_b, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE, title_size=16, bullet_size=11.5)

    # SLIDE 24
    print("Building Slide 24: B2B Scoreboard...")
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "23 // Operational Scoreboard", "B2B Measurement: The Commercial Dashboard",
               "The operating system requires a real-time scoreboard to measure pipeline velocity and identify conversion bottlenecks.")
    add_footer(s24, 24)

    kpis_b2b = [
        ("INQUIRY VELOCITY", "15 - 25 Leads / Mo", [
            "Target weekly inflow of qualified hospitality leads",
            "Measured across Inbound DM and Outbound blitz"
        ]),
        ("QUALIFICATION RATE", "60% Pass Tier A/B", [
            "Percentage of inquiries meeting seating & commercial criteria",
            "Instantly filters out retail tire-kickers"
        ]),
        ("TRIAL CONVERSION", "70% Order €19 Kit", [
            "Percentage of qualified leads ordering €19 credited box",
            "Puts durable teapot directly in baristas' hands"
        ]),
        ("STARTER CRATE CLOSE", "40% Close Rate", [
            "Percentage of trial box recipients ordering €249 Starter Crate",
            "Generates immediate positive ROI on acquisition"
        ]),
        ("ACTIVE VENUES TARGET", "100 Accounts", [
            "Phase 1: 25 active venues (€3k–€5k/mo) → Master Goal: 100 accounts (€15k–€30k/mo)",
            "Achieves full founder independence"
        ]),
        ("FOUNDER WORKLOAD", "10–20 Chats / Day", [
            "Sidy manages high-touch WhatsApp relationships effortlessly with AI drafting",
            "Zero bot hallucination risk with human-in-the-loop"
        ])
    ]
    w_k = Inches(3.72)
    h_k = Inches(2.25)
    gap_xk = Inches(0.28)
    gap_yk = Inches(0.22)
    for i, (name, val, bullets) in enumerate(kpis_b2b):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * (w_k + gap_xk)
        y = Inches(2.0) + row * (h_k + gap_yk)
        create_card(s24, x, y, w_k, h_k, bg_color=COLOR_CARD_BG)
        tb_k = s24.shapes.add_textbox(x + Inches(0.24), y + Inches(0.20), w_k - Inches(0.48), h_k - Inches(0.40))
        tfk = tb_k.text_frame
        tfk.word_wrap = True
        p0 = tfk.paragraphs[0]
        p0.text = name
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE
        p1 = tfk.add_paragraph()
        p1.text = val
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(4)
        for b in bullets:
            pb = tfk.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(11)
            pb.font.color.rgb = COLOR_TEXT_MUTED

    # SLIDE 25
    print("Building Slide 25: B2C Telemetry...")
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "24 // Commerce Analytics", "B2C Telemetry: Making Commerce Observable",
               "Instrumenting the e-commerce funnel with modern event telemetry before scaling acquisition budgets.")
    add_footer(s25, 25)

    add_formatted_card(s25, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "FULL-FUNNEL EVENT TRACKING", "GA4 + Google Tag Manager", [
        "Event 01 (view_item): Track engagement on product detail pages",
        "Event 02 (add_to_cart): Monitor product selection & cart additions",
        "Event 03 (begin_checkout): Measure transition to payment flow",
        "Event 04 (purchase): Verify conversion, revenue, and product basket mix",
        "Meta CAPI: Server-side Conversions API for privacy-compliant ad attribution"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s25, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "AUTOMATED LIFECYCLE FLOWS", "Klaviyo / Brevo Retention Loops", [
        "Welcome Sequence: Brand story, organic sourcing, whole-leaf education (3 emails)",
        "Abandoned Cart Recovery: 1h / 24h triggers with free shipping incentive",
        "Post-Purchase Onboarding: Brewing temperature video & accessories guide",
        "Replenishment Prompt: Triggered at Day 45 based on tea consumption volume",
        "Win-Back Flow: Special reserve blend offer for dormant customers at Day 90"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # SLIDE 26
    print("Building Slide 26: What Success Looks Like...")
    s26 = prs.slides.add_slide(blank_layout)
    add_header(s26, "25 // Future State", "What Success Looks Like for Alandas",
               "A commercial operating system that makes revenue opportunities visible, systematic, and compounding.")
    add_footer(s26, 26)

    outcomes = [
        ("A Lead Enters Once", "Centralized Capture", "No inquiry is ever lost in unread Instagram DMs or fragmented WhatsApp messages across personal devices."),
        ("A Lead Is Understood", "Automated Intake", "Venue profile, seat count, and intent scored before Sidy spends a single minute texting."),
        ("A Trial Has a Journey", "Managed Follow-Up", "The €19 trial box puts the shatter-resistant teapot in the barista's hands, backed by an automated 4-touch follow-up."),
        ("A Customer Has a Next Action", "Predictive Refills", "Day 25 Dolibarr reorder reminders ensure steady wholesale cash flow and eliminate preventable cafe churn."),
        ("Management Sees the Funnel", "Real-Time Clarity", "Sidy tracks pipeline velocity and order logs without manual chaos, while continuing his day job until hitting the 100-account goal."),
        ("Founder Achieves Freedom", "Master Scale Milestone", "Scaling to 100 recurring accounts across Germany delivers €15k–€30k monthly gross margin, allowing Sidy to return to being his own boss full-time.")
    ]
    w_o = Inches(3.72)
    h_o = Inches(2.25)
    gap_xo = Inches(0.28)
    gap_yo = Inches(0.22)
    for i, (name, tag, desc) in enumerate(outcomes):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * (w_o + gap_xo)
        y = Inches(2.0) + row * (h_o + gap_yo)
        create_card(s26, x, y, w_o, h_o, bg_color=COLOR_CARD_BG)
        tb_o = s26.shapes.add_textbox(x + Inches(0.24), y + Inches(0.22), w_o - Inches(0.48), h_o - Inches(0.44))
        tfo = tb_o.text_frame
        tfo.word_wrap = True
        p0 = tfo.paragraphs[0]
        p0.text = tag.upper()
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE if i < 3 else COLOR_OCHRE
        p0.space_after = Pt(4)
        p1 = tfo.add_paragraph()
        p1.text = name
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(6)
        p2 = tfo.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # SLIDE 27
    print("Building Slide 27: 6-Sprint Roadmap...")
    s27 = prs.slides.add_slide(blank_layout)
    add_header(s27, "26 // Implementation Plan", "Proposed Master Roadmap: 6 Sprints to Scale",
               "Each phase earns the next through evidence, validating assumptions before expanding scope.")
    add_footer(s27, 27)

    sprints = [
        ("SPRINT 1", "Validate & Dolibarr", ["Audit volume & economics", "Stabilize Dolibarr CRM & API", "Fix 5 website blockers", "Sync €19 trial box offer"]),
        ("SPRINT 2", "Intake & Hermes AI", ["Deploy 60-sec intake form", "Harden Hermes AI order parser", "Launch €19 credited box", "Containerize prompts & backup"]),
        ("SPRINT 3", "Starter Crate & Outbound", ["Package €249 Starter Crate", "Scrape 100 German target cafes", "Launch margin-based outreach", "Highlight thick glass teapot"]),
        ("SPRINT 4", "Dual Instagram & Inbound", ["Connect OpenReply Instagram loop", "Deploy B2B comment-to-DM flows", "Automate 4-touch tasting cadence", "Install website WhatsApp widget"]),
        ("SPRINT 5", "Retention & Reorders", ["Deploy Day-25 refill automation", "Dolibarr WhatsApp refill prompts", "Barista counter cheat sheets", "Monitor account churn alerts"]),
        ("SPRINT 6", "Scale to 100 Accounts", ["Meta Ads MCP budget scaling", "Multi-venue hospitality rollouts", "GA4 / GTM e-commerce tracking", "Sidy transitions to full-time boss"])
    ]
    w_sp = Inches(1.81)
    gap_sp = Inches(0.17)
    for i, (tag, title, bullets) in enumerate(sprints):
        x = Inches(0.8) + i * (w_sp + gap_sp)
        add_formatted_card(s27, x, Inches(2.0), w_sp, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE if i < 3 else COLOR_OCHRE, title_size=14, bullet_size=11)

    # SLIDE 28
    print("Building Slide 28: Immediate First Step...")
    s28 = prs.slides.add_slide(blank_layout)
    add_header(s28, "27 // Immediate Kickoff", "The Immediate First Step: Mapping Ground Truth",
               "Before building software, we map the exact realities of Alandas' current B2B process.")
    add_footer(s28, 28)

    add_formatted_card(s28, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "SPRINT 1 DISCOVERY AGENDA", "7-Day Foundation & Mapping", [
        "1. Stabilize Sidy's Dolibarr CRM with automated backups and REST API access",
        "2. Re-establish Hermes AI WhatsApp order parsing with strict deterministic guardrails",
        "3. Triage the 5 website blockers (synchronize €19 trial box, fix out-of-stock badge, update map pin)",
        "4. Create the standardized 60-second B2B qualification intake filter",
        "5. Compile the first batch of 25 priority target cafes in Berlin, Munich, Hamburg & Frankfurt"
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    add_formatted_card(s28, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "CALL TO ACTION FOR SIDY", "The Next Decision Today", [
        "Commitment to the 100-Account Master Goal to transition Sidy back to full-time independence",
        "Agreement to keep Sidy as the human-in-the-loop on WhatsApp (10–20 chats/day) with AI drafting",
        "Approval to synchronize the €19 credited discovery box and highlight teapot durability",
        "Access to Dolibarr instance, Shopify admin, and Instagram credentials for integration",
        "Kick off Sprint 1 immediately to stabilize operations before tonight's strategic rollout"
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # Save presentation
    output_path = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\Alandas_Master_Growth_System.pptx"
    alt_output_path = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\Alandas_B2B_Growth_Customer_System.pptx"
    prs.save(output_path)
    prs.save(alt_output_path)
    print(f"\n[SUCCESS] Generated Master PowerPoint Decks:\n1. {output_path}\n2. {alt_output_path}")

if __name__ == "__main__":
    build_deck()
