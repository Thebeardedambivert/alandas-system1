import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

OUTPUT_PATH = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\Alandas_B2B_Growth_Deck.pptx"

# ==============================================================================
# COLOR PALETTE (Warm Linen & Botanical Olive Editorial System)
# ==============================================================================
C_BG            = RGBColor(249, 248, 245) # Warm Linen #F9F8F5
C_WHITE         = RGBColor(255, 255, 255) # Pure White #FFFFFF
C_INK           = RGBColor(28, 29, 26)    # Deep Charcoal #1C1D1A
C_INK_SEC       = RGBColor(74, 75, 69)    # Medium Charcoal #4A4B45
C_MUTED         = RGBColor(115, 116, 108) # Warm Grey #73746C
C_BORDER        = RGBColor(229, 227, 220) # Card Border #E5E3DC
C_BORDER_LIGHT  = RGBColor(239, 236, 230) # Inner Border #EFECE6

C_OLIVE         = RGBColor(85, 91, 62)    # Botanical Olive #555B3E
C_OLIVE_BG      = RGBColor(236, 239, 227) # Olive Tint #ECEFE3

C_GOLD          = RGBColor(158, 116, 39)  # Ochre/Gold #9E7427
C_GOLD_BG       = RGBColor(251, 244, 232) # Gold Tint #FBF4E8

C_GREEN         = RGBColor(46, 99, 71)    # Forest Green #2E6347
C_GREEN_BG      = RGBColor(238, 247, 242) # Green Tint #EEF7F2

C_CRIMSON       = RGBColor(146, 52, 52)   # Crimson Red #923434
C_CRIMSON_BG    = RGBColor(253, 242, 242) # Crimson Tint #FDF2F2

FONT_SERIF = "Georgia"
FONT_SANS  = "Arial"

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def add_base_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # Background fill
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = C_BG
    bg_shape.line.fill.background()
    return slide

def add_header(slide, kicker, title, lead=None):
    tx_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.55), Inches(11.5), Inches(1.3))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Kicker
    p_k = tf.paragraphs[0]
    p_k.text = kicker.upper()
    p_k.font.name = FONT_SANS
    p_k.font.size = Pt(8.5)
    p_k.font.bold = True
    p_k.font.color.rgb = C_OLIVE
    p_k.space_after = Pt(4)
    
    # Title
    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.name = FONT_SERIF
    p_t.font.size = Pt(25)
    p_t.font.bold = False
    p_t.font.color.rgb = C_INK
    p_t.space_after = Pt(4)
    
    # Lead
    if lead:
        p_l = tf.add_paragraph()
        p_l.text = lead
        p_l.font.name = FONT_SANS
        p_l.font.size = Pt(10.5)
        p_l.font.color.rgb = C_MUTED

