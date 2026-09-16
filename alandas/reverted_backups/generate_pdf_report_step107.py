import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Workspace Directories
BASE_DIR = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas"
SCRATCH_ROOT = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch"
ARTIFACT_DIR_CURRENT = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\brain\445482c0-bd2f-4c3e-a494-05a43b97af77"
ARTIFACT_DIR_PREV = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\brain\2e92c3a8-5a9f-4e4e-9c9b-467ab927b185"

# Output PDF destinations
PDF_OUT_MAIN = os.path.join(BASE_DIR, "Alandas_Site_Audit_Report.pdf")
PDF_OUT_DOCS = os.path.join(BASE_DIR, "docs", "Alandas_Site_Audit_Report.pdf")
PDF_OUT_SCRATCH = os.path.join(SCRATCH_ROOT, "Alandas_Site_Audit_Report.pdf")
PDF_OUT_ARTIFACT = os.path.join(ARTIFACT_DIR_CURRENT, "Alandas_Site_Audit_Report.pdf")
PDF_OUT_ARTIFACT_PREV = os.path.join(ARTIFACT_DIR_PREV, "Alandas_Site_Audit_Report.pdf")

# Image assets with fallbacks
def get_asset_path(filename):
    candidates = [
        os.path.join(BASE_DIR, "assets", filename),
        os.path.join(BASE_DIR, filename),
        os.path.join(SCRATCH_ROOT, filename)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

LOGO_PATH = get_asset_path("logo.png")
HERO_PATH = get_asset_path("hero_bombay.png")

PAGE_WIDTH, PAGE_HEIGHT = A4

# =============================================================================
# ENHANCED NUMBERED CANVAS (Luxury Running Header & Footer)
# =============================================================================
class LuxuryNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # -------------------------------------------------------------
        # COVER PAGE (Page 1)
        # -------------------------------------------------------------
        if self._pageNumber == 1:
            # Top decorative brand bar
            self.setFillColor(colors.HexColor("#0F172A")) # Midnight Slate
            self.rect(0, PAGE_HEIGHT - 8, PAGE_WIDTH, 8, stroke=0, fill=1)
            self.setFillColor(colors.HexColor("#C58B2B")) # Alandas Gold stripe
            self.rect(0, PAGE_HEIGHT - 11, PAGE_WIDTH, 3, stroke=0, fill=1)
            
            # Subtle bottom confidentiality footer
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(40, 24, "CONFIDENTIAL & PROPRIETARY — PREPARED FOR CLIENT STRATEGIC ENGAGEMENT")
            self.setFont("Helvetica", 7.5)
            self.drawRightString(PAGE_WIDTH - 40, 24, "SEPTEMBER 2026 | VERSION 2.1")
            self.restoreState()
            return

        # -------------------------------------------------------------
        # INNER PAGES (Pages 2 to 8)
        # -------------------------------------------------------------
        # Running Top Header
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#C58B2B"))
        self.drawString(40, PAGE_HEIGHT - 26, "ALANDAS TEA BERLIN")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(135, PAGE_HEIGHT - 26, "|   COMMERCIAL & TECHNICAL SITE AUDIT")
        
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#94A3B8"))
        self.drawRightString(PAGE_WIDTH - 40, PAGE_HEIGHT - 26, "PRE-ENGAGEMENT CLIENT DOSSIER")
        
        # Dual-tone hairline divider
        self.setStrokeColor(colors.HexColor("#C58B2B"))
        self.setLineWidth(1)
        self.line(40, PAGE_HEIGHT - 31, 130, PAGE_HEIGHT - 31)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(130, PAGE_HEIGHT - 31, PAGE_WIDTH - 40, PAGE_HEIGHT - 31)

        # Running Bottom Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 32, PAGE_WIDTH - 40, 32)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 21, "STRICTLY CONFIDENTIAL — ALANDAS (SIDY SOW) | PREPARED BY CYRIL UZOCHUKWU")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#0F172A"))
        self.drawRightString(PAGE_WIDTH - 40, 21, page_str)
        
        self.restoreState()

# =============================================================================
# HELPER CARD FLOWABLE CREATOR
# =============================================================================
def make_card(content_p, bg_color="#FAF8F5", border_color="#E2E8F0", left_border_color=None, padding=8, width=PAGE_WIDTH - 80):
    t = Table([[content_p]], colWidths=[width])
    t_style = [
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor(border_color)),
        ('LEFTPADDING', (0,0), (-1,-1), padding + (3 if left_border_color else 0)),
        ('RIGHTPADDING', (0,0), (-1,-1), padding),
        ('TOPPADDING', (0,0), (-1,-1), padding),
        ('BOTTOMPADDING', (0,0), (-1,-1), padding),
    ]
    if left_border_color:
        t_style.append(('LINEBEFORE', (0,0), (0,-1), 3.5, colors.HexColor(left_border_color)))
    t.setStyle(TableStyle(t_style))
    return t

# =============================================================================
# MAIN PDF BUILDER FUNCTION
# =============================================================================
def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUT_MAIN,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    # -------------------------------------------------------------
    # LUXURY BRAND PALETTE (Alandas Brand Harmony)
    # -------------------------------------------------------------
    C_MIDNIGHT = colors.HexColor("#0F172A")  # Deep Obsidian/Slate
    C_SLATE    = colors.HexColor("#1E293B")  # Medium Dark Slate
    C_GOLD     = colors.HexColor("#C58B2B")  # Alandas Amber Gold
    C_FOREST   = colors.HexColor("#064E3B")  # Botanical Forest Green
    C_CRIMSON  = colors.HexColor("#991B1B")  # Crimson Alert
    C_MUTED    = colors.HexColor("#64748B")  # Muted Slate
    C_LIGHT_BG = colors.HexColor("#FAF8F5")  # Warm Tea Cream Paper
    C_WHITE    = colors.white
    C_BORDER   = colors.HexColor("#E2E8F0")  # Clean hairline border
    C_AMBER_BG = colors.HexColor("#FEF9EE")  # Subtle Gold Callout Fill

    # -------------------------------------------------------------
    # TYPOGRAPHY STYLES
    # -------------------------------------------------------------
    kicker_style = ParagraphStyle(
        'Kicker', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=10,
        textColor=C_GOLD, spaceAfter=2
    )

    h1_style = ParagraphStyle(
        'Header1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13.5, leading=17,
        textColor=C_MIDNIGHT, spaceBefore=0, spaceAfter=4, keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Header2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.8, leading=13,
        textColor=C_SLATE, spaceBefore=6, spaceAfter=3, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextDark', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.2, leading=11.6,
        textColor=C_SLATE
    )

    callout_style = ParagraphStyle(
        'CalloutText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.9, leading=11.2,
        textColor=C_MIDNIGHT
    )

    table_cell = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=10.2,
        textColor=C_MIDNIGHT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold', parent=table_cell,
        fontName='Helvetica-Bold'
    )

    table_header = ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.8, leading=10.5,
        textColor=C_WHITE
    )

    badge_pill = ParagraphStyle(
        'BadgePill', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=9,
        textColor=C_GOLD
    )

    cover_title = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=21.5, leading=26,
        textColor=C_MIDNIGHT
    )

    cover_sub = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10.5, leading=14.5,
        textColor=C_GOLD
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 4))
    
    # Header Branding Row: Logo + Status Badge
    logo_flowable = Paragraph("<b>ALANDAS TEA BERLIN</b>", h1_style)
    if LOGO_PATH and os.path.exists(LOGO_PATH):
        logo_flowable = Image(LOGO_PATH, width=1.7*inch, height=0.55*inch)
        logo_flowable.hAlign = 'LEFT'

    badge_cell = Table(
        [[Paragraph("STRATEGIC PRE-ENGAGEMENT AUDIT // REVISED V2.1", badge_pill)]],
        colWidths=[240], rowHeights=[20]
    )
    badge_cell.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF9EE")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E9D4A5")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    header_table = Table([[logo_flowable, badge_cell]], colWidths=[275, 240])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # Main Title Block
    story.append(Paragraph("Commercial &amp; Technical Site Audit: Alandas.de", cover_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Storefront Teardown, 26-SKU Catalog Translation, Google Profile Audit &amp; Omnichannel Revenue Blueprint", cover_sub))
    story.append(Spacer(1, 10))

    # Hero Visual Banner
    if HERO_PATH and os.path.exists(HERO_PATH):
        hero_img = Image(HERO_PATH, width=PAGE_WIDTH - 80, height=1.75*inch)
        hero_img.hAlign = 'CENTER'
        story.append(hero_img)
        story.append(Spacer(1, 10))

    # Executive Metadata Grid (Modern 4-Block Card)
    meta_data = [
        [Paragraph("Target Entity:", table_cell_bold), Paragraph("Alandas (Alandas Tea Berlin) | https://alandas.de", table_cell),
         Paragraph("Audit Revision:", table_cell_bold), Paragraph("September 2026 (Updated with Live GBP Findings)", table_cell)],
        [Paragraph("Founder / Lead:", table_cell_bold), Paragraph("Sidy Sow (Lise-Meitner-Str. 39, 10589 Berlin)", table_cell),
         Paragraph("Audit Scope:", table_cell_bold), Paragraph("Storefront, Catalog, Google Maps, Tech &amp; Sales Funnel", table_cell)],
        [Paragraph("Commerce Engine:", table_cell_bold), Paragraph("Shopify (biwzp1-gk.myshopify.com) | Dawn 15.4.1", table_cell),
         Paragraph("Lead Strategist:", table_cell_bold), Paragraph("Cyril Uzochukwu (Strictly Confidential)", table_cell)],
        [Paragraph("Google Profile:", table_cell_bold), Paragraph("<font color='#C58B2B'><b>5.0 ★ (2 Reviews)</b></font> under 'alanda's tea'", table_cell),
         Paragraph("Primary Channels:", table_cell_bold), Paragraph("D2C Online Store + B2B HoReCa Gastronomy", table_cell)],
    ]
    meta_table = Table(meta_data, colWidths=[80, 185, 80, 170])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('LINEBELOW', (0,0), (-1,0), 1.5, C_GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 9))

    # Executive Takeaway Callout Card
    exec_summary_p = Paragraph(
        "<b>Executive Context &amp; Core Diagnosis:</b><br/>"
        "Alandas is a standout brand with <b>world-class cultural storytelling</b> (destination blends inspired by Istanbul, Bombay, "
        "Marrakech, Paris, Berlin) and proven 90%+ gross margin hospitality unit economics (~€0.25/pot cost vs. €5.50 menu price). "
        "However, the commercial engine is severely bottlenecked: <b>zero analytics (no GA4 or Meta Pixel)</b>, conflicting shipping thresholds, "
        "sample box pricing contradictions (€9.90 vs €19), out-of-stock flagship counter displays, and a Google Business Profile that is "
        "verified (5.0★, 2 reviews) but misconfigured as an e-commerce service with a hidden address—dropping the pin in central Germany instead "
        "of Berlin. Furthermore, while the homepage has 3 quotes, product pages lack verified reviews. "
        "Resolving these gaps transforms Alandas into a high-converting D2C and B2B revenue powerhouse.",
        callout_style
    )
    story.append(make_card(exec_summary_p, bg_color="#FEF9EE", border_color="#E9D4A5", left_border_color="#C58B2B", padding=8))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: BRAND IDENTITY & DUAL REVENUE MODEL
    # =========================================================================
    story.append(Paragraph("AUDIT CHAPTER 01 // BRAND POSITIONING", kicker_style))
    story.append(Paragraph("1. Brand Identity &amp; Dual Revenue Model Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "<b>Brand Heritage &amp; Positioning:</b> Operating under the slogan <i>'Alandas ist anders'</i> (Alandas is different), "
        "the company was founded in Berlin by a new generation with multicultural roots. Rather than marketing commodity teas, "
        "Alandas curates signature blends named after world cultural capitals (Istanbul, Marrakech, Bombay, Paris, Berlin, Damascus, "
        "Manila, California). Hand-crafted in small batches without artificial additives, the brand positions tea as a sensory ritual "
        "that connects people, places, and memories.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Commercial Architecture: Retail (B2C) vs Hospitality (B2B)", h2_style))

    biz_model_data = [
        [Paragraph("Commercial Dimension", table_header), Paragraph("B2C Consumer Division (Retail)", table_header), Paragraph("B2B Hospitality Division (Gastro / HoReCa)", table_header)],
        [
            Paragraph("<b>Target Audience</b>", table_cell_bold),
            Paragraph("Urban tea lovers, aesthetic wellness shoppers, gift buyers seeking sensory destination tea.", table_cell),
            Paragraph("Owner-operated specialty cafes, third-wave coffee bars, brunch bistros, boutique hotels.", table_cell)
        ],
        [
            Paragraph("<b>Value Proposition</b>", table_cell_bold),
            Paragraph("Sensory 'world travel in a cup', aesthetic resealable 220g Doypacks, 100% natural botanicals.", table_cell),
            Paragraph("Turnkey Tea Bar serving concept: Borosilicate pot with lid-filter + bamboo tray + precise dosing spoon.", table_cell)
        ],
        [
            Paragraph("<b>Unit Economics</b>", table_cell_bold),
            Paragraph("€14.69 per 220g bag (€6.68 / 100g). Free shipping threshold €40 / €59 discrepancy.", table_cell),
            Paragraph("Cost per pot: ~€0.25 | Menu price: €4.50–€5.90 | Gross profit: €4.25–€5.65 (<b>90%+ gross margin</b>).", table_cell)
        ],
        [
            Paragraph("<b>Sales Motion</b>", table_cell_bold),
            Paragraph("Direct storefront checkout via Shop Pay, Apple Pay, PayPal, Klarna.", table_cell),
            Paragraph("Entry via 'Tea Experience Box' (€19 vs €9.90), direct WhatsApp line, offline catalog request.", table_cell)
        ],
        [
            Paragraph("<b>Current Social Proof</b>", table_cell_bold),
            Paragraph("3 static homepage quotes (Jasmin B., Marah A., Allen W.) but <b>0 reviews on product pages</b>.", table_cell),
            Paragraph("2x 5.0★ Google reviews under 'alanda's tea' + 3 Berlin HoReCa quotes (*Cafe Lafemme*, *Meyman*).", table_cell)
        ]
    ]

    biz_table = Table(biz_model_data, colWidths=[110, 202, 203])
    biz_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_MIDNIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 5.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(biz_table)
    story.append(Spacer(1, 9))

    # Entity & Verified Google Profile Card
    entity_text = (
        "<b>Corporate Registration &amp; Google Profile Details:</b><br/>"
        "• <b>Legal Structure:</b> Sole Proprietorship (<i>Einzelunternehmen</i> / Registered Gewerbe in Berlin-Charlottenburg).<br/>"
        "• <b>Proprietor:</b> Sidy Sow | Address: Lise-Meitner-Str. 39, 10589 Berlin, Germany (Gewerbehof near Jungfernheide).<br/>"
        "• <b>VAT Identification Number:</b> DE312066015 (USt-IdNr gemäß §27a UStG) | Store Backend: biwzp1-gk.myshopify.com.<br/>"
        "• <b>Google Business Profile:</b> Registered as <b>'alanda's tea'</b> (5.0 ★ based on 2 reviews). Listed phone: +49 1515 6856439.<br/>"
        "• <b>Website Contact:</b> Fast WhatsApp Chat widget &amp; Contact page list: <b>+49 15678 689200</b> | Email: info@alandas.de."
    )
    story.append(make_card(Paragraph(entity_text, callout_style), bg_color="#FAF8F5", border_color="#E2E8F0", left_border_color="#0F172A", padding=8))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: CATALOG MATRIX - PART 1 (FLAGSHIP CULTURAL BLENDS)
    # =========================================================================
    story.append(Paragraph("AUDIT CHAPTER 02 // PRODUCT CATALOG", kicker_style))
    story.append(Paragraph("2. Complete Catalog Scoping &amp; Translation Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Alandas maintains 26 active SKUs. Below is the flagship line of 13 Cultural Destination Blends, completely translated into "
        "English with botanical ingredients, weight, pricing, and live inventory status.",
        body_style
    ))
    story.append(Spacer(1, 5))
    story.append(Paragraph("A. Cultural Destination Blends (Flagship 220g Doypacks)", h2_style))

    cat_a_data = [
        [Paragraph("SKU", table_header), Paragraph("Blend Name", table_header), Paragraph("Key Ingredients &amp; Profile (Translated to English)", table_header), Paragraph("Weight", table_header), Paragraph("Price", table_header), Paragraph("Status", table_header)],
        [Paragraph("50115", table_cell), Paragraph("<b>ISTANBUL</b>", table_cell_bold), Paragraph("Black tea, cinnamon, dried apple, rose petals. Spicy-floral Turkish Chai.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("60117", table_cell), Paragraph("<b>BOMBAY</b>", table_cell_bold), Paragraph("Black tea, cardamom, cloves, cinnamon. Authentic Indian bazaar Chai Latte.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("40111", table_cell), Paragraph("<b>MARRAKECH</b>", table_cell_bold), Paragraph("Green tea, peppermint, lemon peel, natural citrus. Refreshing Moroccan mint.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("10113", table_cell), Paragraph("<b>PARIS</b>", table_cell_bold), Paragraph("Strawberry, apple, hibiscus, rosehip, cornflowers, cream note. French patisserie fruit.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("50110", table_cell), Paragraph("<b>BERLIN</b>", table_cell_bold), Paragraph("Rooibos, hemp, carrots, green mate, papaya. Tangy, earthy urban energy.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("50120", table_cell), Paragraph("<b>DAMASKUS</b>", table_cell_bold), Paragraph("Japanese Sencha green tea + black tea + rose, sunflower &amp; jasmine blossoms.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("50117", table_cell), Paragraph("<b>LONDON</b>", table_cell_bold), Paragraph("Black tea, rooibos, caramel pieces, vanilla, jasmine, mallow flowers.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("50232", table_cell), Paragraph("<b>CALIFORNIA</b>", table_cell_bold), Paragraph("Rooibos, orange peel, orange blossoms. Sunny, fruity, naturally caffeine-free.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("50116", table_cell), Paragraph("<b>GRANADA</b>", table_cell_bold), Paragraph("Green tea, mint, orange peel, orange blossom, hibiscus. Tart Andalusian garden.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("40144", table_cell), Paragraph("<b>MANILA</b>", table_cell_bold), Paragraph("Green tea, pineapple, papaya, apple, orange, marigold, rose petals. Tropical fruit.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("30125", table_cell), Paragraph("<b>SCHWARZWALD</b>", table_cell_bold), Paragraph("Lingonberries, blackberries, raisins, hibiscus. Rich German Black Forest berry.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("60113", table_cell), Paragraph("<b>HIMALAYA</b>", table_cell_bold), Paragraph("Ayurvedic black tea, ginger, cardamom, cinnamon, clove, black pepper, citrus.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("233038", table_cell), Paragraph("<b>BUDAPEST</b>", table_cell_bold), Paragraph("Lemongrass, apple, ginger, stevia leaves, sunflower blossoms. Sugar-free sweet.", table_cell), Paragraph("150g", table_cell), Paragraph("€10.20", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)]
    ]

    cat_a_table = Table(cat_a_data, colWidths=[40, 78, 255, 42, 45, 55])
    cat_a_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_MIDNIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(cat_a_table)
    story.append(Spacer(1, 9))

    cat_a_note = (
        "<b>Merchandising Opportunity:</b> All flagship blends (except Budapest at 150g) are standardized at 220g for €14.69 "
        "(€6.68/100g). While the price per gram is very competitive, forcing first-time retail buyers to purchase 220g creates a high "
        "trial barrier. Introducing a <b>'Cultural World Tour' Sampler Pack (5x 30g tins for €19.90)</b> solves this barrier immediately."
    )
    story.append(make_card(Paragraph(cat_a_note, callout_style), bg_color="#FEF9EE", border_color="#E9D4A5", left_border_color="#C58B2B", padding=7))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: CATALOG MATRIX - PART 2 (CLASSICS & HARDWARE)
    # =========================================================================
    story.append(Paragraph("AUDIT CHAPTER 02 // PRODUCT CATALOG (CONT.)", kicker_style))
    story.append(Paragraph("2. Complete Catalog Scoping (Classics &amp; Hardware)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("B. Pure Classics &amp; Single-Origins (6 SKUs)", h2_style))
    cat_b_data = [
        [Paragraph("SKU", table_header), Paragraph("Product Name", table_header), Paragraph("Profile, Origin &amp; Quality Notes", table_header), Paragraph("Weight", table_header), Paragraph("Price", table_header), Paragraph("Status", table_header)],
        [Paragraph("20118", table_cell), Paragraph("<b>EARL GREY BLUE</b>", table_cell_bold), Paragraph("Single-estate Rukeri black tea from Rwanda, bergamot oil, cornflower petals.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("14183", table_cell), Paragraph("<b>GRÜNTEE SENCHA</b>", table_cell_bold), Paragraph("Pure Japanese Sencha green tea. Grassy, marine, refreshing umami profile.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("13860", table_cell), Paragraph("<b>SCHWARZTEE</b>", table_cell_bold), Paragraph("Classic Ceylon &amp; Darjeeling blend (English Breakfast style). Robust &amp; malty.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("50118", table_cell), Paragraph("<b>OOLONG SE CHUNG</b>", table_cell_bold), Paragraph("Semi-fermented blue tea from Fujian Province, China. Complex, nutty-fruity.", table_cell), Paragraph("220g", table_cell), Paragraph("€14.69", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("26118", table_cell), Paragraph("<b>KAMILLE</b>", table_cell_bold), Paragraph("100% whole, uncrushed chamomile blossoms. Gentle, relaxing, soothing.", table_cell), Paragraph("80g", table_cell), Paragraph("€5.49", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("26113", table_cell), Paragraph("<b>PFEFFERMINZE</b>", table_cell_bold), Paragraph("Coarse-cut pure peppermint leaves. High natural menthol clarity.", table_cell), Paragraph("120g", table_cell), Paragraph("€8.49", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
    ]
    cat_b_table = Table(cat_b_data, colWidths=[40, 95, 235, 42, 45, 58])
    cat_b_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_MIDNIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(cat_b_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("C. Hardware, Teaware &amp; Gastro Equipment (7 SKUs)", h2_style))
    cat_c_data = [
        [Paragraph("SKU", table_header), Paragraph("Hardware Item", table_header), Paragraph("Function, Materials &amp; Dimensions", table_header), Paragraph("Price", table_header), Paragraph("Availability", table_header)],
        [Paragraph("10030", table_cell), Paragraph("<b>Glass Teapot 350ml</b>", table_cell_bold), Paragraph("Handcrafted Borosilicate glass with built-in stainless lid-filter (-40°C to +150°C).", table_cell), Paragraph("€24.95", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("10050", table_cell), Paragraph("<b>Bamboo Serving Tray</b>", table_cell_bold), Paragraph("Sustainable polished bamboo wood, sized for 1 teapot + 1 glass (22.5 × 14 × 2.5 cm).", table_cell), Paragraph("€9.89", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("10040", table_cell), Paragraph("<b>Airtight Storage Jar</b>", table_cell_bold), Paragraph("800ml Borosilicate glass cylinder with aroma-tight bamboo lid (15 × 10 cm).", table_cell), Paragraph("€8.90", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("10070", table_cell), Paragraph("<b>Stainless Dosing Spoon</b>", table_cell_bold), Paragraph("Ergonomic stainless steel spoon measured for 1 standard teapot (14 × 3.5 cm).", table_cell), Paragraph("€3.90", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("—", table_cell), Paragraph("<b>Heart Tea Strainer</b>", table_cell_bold), Paragraph("Snap-lock stainless heart infuser spoon for single-cup brewing.", table_cell), Paragraph("€5.95", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
        [Paragraph("—", table_cell), Paragraph("<b>Teebar Wooden Shelf</b>", table_cell_bold), Paragraph("Solid wood counter rack + 6 or 8 glass jars with bamboo lids. <b>Flagship B2B Display.</b>", table_cell), Paragraph("€79.00", table_cell), Paragraph("<font color='#991B1B'><b>OUT OF STOCK</b></font>", table_cell)],
        [Paragraph("—", table_cell), Paragraph("<b>Tea Experience Box</b>", table_cell_bold), Paragraph("Gastro starter pack: Teapot, bamboo tray, spoon, 5–6 teas. <i>Price conflict noted below.</i>", table_cell), Paragraph("€19.00*", table_cell), Paragraph("<font color='#064E3B'><b>In Stock</b></font>", table_cell)],
    ]
    cat_c_table = Table(cat_c_data, colWidths=[40, 115, 215, 50, 95])
    cat_c_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_MIDNIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 3.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(cat_c_table)
    story.append(Spacer(1, 9))

    cat_bc_note = (
        "<b>Flagship Hardware Bottleneck:</b> The borosilicate teapot and bamboo tray form the core operational serving ritual for cafes. "
        "However, the <b>Teebar Wooden Shelf (€79.00)</b> is marked out of stock. Because this counter rack is the primary visual sales "
        "centerpiece for hospitality, cafes cannot launch the complete setup. Setting this to <i>'Pre-Order for Your Venue'</i> is an immediate fix."
    )
    story.append(make_card(Paragraph(cat_bc_note, callout_style), bg_color="#FEF2F2", border_color="#FECACA", left_border_color="#991B1B", padding=7))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TECHNICAL STACK & BLIND SPOTS
    # =========================================================================
    story.append(Paragraph("AUDIT CHAPTER 03 // TECHNICAL INFRASTRUCTURE", kicker_style))
    story.append(Paragraph("3. Technical Stack Audit, Tracking &amp; Review Infrastructure", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceBefore=2, spaceAfter=8))

    tech_overview_text = (
        "<b>Architecture &amp; Theme:</b> Built on Shopify's native infrastructure (`biwzp1-gk.myshopify.com`) using customized "
        "<b>Dawn 15.4.1</b>. Typography pairs <i>Raleway</i> (sans-serif) and <i>Libre Caslon Text</i> (serif). While the frontend "
        "aesthetic is polished, our audit revealed <b>critical gaps in analytics, attribution, local SEO, and review verification</b>."
    )
    story.append(Paragraph(tech_overview_text, body_style))
    story.append(Spacer(1, 7))

    tech_audit_data = [
        [Paragraph("Technical Dimension", table_header), Paragraph("Observed Status on Alandas.de", table_header), Paragraph("Business Impact &amp; Severity", table_header)],
        [
            Paragraph("<b>Web Analytics (GA4 / GTM)</b>", table_cell_bold),
            Paragraph("<b>COMPLETELY MISSING.</b> No Google Analytics 4 (`G-XXXXXX`) or GTM container installed.", table_cell),
            Paragraph("<font color='#991B1B'><b>CRITICAL:</b></font> Zero visibility into funnel drop-offs, checkout abandonment, or acquisition sources.", table_cell)
        ],
        [
            Paragraph("<b>Paid Ad Attribution</b>", table_cell_bold),
            Paragraph("<b>COMPLETELY MISSING.</b> No Meta Pixel (Facebook/Instagram), TikTok Pixel, or CAPI.", table_cell),
            Paragraph("<font color='#991B1B'><b>CRITICAL:</b></font> Running ads burns cash blindly—no algorithm optimization or retargeting audiences.", table_cell)
        ],
        [
            Paragraph("<b>Email Marketing Engine</b>", table_cell_bold),
            Paragraph("No Klaviyo, Omnisend, or Mailchimp. Only Shopify's default unsegmented newsletter input form.", table_cell),
            Paragraph("<font color='#C58B2B'><b>HIGH LEAK:</b></font> Missing 20–30% in automated back-end email revenue (welcome, cart recovery, replenishment).", table_cell)
        ],
        [
            Paragraph("<b>Customer Reviews Engine</b>", table_cell_bold),
            Paragraph("3 static text quotes on homepage (Jasmin, Marah, Allen). <b>Zero review apps on PDPs</b> (Judge.me/Loox).", table_cell),
            Paragraph("<font color='#C58B2B'><b>HIGH FRICTION:</b></font> No verified buyer badges, no star ratings on product pages, and no Google search rich snippets.", table_cell)
        ],
        [
            Paragraph("<b>Google Business Profile</b>", table_cell_bold),
            Paragraph("Verified under <b>'alanda's tea'</b> (5.0★, 2 reviews), but categorized only as 'E-commerce service' (hidden address).", table_cell),
            Paragraph("<font color='#C58B2B'><b>LOCAL GAP:</b></font> Pin drops in central Germany instead of Berlin. Misses all Berlin HoReCa local map searches.", table_cell)
        ],
        [
            Paragraph("<b>Agentic Commerce (UCP)</b>", table_cell_bold),
            Paragraph("Implemented! `/agents.md` and `sitemap_agentic_discovery.xml` active with Universal Commerce Protocol.", table_cell),
            Paragraph("<font color='#064E3B'><b>POSITIVE:</b></font> Forward-looking protocol enabling AI shopping agents to crawl and parse products.", table_cell)
        ],
        [
            Paragraph("<b>Schema.org Structured Data</b>", table_cell_bold),
            Paragraph("JSON-LD Organization schema outputs empty strings `\"\"` for unfilled social handles.", table_cell),
            Paragraph("<font color='#64748B'><b>MEDIUM:</b></font> Triggers Google rich snippet validation warnings in Search Console.", table_cell)
        ]
    ]

    tech_table = Table(tech_audit_data, colWidths=[120, 190, 205])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_MIDNIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 9))

    tech_summary_card = (
        "<b>Technical Synthesis for Consultation:</b><br/>"
        "Alandas has built an attractive digital storefront and embraced innovative protocols (UCP / agents.md), but is <b>flying blind "
        "operationally</b>. Without GA4, Meta CAPI, or Klaviyo, the client cannot calculate Customer Acquisition Cost (CAC), cannot retarget "
        "engaged visitors, and loses 20%+ in automated email revenue. Furthermore, while Sidy has 2 Google reviews and 3 homepage testimonials, "
        "they are not linked to a functional product review engine or local Berlin map pack ranking. Fixing this represents immediate ROI."
    )
    story.append(make_card(Paragraph(tech_summary_card, callout_style), bg_color="#FEF9EE", border_color="#E9D4A5", left_border_color="#C58B2B", padding=8))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: DUAL CUSTOMER VIEWPOINTS: B2C VS B2B
    # =========================================================================
    story.append(Paragraph("AUDIT CHAPTER 04 // CUSTOMER EXPERIENCE", kicker_style))
    story.append(Paragraph("4. Customer Journey Evaluation: B2C vs B2B Perspectives", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "To maximize impact during the client pitch, we evaluated the storefront through two distinct commercial personas: "
        "the retail consumer (B2C) seeking an aesthetic lifestyle experience, and the professional cafe or hotel operator (B2B) "
        "seeking beverage margin expansion and operational simplicity.",
        body_style
    ))
    story.append(Spacer(1, 7))

    b2c_content = [
        [Paragraph("<b>A. THE B2C CONSUMER VIEWPOINT (Retail Buyer Journey)</b>", table_header)],
        [Paragraph(
            "<b>The Strengths (What Hooks the Consumer):</b><br/>"
            "• <b>Sensory Destination Storytelling:</b> Blends named after iconic cultural capitals (Istanbul, Paris, Marrakech) immediately elevate "
            "the product above generic supermarket teas, evoking travel, mindfulness, and sensory exploration.<br/>"
            "• <b>Ingredient Transparency:</b> Prominently lists whole botanical ingredients (real strawberry chunks, uncrushed chamomile "
            "blossoms, real bergamot oil on Rwanda Rukeri) with zero artificial flavor enhancers.<br/>"
            "• <b>Frictionless Mobile Checkout:</b> Native 1-click checkout with Apple Pay, Google Pay, Shop Pay, and Klarna.<br/><br/>"
            "<b>The Dealbreakers (What Causes Cart Abandonment):</b><br/>"
            "• <b>Unverified Social Proof:</b> The homepage has 3 text quotes (Jasmin B., Marah A., Allen W.), but individual product pages have "
            "zero star ratings or review widgets. In Germany, unverified text quotes lack credibility without 'Verified Buyer' badges.<br/>"
            "• <b>Conflicting Shipping Thresholds:</b> Product descriptions state <i>'Free shipping over €59'</i>, but the shipping policy page "
            "states <i>'Free shipping over €40'</i>. A customer ordering €45 who gets hit with shipping at checkout will abandon.<br/>"
            "• <b>Excessive Trial Commitment (220g Only):</b> No sampler discovery packs exist. Sampling 3 flavors requires spending €44.07 for "
            "660g of tea, which is an excessive commitment for first-time shoppers.",
            callout_style
        )]
    ]
    b2c_box = Table(b2c_content, colWidths=[PAGE_WIDTH - 80])
    b2c_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SLATE),
        ('BACKGROUND', (0,1), (-1,1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(b2c_box)
    story.append(Spacer(1, 9))

    b2b_content = [
        [Paragraph("<b>B. THE B2B OPERATOR VIEWPOINT (Cafe, Bistro &amp; Hotelier Journey)</b>", table_header)],
        [Paragraph(
            "<b>The Strengths (What Hooks the Hospitality Operator):</b><br/>"
            "• <b>Solves a Universal Pain Point:</b> In 90% of cafes, tea is an afterthought—a cheap €0.10 teabag in warm water for €3.80. "
            "Alandas transforms tea into a high-margin visual ritual served on a dedicated bamboo tray.<br/>"
            "• <b>High Gross Margin (90%+):</b> Cost per pot ~€0.25 vs. €4.50–€5.90 menu price. Selling just 20 pots a day generates €1,400+ in extra "
            "gross profit per month (€17,000/year).<br/>"
            "• <b>Operational Simplicity:</b> Handcrafted borosilicate pot with lid filter means baristas don't deal with messy strainers, "
            "and preparation takes only 15 seconds.<br/><br/>"
            "<b>The Dealbreakers (What Kills the Wholesale Deal):</b><br/>"
            "• <b>Sample Box Price Contradiction:</b> The Gastro page lists the box at <b>€19.00</b>, while the Contact page advertises it at "
            "<b>€9.90 netto</b>. This pricing mismatch undermines trust.<br/>"
            "• <b>Flagship Display Shelf is Out of Stock:</b> The Teebar wooden rack (€79.00), marketed as the visual centerpiece, is unavailable.<br/>"
            "• <b>Local Berlin Map Invisibility:</b> Because Google Business Profile is set as an online e-commerce service, the pin is dropped "
            "in central Germany. Berlin cafe owners searching locally for <i>'Tee Großhandel Berlin'</i> will never find Alandas.<br/>"
            "• <b>Unstructured Wholesale Ordering:</b> Currently relies on <i>'Send a WhatsApp photo of your order'</i>. Multi-unit cafes require "
            "automated net-price accounts, volume tiers, and formal VAT purchase orders.",
            callout_style
        )]
    ]
    b2b_box = Table(b2b_content, colWidths=[PAGE_WIDTH - 80])
    b2b_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_MIDNIGHT),
        ('BACKGROUND', (0,1), (-1,1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(b2b_box)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: CRITICAL STOREFRONT INCONSISTENCIES & DISCOVERY QUESTIONS
    # =========================================================================
    story.append(Paragraph("AUDIT CHAPTER 05 // DISCREPANCIES & DISCOVERY", kicker_style))
    story.append(Paragraph("5. Critical Inconsistencies &amp; Strategic Discovery Questions", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Below is the consolidated matrix of technical and commercial discrepancies discovered during the audit, along with "
        "high-leverage discovery questions to lead your client consultation with Sidy Sow.",
        body_style
    ))
    story.append(Spacer(1, 6))

    glitch_data = [
        [Paragraph("Discrepancy Item", table_header), Paragraph("Location A (Storefront)", table_header), Paragraph("Location B (Conflict)", table_header), Paragraph("Recommended Resolution", table_header)],
        [
            Paragraph("<b>Shipping Free Threshold</b>", table_cell_bold),
            Paragraph("PDPs: <b>€59.00</b> (under 'Versand')", table_cell),
            Paragraph("Policy Page: <b>€40.00</b>", table_cell),
            Paragraph("Standardize unified threshold at <b>€49.00</b> with interactive cart progress bar.", table_cell)
        ],
        [
            Paragraph("<b>Gastro Sample Box Price</b>", table_cell_bold),
            Paragraph("Gastro Page: <b>€19.00</b>", table_cell),
            Paragraph("Contact Page: <b>€9.90 netto</b>", table_cell),
            Paragraph("Set at <b>€9.90 netto</b> (100% credited against first wholesale order).", table_cell)
        ],
        [
            Paragraph("<b>Phone Number Mismatch</b>", table_cell_bold),
            Paragraph("Website / WhatsApp: <b>+49 15678 689200</b>", table_cell),
            Paragraph("Google Maps: <b>+49 1515 6856439</b>", table_cell),
            Paragraph("Synchronize numbers so incoming Google calls route straight to WhatsApp Business.", table_cell)
        ],
        [
            Paragraph("<b>Google Maps Location Pin</b>", table_cell_bold),
            Paragraph("Registered Address: <b>Berlin (10589)</b>", table_cell),
            Paragraph("Google Map Pin: <b>Central Germany</b>", table_cell),
            Paragraph("Add Berlin/Potsdam as primary Service Area &amp; set category to <i>Tee-Großhändler</i>.", table_cell)
        ],
        [
            Paragraph("<b>Teebar Shelf Inventory</b>", table_cell_bold),
            Paragraph("Gastro Copy: <i>'Visual Highlight'</i>", table_cell),
            Paragraph("PDP: <b>Unavailable / Out of Stock</b>", table_cell),
            Paragraph("Enable <i>'Pre-Order for Your Venue'</i> button with 10-day dispatch notice.", table_cell)
        ],
        [
            Paragraph("<b>Social Proof Architecture</b>", table_cell_bold),
            Paragraph("Homepage: 3 static text quotes", table_cell),
            Paragraph("PDPs: <b>0 stars / 0 review app</b>", table_cell),
            Paragraph("Import quotes into Judge.me as verified seed reviews; anchor star ratings to PDPs.", table_cell)
        ]
    ]

    glitch_table = Table(glitch_data, colWidths=[105, 120, 120, 170])
    glitch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_MIDNIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(glitch_table)
    story.append(Spacer(1, 9))

    questions_content = [
        [Paragraph("<b>HIGH-LEVERAGE DISCOVERY QUESTIONS TO ASK THE CLIENT</b>", table_header)],
        [Paragraph(
            "1. <i>'I saw you have a 5.0 rating with 2 reviews on Google under alanda's tea—is +49 1515 6856439 your direct line, and should we route Google leads straight into your main business WhatsApp (+49 15678 689200)?'</i><br/>"
            "2. <i>'You have wonderful quotes from Jasmin, Marah, and Allen on the homepage—have you considered pulling those star ratings onto the individual product pages with Judge.me to lift conversion on Schwarzwald and Istanbul?'</i><br/>"
            "3. <i>'I noticed the Teebar wooden shelf is out of stock online—are you currently fulfilling wholesale display racks manually, or is supplier inventory a bottleneck for onboarding new cafes?'</i><br/>"
            "4. <i>'Right now your Gastro Experience Box is listed at €19 on the B2B page but €9.90 on the contact page—which price point has yielded higher trial conversion for cafes?'</i><br/>"
            "5. <i>'Since there is currently no GA4 or Meta Pixel active on the store, what channel currently drives your primary sales: Instagram organic, Berlin word-of-mouth, or in-person B2B sales visits?'</i>",
            callout_style
        )]
    ]
    q_box = Table(questions_content, colWidths=[PAGE_WIDTH - 80])
    q_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_GOLD),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FFFAF0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E9D4A5")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(q_box)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: STRATEGIC 30-DAY GROWTH ROADMAP & MODERN TECH STACK
    # =========================================================================
    story.append(Paragraph("AUDIT CHAPTER 06 // REVENUE BLUEPRINT", kicker_style))
    story.append(Paragraph("6. Strategic 30-Day Growth Roadmap &amp; Technology Stack", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph(
        "Presenting this structured 30-day growth blueprint during consultation immediately positions you as an indispensable "
        "commercial growth partner rather than a commoditized web developer.",
        body_style
    ))
    story.append(Spacer(1, 6))

    roadmap_data = [
        [Paragraph("Implementation Phase", table_header), Paragraph("Key Deliverables &amp; Action Steps", table_header), Paragraph("Measurable Business Impact", table_header)],
        [
            Paragraph("<b>Phase 1: Conversion Triage &amp; Google Sync</b><br/><i>(Days 1 – 7)</i>", table_cell_bold),
            Paragraph(
                "• Standardize shipping policy (€49 unified threshold + cart bar).<br/>"
                "• Resolve sample box pricing (€9.90 credited against first order).<br/>"
                "• Update Google Business Profile (Berlin service area + phone sync).<br/>"
                "• Install Judge.me / Loox; seed with Jasmin, Marah, Allen &amp; Google reviews.",
                table_cell
            ),
            Paragraph("Stops immediate cart drops; unlocks Berlin local search; lifts storefront conversion 15–25%.", table_cell)
        ],
        [
            Paragraph("<b>Phase 2: Analytics &amp; Retention Engine</b><br/><i>(Days 8 – 14)</i>", table_cell_bold),
            Paragraph(
                "• Deploy Google Analytics 4 (GA4) with enhanced e-commerce funnels.<br/>"
                "• Install Meta Pixel &amp; CAPI to prepare for retargeting ads.<br/>"
                "• Connect Klaviyo email automation:<br/>"
                "  - Welcome Flow with 10% first-time discount code.<br/>"
                "  - 3-step Abandoned Cart recovery highlighting sensory tea rituals.<br/>"
                "  - Automated 45-day replenishment reminders based on tea consumption.",
                table_cell
            ),
            Paragraph("Unlocks full traffic attribution and captures 20%+ in automated back-end email revenue.", table_cell)
        ],
        [
            Paragraph("<b>Phase 3: Organic IG Funnel &amp; AI Video</b><br/><i>(Days 15 – 21)</i>", table_cell_bold),
            Paragraph(
                "• Deploy <b>OpenReply</b>: Self-hosted Instagram Comment-to-DM engine.<br/>"
                "  - Reel CTA: <i>'Comment CHAI for 10% off + autumn brewing guide'</i>.<br/>"
                "  - Gastro CTA: <i>'Comment GASTRO for wholesale rate card &amp; sample box'</i>.<br/>"
                "• Integrate <b>OpenChatCut</b> (MCP Agent Video Editor) for rapid batch creation of 9:16 vertical tea brewing Reels.",
                table_cell
            ),
            Paragraph("Monetizes Sidy's active `@alandastea` audience without paying expensive SaaS fees (ManyChat).", table_cell)
        ],
        [
            Paragraph("<b>Phase 4: Scaled B2B Wholesale Engine</b><br/><i>(Days 22 – 30)</i>", table_cell_bold),
            Paragraph(
                "• Build dedicated wholesale portal with automatic VAT ID validation.<br/>"
                "• Transparent catering tiers (1kg refill bags with volume discount).<br/>"
                "• Turnkey digital collateral for cafes: printable QR table tents &amp; brewing sheets.<br/>"
                "• Enable Shopify Markets English localization for Berlin expats &amp; hotels.",
                table_cell
            ),
            Paragraph("Transforms informal WhatsApp orders into scalable, predictable recurring B2B accounts across DACH.", table_cell)
        ]
    ]

    road_table = Table(roadmap_data, colWidths=[115, 255, 145])
    road_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_MIDNIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(road_table)
    story.append(Spacer(1, 8))

    closing_box_content = [
        [Paragraph("<b>CONSULTATION PITCH STANCE &amp; CLIENT CLOSING PLAYBOOK</b>", table_header)],
        [Paragraph(
            "<b>The Winning Mindset:</b> Approach Sidy Sow not as a critical auditor pointing out mistakes, but as a strategic commercial "
            "partner presenting <i>unclaimed revenue</i>. He has already built exceptional branding, authentic botanical products, and an "
            "operationally proven hospitality concept in Berlin. By framing your proposal around fixing conversion leaks, syncing his Google "
            "presence, turning Instagram comments into automated DMs (OpenReply), and building a repeatable B2B wholesale engine, you elevate "
            "the conversation from a commoditized freelance job into an indispensable high-ticket growth partnership.",
            callout_style
        )]
    ]
    closing_box = Table(closing_box_content, colWidths=[PAGE_WIDTH - 80])
    closing_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SLATE),
        ('BACKGROUND', (0,1), (-1,1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6.5),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(closing_box)

    # -------------------------------------------------------------
    # BUILD DOCUMENT
    # -------------------------------------------------------------
    doc.build(story, canvasmaker=LuxuryNumberedCanvas)
    print(f"[OK] Generated Master PDF: {PDF_OUT_MAIN}")

    # Mirror to all target paths
    for target in [PDF_OUT_DOCS, PDF_OUT_SCRATCH, PDF_OUT_ARTIFACT, PDF_OUT_ARTIFACT_PREV]:
        try:
            target_dir = os.path.dirname(target)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
            shutil.copy2(PDF_OUT_MAIN, target)
            print(f"[OK] Mirrored to: {target}")
        except Exception as e:
            print(f"[WARN] Could not mirror to {target}: {e}")

if __name__ == "__main__":
    build_pdf()