def add_footer(slide, current_idx, total_slides=12):
    tx_box = slide.shapes.add_textbox(Inches(0.9), Inches(6.85), Inches(11.533), Inches(0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = "ALANDAS TEA BERLIN • COMMERCIAL OPERATING SYSTEM"
    p.font.name = FONT_SANS
    p.font.size = Pt(7.5)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.RIGHT
    p2.text = f"Slide {current_idx} of {total_slides}"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(7.5)
    p2.font.bold = True
    p2.font.color.rgb = C_MUTED

def add_card(slide, left, top, width, height, bg_color=C_WHITE, border_color=C_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

def add_callout(slide, left, top, width, height, text):
    callout = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    callout.fill.solid()
    callout.fill.fore_color.rgb = RGBColor(241, 239, 233)
    callout.line.color.rgb = C_OLIVE
    callout.line.width = Pt(2)
    
    tf = callout.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.1)
    tf.margin_bottom = Inches(0.1)
    
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = FONT_SANS
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_INK
    return callout

# ==============================================================================
# SLIDE BUILDERS
# ==============================================================================

def build_slide_1(prs):
    slide = add_base_slide(prs)
    
    # Title Block
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(1.1), Inches(11.5), Inches(2.3))
    tf = tx.text_frame
    tf.word_wrap = True
    
    pk = tf.paragraphs[0]
    pk.text = "ALANDAS TEA BERLIN • COMMERCIAL OPERATING SYSTEM"
    pk.font.name = FONT_SANS
    pk.font.size = Pt(9.5)
    pk.font.bold = True
    pk.font.color.rgb = C_OLIVE
    pk.space_after = Pt(12)
    
    pt = tf.add_paragraph()
    pt.text = "Connecting Your B2B Proposition to a Repeatable Revenue Engine"
    pt.font.name = FONT_SERIF
    pt.font.size = Pt(36)
    pt.font.bold = False
    pt.font.color.rgb = C_INK
    pt.space_after = Pt(10)
    
    pl = tf.add_paragraph()
    pl.text = "How we take your proven wholesale catalog, 13 partner venues, and retail storefront to build an automated customer acquisition, validation, and replenishment system."
    pl.font.name = FONT_SANS
    pl.font.size = Pt(12)
    pl.font.color.rgb = C_MUTED
    
    # 4 Overview Cards along the bottom
    cards_data = [
        ("01 // FOUNDATION", "13 Verified Venues", "Proven adoption across cafes, restaurants & lounges in Berlin, Bavaria & NRW."),
        ("02 // OFFER", "96% Cafe Margin", "€0.195 leaf cost vs €5 menu price. Unbeatable wholesale economics for operators."),
        ("03 // VALIDATION", "Automated Filter", "Eliminate tire-kickers with structured intake & €9.90 credited trial box."),
        ("04 // SCALE", "Self-Serve Portal", "Automate 30-day refills and free founder time from manual WhatsApp chats.")
    ]
    card_w = Inches(2.68)
    card_h = Inches(2.4)
    top_pos = Inches(3.9)
    gap = Inches(0.27)
    
    for i, (label, title, desc) in enumerate(cards_data):
        left_pos = Inches(0.9) + i * (card_w + gap)
        add_card(slide, left_pos, top_pos, card_w, card_h)
        
        tx_c = slide.shapes.add_textbox(left_pos + Inches(0.18), top_pos + Inches(0.18), card_w - Inches(0.36), card_h - Inches(0.36))
        tfc = tx_c.text_frame
        tfc.word_wrap = True
        tfc.margin_left = tfc.margin_right = tfc.margin_top = tfc.margin_bottom = 0
        
        p1 = tfc.paragraphs[0]
        p1.text = label
        p1.font.name = FONT_SANS
        p1.font.size = Pt(7.5)
        p1.font.bold = True
        p1.font.color.rgb = C_OLIVE
        p1.space_after = Pt(8)
        
        p2 = tfc.add_paragraph()
        p2.text = title
        p2.font.name = FONT_SANS
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_INK
        p2.space_after = Pt(6)
        
        p3 = tfc.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_SANS
        p3.font.size = Pt(9.2)
        p3.font.color.rgb = C_INK_SEC
        
    add_footer(slide, 1)

def build_slide_2(prs):
    slide = add_base_slide(prs)
    add_header(slide, "01 // Empirical Evidence", "You Have Already Built What Most Brands Struggle to Prove",
               "Your 24-page wholesale catalog reveals clear Product-Market Fit. The tea and concept work; the bottleneck is the commercial plumbing around it.")
    
    # 3 Cards Grid
    cards_data = [
        ("ADOPTION PROOF", "13 Venues", "Established Hospitality Roster", 
         "Active partner accounts across diverse dining categories:\n• Dining: Vesuvio Ristorante, Hürrem Sultan, La fiamma\n• Cafes/Brunch: Melt Creperie, Café Friedrichs\n• National Reach: Flawless (Würzburg), Huqqa & Junia (NRW)", C_GOLD_BG, C_GOLD),
        ("WHOLESALE ECONOMICS", "96% Margin", "The Cafe Operator Pitch Hook",
         "At your €10.74 netto wholesale price for 220g:\n• Yields 55 standard 330ml teapots (4g dosage)\n• Tea cost per pot: only €0.195\n• Sold at €5.00 menu price = €4.80 profit per pot\n• 25 pots/day = €3,600+ monthly net margin for the cafe.", C_GREEN_BG, C_GREEN),
        ("PRODUCT & HARDWARE", "18+ SKUs", "Turnkey Serving Ritual",
         "• 13 destination blends (Istanbul, Bombay, Paris, Marrakech)\n• Borosilicate glass pot (€10.86 net) + bamboo tray (€4.20 net)\n• Teebar wooden display rack (from €49 net)\n• Eliminates messy tea bag waste; creates a 90-second premium ritual.", C_WHITE, C_BORDER)
    ]
    card_w = Inches(3.64)
    card_h = Inches(4.0)
    top_pos = Inches(2.05)
    gap = Inches(0.29)
    
    for i, (tag, stat, title, body, bg_col, b_col) in enumerate(cards_data):
        left_pos = Inches(0.9) + i * (card_w + gap)
        add_card(slide, left_pos, top_pos, card_w, card_h, bg_col, b_col)
        
        tx = slide.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p1 = tf.paragraphs[0]
        p1.text = tag
        p1.font.name = FONT_SANS
        p1.font.size = Pt(8)
        p1.font.bold = True
        p1.font.color.rgb = b_col
        
        p_stat = tf.add_paragraph()
        p_stat.text = stat
        p_stat.font.name = FONT_SERIF
        p_stat.font.size = Pt(28)
        p_stat.font.bold = True
        p_stat.font.color.rgb = b_col
        p_stat.space_after = Pt(4)
        
        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = FONT_SANS
        p2.font.size = Pt(11.5)
        p2.font.bold = True
        p2.font.color.rgb = C_INK
        p2.space_after = Pt(6)
        
        p3 = tf.add_paragraph()
        p3.text = body
        p3.font.name = FONT_SANS
        p3.font.size = Pt(9)
        p3.font.color.rgb = C_INK_SEC
        
    add_callout(slide, Inches(0.9), Inches(6.15), Inches(11.5), Inches(0.55),
                "Strategic Reality: We do not need to guess if cafes want Alandas. They already buy it. Our mission is to take Sidy out of manual order-taking and build a systematic pipeline to reach 100+ accounts.")
    add_footer(slide, 2)

def build_slide_3(prs):
    slide = add_base_slide(prs)
    add_header(slide, "02 // Operational Diagnosis", "Where the Business Is Currently Experiencing Friction",
               "Alandas operates as two separate silos: an offline B2B channel run manually, and an online store that leaks potential wholesale buyers.")
    
    col_w = Inches(5.61)
    col_h = Inches(4.0)
    top_pos = Inches(2.05)
    
    # Left Card: Silo 1
    add_card(slide, Inches(0.9), top_pos, col_w, col_h, C_CRIMSON_BG, C_CRIMSON)
    tx1 = slide.shapes.add_textbox(Inches(1.15), top_pos + Inches(0.25), col_w - Inches(0.5), col_h - Inches(0.5))
    tf1 = tx1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "SILO 1: OFFLINE B2B WHOLESALE"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = C_CRIMSON
    
    p2 = tf1.add_paragraph()
    p2.text = "High Traction, High Founder Overhead"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_INK
    p2.space_after = Pt(10)
    
    bullets1 = [
        ("Unfiltered Inquiries", "Leads arrive via Instagram DMs and WhatsApp. Sidy manually sifts real buyers from freebie seekers."),
        ("Manual PDF Distribution", "The 24-page catalog is sent manually back-and-forth over email or chat attachments."),
        ("Manual Reorder Drag", "Existing cafes text photos of empty bags. Sidy manually creates draft orders and invoices."),
        ("Founder Time Ceiling", "Sidy's personal hours are trapped in order administration instead of growth.")
    ]
    for b_title, b_desc in bullets1:
        pb = tf1.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = FONT_SANS
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = C_INK_SEC
        pb.space_after = Pt(6)
        
    # Right Card: Silo 2
    add_card(slide, Inches(6.8), top_pos, col_w, col_h, C_CRIMSON_BG, C_CRIMSON)
    tx2 = slide.shapes.add_textbox(Inches(7.05), top_pos + Inches(0.25), col_w - Inches(0.5), col_h - Inches(0.5))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    
    p1 = tf2.paragraphs[0]
    p1.text = "SILO 2: ONLINE STOREFRONT (ALANDAS.DE)"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = C_CRIMSON
    
    p2 = tf2.add_paragraph()
    p2.text = "Hiding Social Proof & Conversion Leaks"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13)
    p2.font.bold = True
    p2.font.color.rgb = C_INK
    p2.space_after = Pt(10)
    
    bullets2 = [
        ("Hiding 80% of Clients", "The website only mentions 3 partners; 10 top venues like Vesuvio and Melt are invisible."),
        ("No Product Page Reviews", "Zero customer star badges or review widgets on individual tea pages."),
        ("Trial Price Contradiction", "Gastro page lists the sample box at €19.00; Contact page lists €9.90 netto."),
        ("Zero Tracking Attribution", "No Google Analytics 4, Tag Manager, or Meta Pixel installed to measure conversions.")
    ]
    for b_title, b_desc in bullets2:
        pb = tf2.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = FONT_SANS
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = C_INK_SEC
        pb.space_after = Pt(6)

    add_callout(slide, Inches(0.9), Inches(6.15), Inches(11.5), Inches(0.55),
                "The Goal: Connect both worlds into a unified commercial engine where the website validates leads, the system qualifies them, and reorders happen automatically.")
    add_footer(slide, 3)

def build_slide_4(prs):
    slide = add_base_slide(prs)
    add_header(slide, "03 // Storefront Triage", "Fixing the 5 Public Signals That Kill Commercial Trust",
               "Before pouring new leads into the funnel, we must repair the five discrepancies discovered during the audit that cause wholesale buyers to hesitate.")
    
    # Table Shape
    rows = 6
    cols = 3
    left = Inches(0.9)
    top = Inches(2.05)
    width = Inches(11.5)
    height = Inches(4.5)
    
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(4.2)
    table.columns[2].width = Inches(4.7)
    
    headers = ["AUDIT DISCREPANCY", "WHAT CAFE BUYERS SEE TODAY", "THE PHASE 1 FIX & COMMERCIAL RESULT"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(242, 239, 232)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_SANS
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_INK
        
    data = [
        ("Sample Box Price Conflict", "Gastro page says €19.00; Contact page says €9.90 netto. Destroys pricing confidence.", "Standardize €9.90 Netto: Credited 100% against first wholesale order. Restores trust & secures trial intent."),
        ("Hidden Partner Proof", "Website only mentions 3 partners; 10 major venues (Vesuvio, Melt, Friedrichs) are omitted.", "Interactive Partner Map: Showcase 'Where to Drink Alandas in Berlin' with venue photos to prove legitimacy."),
        ("Teebar Display Out of Stock", "Marketed as the core B2B counter asset, but product page shows Unavailable (€79.00).", "Enable Pre-Orders: Turn on 'Pre-Order for Your Venue' with a 10-day notice. Stop turning away ready buyers."),
        ("Google Business Profile Disconnect", "Listed under alanda's tea (5.0★) with address hidden, dropping pin in central Germany.", "Set Berlin Service Area: Add Tee-Großhändler category & forward calls to Sidy's active WhatsApp Business line."),
        ("Shipping Threshold Conflict", "Product pages say €59; shipping policy page says €40. Causes checkout abandonment.", "Unify at €49 Threshold: Install interactive cart progress bar to lift retail average order value.")
    ]
    for row_idx, (col1, col2, col3) in enumerate(data):
        cell1 = table.cell(row_idx + 1, 0)
        cell2 = table.cell(row_idx + 1, 1)
        cell3 = table.cell(row_idx + 1, 2)
        
        for c in [cell1, cell2, cell3]:
            c.fill.solid()
            c.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 0 else RGBColor(252, 251, 248)
            
        p1 = cell1.text_frame.paragraphs[0]
        p1.text = col1
        p1.font.name = FONT_SANS
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_INK
        
        p2 = cell2.text_frame.paragraphs[0]
        p2.text = col2
        p2.font.name = FONT_SANS
        p2.font.size = Pt(8.8)
        p2.font.color.rgb = C_INK_SEC
        
        p3 = cell3.text_frame.paragraphs[0]
        p3.text = col3
        p3.font.name = FONT_SANS
        p3.font.size = Pt(8.8)
        p3.font.color.rgb = C_GREEN
        p3.font.bold = True
        
    add_footer(slide, 4)

def build_slide_5(prs):
    slide = add_base_slide(prs)
    add_header(slide, "04 // Lead Validation", "The Automated Lead Qualification Filter",
               "How we protect Sidy's time by systematically filtering out tire-kickers and fast-tracking high-volume hospitality accounts.")
    
    stages = [
        ("STAGE 1 // INTAKE", "Structured Intake", 
         "Replaces open chat with a 60-second digital B2B form capturing:\n• Venue Name & Address\n• German Tax ID (USt-IdNr)\n• Seating Covers (>40)\n• Current Weekly Tea Spend\n• Decision Maker Contact", C_WHITE, C_BORDER),
        ("STAGE 2 // FILTER", "Automated Scoring", 
         "System automatically categorizes:\n• Tier 1 (VIP Cafe): >40 seats -> instant booking link.\n• Tier 2 (Small Venue): Sample pack offer.\n• Disqualified: Home consumer -> redirect to D2C store with 10% coupon.", C_OLIVE_BG, C_OLIVE),
        ("STAGE 3 // COMMIT", "€9.90 Trial Box", 
         "Standardize Experience Box at €9.90 netto.\n\n• Eliminates 100% of freebie hunters.\n• Credited 100% on first order.\n• Includes pot, tray, spoon, 5 teas + QR brewing video.", C_GOLD_BG, C_GOLD),
        ("STAGE 4 // CLOSE", "4-Touch Follow-Up", 
         "Triggered automatically upon parcel delivery:\n• Day 2: WhatsApp unboxing check-in.\n• Day 4: Sensory brew & margin guide.\n• Day 7: Turnkey Starter Crate close.\n• Sidy steps in only when warm.", C_GREEN_BG, C_GREEN)
    ]
    card_w = Inches(2.68)
    card_h = Inches(4.0)
    top_pos = Inches(2.05)
    gap = Inches(0.27)
    
    for i, (k, t, b, bg_col, b_col) in enumerate(stages):
        left_pos = Inches(0.9) + i * (card_w + gap)
        add_card(slide, left_pos, top_pos, card_w, card_h, bg_col, b_col)
        
        tx = slide.shapes.add_textbox(left_pos + Inches(0.18), top_pos + Inches(0.18), card_w - Inches(0.36), card_h - Inches(0.36))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = k
        p1.font.name = FONT_SANS
        p1.font.size = Pt(7.5)
        p1.font.bold = True
        p1.font.color.rgb = b_col
        p1.space_after = Pt(6)
        
        p2 = tf.add_paragraph()
        p2.text = t
        p2.font.name = FONT_SANS
        p2.font.size = Pt(12.5)
        p2.font.bold = True
        p2.font.color.rgb = C_INK
        p2.space_after = Pt(8)
        
        p3 = tf.add_paragraph()
        p3.text = b
        p3.font.name = FONT_SANS
        p3.font.size = Pt(8.8)
        p3.font.color.rgb = C_INK_SEC
        
    add_callout(slide, Inches(0.9), Inches(6.15), Inches(11.5), Inches(0.55),
                "The Filter Outcome: Sidy never spends 30 minutes fielding inquiries from home consumers again. Only qualified hospitality operators with real commercial intent reach his calendar.")
    add_footer(slide, 5)

def build_slide_6(prs):
    slide = add_base_slide(prs)
    add_header(slide, "05 // Lead Generation", "Building the Pipeline: Inbound Social & Outbound Blitz",
               "How we feed qualified leads into the qualification filter consistently using organic channels and targeted regional outreach.")
    
    col_w = Inches(5.61)
    col_h = Inches(4.5)
    top_pos = Inches(2.05)
    
    # Inbound
    add_card(slide, Inches(0.9), top_pos, col_w, col_h, C_GOLD_BG, C_GOLD)
    tx1 = slide.shapes.add_textbox(Inches(1.15), top_pos + Inches(0.25), col_w - Inches(0.5), col_h - Inches(0.5))
    tf1 = tx1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "ENGINE 1 // INBOUND SOCIAL"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = C_GOLD
    
    p2 = tf1.add_paragraph()
    p2.text = "OpenReply Comment-to-DM Engine"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13.5)
    p2.font.bold = True
    p2.font.color.rgb = C_INK
    p2.space_after = Pt(8)
    
    inbound_bullets = [
        ("The Audience Asset", "Alandas already has active followers on Instagram (@alandastea). Right now, engagement produces zero structured leads."),
        ("The Visual Hook", "Sidy posts a 15-second Reel of tea blooming in the borosilicate pot on a bamboo tray."),
        ("The Trigger CTA", "Caption: 'Berlin cafe & restaurant managers: Comment GASTRO for our wholesale catalog & sample kit.'"),
        ("Automated Instant DM", "OpenReply (self-hosted via official Meta Graph API) sends an automated DM within 3 seconds with the private intake form."),
        ("Zero SaaS Cost", "No expensive $150/month ManyChat subscription.")
    ]
    for b_title, b_desc in inbound_bullets:
        pb = tf1.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = FONT_SANS
        pb.font.size = Pt(9.2)
        pb.font.color.rgb = C_INK_SEC
        pb.space_after = Pt(4.5)

    # Outbound
    add_card(slide, Inches(6.8), top_pos, col_w, col_h, C_WHITE, C_BORDER)
    tx2 = slide.shapes.add_textbox(Inches(7.05), top_pos + Inches(0.25), col_w - Inches(0.5), col_h - Inches(0.5))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    
    p1 = tf2.paragraphs[0]
    p1.text = "ENGINE 2 // REGIONAL OUTBOUND"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = C_OLIVE
    
    p2 = tf2.add_paragraph()
    p2.text = "Berlin District-by-District Blitz"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13.5)
    p2.font.bold = True
    p2.font.color.rgb = C_INK
    p2.space_after = Pt(8)
    
    outbound_bullets = [
        ("The Market Universe", "Berlin has over 3,000 licensed food and beverage venues. We target 50 qualified venues per district cluster."),
        ("Charlottenburg / Ku'damm", "Bakeries, patisseries, daytime cafes (Target blends: Earl Grey Blue, Sencha, Paris)."),
        ("Kreuzberg / Neukölln", "High-volume Mediterranean dining & evening lounges (Hürrem Sultan profile; massive black tea demand)."),
        ("Mitte / Friedrichshain", "Specialty brunch spots & boutique hotels (Melt Creperie profile)."),
        ("The Touchpoint", "20-second personalized founder voice note or physical mini-sample drop with QR code.")
    ]
    for b_title, b_desc in outbound_bullets:
        pb = tf2.add_paragraph()
        pb.text = f"• {b_title}: {b_desc}"
        pb.font.name = FONT_SANS
        pb.font.size = Pt(9.2)
        pb.font.color.rgb = C_INK_SEC
        pb.space_after = Pt(4.5)
        
    add_footer(slide, 6)

def build_slide_7(prs):
    slide = add_base_slide(prs)
    add_header(slide, "06 // Offer Architecture", "The High-Conversion Offer: Turnkey Starter Crate (€249 Netto)",
               "Cafes hesitate when forced to piece together individual teapots, trays, and tea bags. We package an all-in-one launch pack that makes buying an immediate decision.")
    
    col_w = Inches(5.61)
    col_h = Inches(4.5)
    top_pos = Inches(2.05)
    
    # Left: Composition
    add_card(slide, Inches(0.9), top_pos, col_w, col_h, C_WHITE, C_BORDER)
    tx1 = slide.shapes.add_textbox(Inches(1.15), top_pos + Inches(0.25), col_w - Inches(0.5), col_h - Inches(0.5))
    tf1 = tx1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "PACKAGE SPECIFICATION"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = C_OLIVE
    
    p2 = tf1.add_paragraph()
    p2.text = "Everything a Cafe Needs in One Box"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13.5)
    p2.font.bold = True
    p2.font.color.rgb = C_INK
    p2.space_after = Pt(10)
    
    specs = [
        ("1x Solid Wood Teebar Display", "Visual countertop sales centerpiece holding 6 aroma-tight canisters (Catalog cost: €49.00)."),
        ("6x Borosilicate Glass Teapots (330ml)", "Built-in lid strainers; zero messy clean-up for waitstaff (Catalog cost: €65.16)."),
        ("6x Sustainable Bamboo Trays", "Dedicated tableside presentation for 1 pot + 1 glass (Catalog cost: €25.20)."),
        ("1x Stainless Dosing Spoon", "Calibrated 1-pot dose; eliminates employee waste (Catalog cost: €2.00)."),
        ("6x Flagship 220g Tea Pouches", "1.32kg total tea stock / ~330 fresh servings (Catalog cost: €64.44).")
    ]
    for s_title, s_desc in specs:
        pb = tf1.add_paragraph()
        pb.text = f"• {s_title}: {s_desc}"
        pb.font.name = FONT_SANS
        pb.font.size = Pt(9.2)
        pb.font.color.rgb = C_INK_SEC
        pb.space_after = Pt(6)

    # Right: Margin Math
    add_card(slide, Inches(6.8), top_pos, col_w, col_h, C_GREEN_BG, C_GREEN)
    tx2 = slide.shapes.add_textbox(Inches(7.05), top_pos + Inches(0.25), col_w - Inches(0.5), col_h - Inches(0.5))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    
    p1 = tf2.paragraphs[0]
    p1.text = "COMMERCIAL UNIT ECONOMICS"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = C_GREEN
    
    p2 = tf2.add_paragraph()
    p2.text = "Day-1 Profit & The Recurring Refill Lock-In"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13.5)
    p2.font.bold = True
    p2.font.color.rgb = C_INK
    p2.space_after = Pt(10)
    
    math_text = (
        "For Alandas:\n"
        "• Total Wholesale Component Cost: €205.80\n"
        "• Starter Crate Package Price: €249.00 Netto\n"
        "• Day-1 Net Profit: €43.20 (zero hardware subsidy or loss).\n\n"
        "For the Cafe Operator:\n"
        "• 330 servings sold at €5.00 menu price = €1,650 in gross sales.\n"
        "• Net return on their €249 investment: €1,401 pure profit.\n\n"
        "The Recurring Cash Flow Lock-In:\n"
        "Once the display is on the counter, the venue reorders 2–4kg in refills monthly, generating €150–€300/month in recurring wholesale orders on autopilot."
    )
    p3 = tf2.add_paragraph()
    p3.text = math_text
    p3.font.name = FONT_SANS
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = C_INK_SEC
    
    add_footer(slide, 7)

def build_slide_8(prs):
    slide = add_base_slide(prs)
    add_header(slide, "07 // Technical Architecture", "The Automation Architecture: Orchestrating the Business",
               "The software layer must connect the business, not complicate it. A clear division between automation, commerce state, and human judgment.")
    
    layers = [
        ("LAYER 1 // TOUCHPOINTS", "Customer Frontends", 
         "Where buyers interact:\n• Instagram: OpenReply comment triggers\n• Storefront: Shopify + B2B intake form\n• WhatsApp: Direct high-touch communication\n• Local Search: Google Business Profile", C_WHITE, C_BORDER),
        ("LAYER 2 // ORCHESTRATION", "Central Automation Core", 
         "Managed via n8n + Webhooks:\n• Routes leads from IG/Form into CRM\n• Evaluates 5-point qualification score\n• Triggers automated delivery follow-up\n• Pings Sidy on WhatsApp for VIP leads", C_OLIVE_BG, C_OLIVE),
        ("LAYER 3 // STATE OF RECORD", "Commerce & Customer Truth", 
         "The databases holding truth:\n• Shopify: Orders, inventory, VAT status\n• CRM: Account stage (Trial, Won, Refill)\n• Human Control: Sidy handles tastings, negotiations, and partner relationships.", C_WHITE, C_BORDER)
    ]
    card_w = Inches(3.64)
    card_h = Inches(4.0)
    top_pos = Inches(2.05)
    gap = Inches(0.29)
    
    for i, (k, t, b, bg_col, b_col) in enumerate(layers):
        left_pos = Inches(0.9) + i * (card_w + gap)
        add_card(slide, left_pos, top_pos, card_w, card_h, bg_col, b_col)
        
        tx = slide.shapes.add_textbox(left_pos + Inches(0.2), top_pos + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = k
        p1.font.name = FONT_SANS
        p1.font.size = Pt(8)
        p1.font.bold = True
        p1.font.color.rgb = b_col
        p1.space_after = Pt(6)
        
        p2 = tf.add_paragraph()
        p2.text = t
        p2.font.name = FONT_SANS
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_INK
        p2.space_after = Pt(8)
        
        p3 = tf.add_paragraph()
        p3.text = b
        p3.font.name = FONT_SANS
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = C_INK_SEC
        
    add_callout(slide, Inches(0.9), Inches(6.15), Inches(11.5), Inches(0.55),
                "The Design Principle: Deterministic rules for pricing, inventory, and qualification. Human judgment for taste, hospitality culture, and long-term contracts.")
    add_footer(slide, 8)

def build_slide_9(prs):
    slide = add_base_slide(prs)
    add_header(slide, "08 // Implementation Timeline", "The 30-Day Phased Implementation Plan",
               "A disciplined rollout where each phase builds the foundation for the next, with zero disruption to daily tea fulfillment.")
    
    rows = 5
    cols = 3
    left = Inches(0.9)
    top = Inches(2.05)
    width = Inches(11.5)
    height = Inches(4.5)
    
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(2.4)
    table.columns[1].width = Inches(5.6)
    table.columns[2].width = Inches(3.5)
    
    headers = ["PHASE & TIMELINE", "CORE ACTIONS & DELIVERABLES", "MEASURABLE BUSINESS OUTCOME"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(242, 239, 232)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_SANS
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = C_INK
        
    phases_data = [
        ("Phase 1: Triage & Proof\nDays 1 – 7", 
         "• Standardize sample box at €9.90 netto credited.\n• Unify shipping at €49 threshold with cart progress bar.\n• Sync Google Business Profile to Berlin & forward phone to WhatsApp.\n• Publish 13 verified partner venues on interactive map on alandas.de.\n• Enable pre-orders on Teebar wooden counter rack.",
         "Stops Inbound Leaks\nImmediate trust boost; stops cart abandonment."),
        ("Phase 2: Intake & Tracking\nWeeks 2 – 3",
         "• Deploy structured B2B Lead Intake Form & scoring filter.\n• Deploy GA4, GTM e-commerce tracking & Meta CAPI.\n• Integrate Klaviyo & launch automated 4-touch sample follow-up.\n• Launch B2C 'World Tour' Sampler Pack (€19.90).",
         "Protects Founder Time\nTire-kickers filtered; full funnel analytics active."),
        ("Phase 3: Social & Video\nWeeks 4 – 5",
         "• Deploy OpenReply on @alandastea (Reel trigger: 'GASTRO').\n• Batch-produce 9:16 vertical brewing Reels using OpenChatCut.\n• Launch Instagram Comment-to-DM B2B sample acquisition flow.",
         "Zero-Cost Inbound Flow\nDirectly monetizes existing Instagram audience."),
        ("Phase 4: Scaled B2B Portal\nWeeks 6 – 8",
         "• Build self-serve Shopify B2B Wholesale Portal with instant VAT check.\n• Display €10.74 tea rates, €10.86 pots, and bulk 1kg catering tiers.\n• Launch Turnkey Hospitality Starter Crate (€249 package).\n• Execute Berlin Outbound Blitz (50 targeted venues/district).",
         "Scales to 100+ Venues\nAutomated reordering; recurring wholesale cash flow.")
    ]
    for row_idx, (col1, col2, col3) in enumerate(phases_data):
        cell1 = table.cell(row_idx + 1, 0)
        cell2 = table.cell(row_idx + 1, 1)
        cell3 = table.cell(row_idx + 1, 2)
        
        for c in [cell1, cell2, cell3]:
            c.fill.solid()
            c.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 0 else RGBColor(252, 251, 248)
            
        p1 = cell1.text_frame.paragraphs[0]
        p1.text = col1
        p1.font.name = FONT_SANS
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_GOLD
        
        p2 = cell2.text_frame.paragraphs[0]
        p2.text = col2
        p2.font.name = FONT_SANS
        p2.font.size = Pt(8.8)
        p2.font.color.rgb = C_INK_SEC
        
        p3 = cell3.text_frame.paragraphs[0]
        p3.text = col3
        p3.font.name = FONT_SANS
        p3.font.size = Pt(8.8)
        p3.font.color.rgb = C_GREEN
        p3.font.bold = True
        
    add_footer(slide, 9)

def build_slide_10(prs):
    slide = add_base_slide(prs)
    add_header(slide, "09 // Measurement", "The System Needs a Scoreboard",
               "We manage what we measure. The 6 key operational metrics that determine if the commercial engine is succeeding.")
    
    metrics = [
        ("METRIC 1", "Inquiry Response Time", "Target: < 5 minutes via OpenReply automated DM vs. 24–48 hours manual WhatsApp response."),
        ("METRIC 2", "Lead Qualification Rate", "Target: 100% of non-commercial freebie seekers filtered out before touching Sidy's calendar."),
        ("METRIC 3", "Trial Box Conversion", "Target: > 40% of €9.90 sample boxes converting into first wholesale orders via 4-touch cadence."),
        ("METRIC 4", "First-Order Starter Value", "Target: €249 Starter Crate AOV rather than small piecemeal orders, ensuring Day-1 hardware profit."),
        ("METRIC 5", "30-Day Reorder Rate", "Target: > 75% recurring monthly replenishment driven by automated restock reminders."),
        ("METRIC 6", "Founder Manual Hours", "Target: Reduce Sidy's manual order-entry time by 12+ hours/week through self-serve portal.")
    ]
    card_w = Inches(3.64)
    card_h = Inches(1.95)
    gap_x = Inches(0.29)
    gap_y = Inches(0.25)
    
    for i, (m_tag, m_title, m_desc) in enumerate(metrics):
        col = i % 3
        row = i // 3
        left_pos = Inches(0.9) + col * (card_w + gap_x)
        top_pos = Inches(2.15) + row * (card_h + gap_y)
        
        bg_col = C_OLIVE_BG if i == 5 else C_WHITE
        b_col = C_OLIVE if i == 5 else C_BORDER
        add_card(slide, left_pos, top_pos, card_w, card_h, bg_col, b_col)
        
        tx = slide.shapes.add_textbox(left_pos + Inches(0.18), top_pos + Inches(0.15), card_w - Inches(0.36), card_h - Inches(0.3))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = m_tag
        p1.font.name = FONT_SANS
        p1.font.size = Pt(7.5)
        p1.font.bold = True
        p1.font.color.rgb = C_OLIVE
        p1.space_after = Pt(3)
        
        p2 = tf.add_paragraph()
        p2.text = m_title
        p2.font.name = FONT_SANS
        p2.font.size = Pt(11.5)
        p2.font.bold = True
        p2.font.color.rgb = C_INK
        p2.space_after = Pt(4)
        
        p3 = tf.add_paragraph()
        p3.text = m_desc
        p3.font.name = FONT_SANS
        p3.font.size = Pt(8.8)
        p3.font.color.rgb = C_INK_SEC
        
    add_footer(slide, 10)

def build_slide_11(prs):
    slide = add_base_slide(prs)
    add_header(slide, "10 // Immediate Kickoff", "How We Start: The Phase 1 Quick Wins This Week",
               "We begin with immediate, high-impact fixes that remove friction, establish proof, and prepare the foundation.")
    
    col_w = Inches(5.61)
    col_h = Inches(4.5)
    top_pos = Inches(2.05)
    
    # Left
    add_card(slide, Inches(0.9), top_pos, col_w, col_h, C_GOLD_BG, C_GOLD)
    tx1 = slide.shapes.add_textbox(Inches(1.15), top_pos + Inches(0.25), col_w - Inches(0.5), col_h - Inches(0.5))
    tf1 = tx1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "THE PARTNERSHIP ROLE"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = C_GOLD
    
    p2 = tf1.add_paragraph()
    p2.text = "What I Build for Alandas"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13.5)
    p2.font.bold = True
    p2.font.color.rgb = C_INK
    p2.space_after = Pt(8)
    
    p_desc = tf1.add_paragraph()
    p_desc.text = "I do not operate as a typical freelance web designer who just changes fonts or installs bloated monthly plugins."
    p_desc.font.name = FONT_SANS
    p_desc.font.size = Pt(9.5)
    p_desc.font.color.rgb = C_INK_SEC
    p_desc.space_after = Pt(8)
    
    roles = [
        ("Technical Systems Architect", "Building custom API connections, automated lead scoring, and clean server-side integrations."),
        ("Revenue Operations (RevOps)", "Fixing checkout leaks, harmonizing pricing, and setting up true attribution tracking."),
        ("Founder Liberation", "Decoupling your personal hours from order fulfillment so you can focus on partnerships and brand vision.")
    ]
    for r_title, r_desc in roles:
        pb = tf1.add_paragraph()
        pb.text = f"• {r_title}: {r_desc}"
        pb.font.name = FONT_SANS
        pb.font.size = Pt(9.2)
        pb.font.color.rgb = C_INK_SEC
        pb.space_after = Pt(6)

    # Right
    add_card(slide, Inches(6.8), top_pos, col_w, col_h, C_GREEN_BG, C_GREEN)
    tx2 = slide.shapes.add_textbox(Inches(7.05), top_pos + Inches(0.25), col_w - Inches(0.5), col_h - Inches(0.5))
    tf2 = tx2.text_frame
    tf2.word_wrap = True
    
    p1 = tf2.paragraphs[0]
    p1.text = "ACTION ITEMS FOR TODAY"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = C_GREEN
    
    p2 = tf2.add_paragraph()
    p2.text = "Phase 1 Kickoff Checklist"
    p2.font.name = FONT_SANS
    p2.font.size = Pt(13.5)
    p2.font.bold = True
    p2.font.color.rgb = C_INK
    p2.space_after = Pt(10)
    
    checklist = [
        ("Step 1: Grant Shopify Access", "Grant collaborator access so I can standardize the €9.90 sample box and unify shipping at €49."),
        ("Step 2: Sync Google Profile", "Forward Google Business phone number to your active WhatsApp Business line and add Berlin service area."),
        ("Step 3: Publish Partner Map", "Build and publish the interactive 13-venue partner map on alandas.de."),
        ("Step 4: Deploy OpenReply", "Deploy OpenReply on our server to prep your first Instagram Comment-to-DM Reel test.")
    ]
    for c_title, c_desc in checklist:
        pb = tf2.add_paragraph()
        pb.text = f"• {c_title}: {c_desc}"
        pb.font.name = FONT_SANS
        pb.font.size = Pt(9.2)
        pb.font.color.rgb = C_INK_SEC
        pb.space_after = Pt(6)
        
    add_footer(slide, 11)

def build_slide_12(prs):
    slide = add_base_slide(prs)
    
    # Centered Header
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(1.2), Inches(11.5), Inches(2.2))
    tf = tx.text_frame
    tf.word_wrap = True
    
    pk = tf.paragraphs[0]
    pk.text = "11 // STRATEGIC ALIGNMENT"
    pk.alignment = PP_ALIGN.CENTER
    pk.font.name = FONT_SANS
    pk.font.size = Pt(9.5)
    pk.font.bold = True
    pk.font.color.rgb = C_OLIVE
    pk.space_after = Pt(12)
    
    pt = tf.add_paragraph()
    pt.text = "Let's Build Your Commercial Operating System"
    pt.alignment = PP_ALIGN.CENTER
    pt.font.name = FONT_SERIF
    pt.font.size = Pt(36)
    pt.font.bold = False
    pt.font.color.rgb = C_INK
    pt.space_after = Pt(12)
    
    pl = tf.add_paragraph()
    pl.text = "\"You've already built the brand, the cultural blends, and proven traction across 13 venues. Let's install the system that scales it.\""
    pl.alignment = PP_ALIGN.CENTER
    pl.font.name = FONT_SANS
    pl.font.size = Pt(12)
    pl.font.italic = True
    pl.font.color.rgb = C_MUTED
    
    # Centered Discussion Card
    c_w = Inches(9.2)
    c_h = Inches(2.4)
    c_left = (Inches(13.333) - c_w) / 2
    c_top = Inches(3.8)
    
    add_card(slide, c_left, c_top, c_w, c_h, C_WHITE, C_OLIVE)
    txc = slide.shapes.add_textbox(c_left + Inches(0.4), c_top + Inches(0.3), c_w - Inches(0.8), c_h - Inches(0.6))
    tfc = txc.text_frame
    tfc.word_wrap = True
    
    p1 = tfc.paragraphs[0]
    p1.text = "Key Discussion Questions for Today:"
    p1.font.name = FONT_SANS
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = C_OLIVE
    p1.space_after = Pt(10)
    
    questions = (
        "1. Which of your 13 partner venues represents your ideal customer profile (dining, brunch, or lounge)?\n"
        "2. How much time are you currently spending manually entering WhatsApp reorders and invoices?\n"
        "3. Are you ready to grant Shopify collaborator access so we can launch Phase 1 this week?"
    )
    p2 = tfc.add_paragraph()
    p2.text = questions
    p2.font.name = FONT_SANS
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_INK_SEC
    
    add_footer(slide, 12)

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    prs = create_deck()
    print("Building Slide 1...")
    build_slide_1(prs)
    print("Building Slide 2...")
    build_slide_2(prs)
    print("Building Slide 3...")
    build_slide_3(prs)
    print("Building Slide 4...")
    build_slide_4(prs)
    print("Building Slide 5...")
    build_slide_5(prs)
    print("Building Slide 6...")
    build_slide_6(prs)
    print("Building Slide 7...")
    build_slide_7(prs)
    print("Building Slide 8...")
    build_slide_8(prs)
    print("Building Slide 9...")
    build_slide_9(prs)
    print("Building Slide 10...")
    build_slide_10(prs)
    print("Building Slide 11...")
    build_slide_11(prs)
    print("Building Slide 12...")
    build_slide_12(prs)
    
    prs.save(OUTPUT_PATH)
    print(f"\n[SUCCESS] Generated Master PowerPoint Deck: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
