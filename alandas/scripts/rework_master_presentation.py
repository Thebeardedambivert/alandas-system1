import re

def build_presentation():
    with open('Alandas_Master_Growth_System.backup.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for slides
    pattern = re.compile(r'<!-- SLIDE (\d+): (.*?) -->\s*<section class="slide([^"]*)">(.*?)</section>', re.DOTALL)
    slides = pattern.findall(content)
    total_slides = len(slides)
    print(f"Loaded {total_slides} slides from backup.")

    slide_html_list = []
    
    for num_str, name, extra_class, body in slides:
        num = int(num_str)
        is_first = (num == 1)
        active_class = " active visible" if is_first else ""
        
        # Extract kicker, slide-title, slide-lead if present
        kicker_match = re.search(r'<div class="kicker">(.*?)</div>', body, re.DOTALL)
        title_match = re.search(r'<h1 class="slide-title"[^>]*>(.*?)</h1>', body, re.DOTALL)
        lead_match = re.search(r'<p class="slide-lead"[^>]*>(.*?)</p>', body, re.DOTALL)
        
        kicker_html = kicker_match.group(0).strip() if kicker_match else ""
        title_html = re.sub(r'\s+style="[^"]*"', '', title_match.group(0)).strip() if title_match else ""
        lead_html = re.sub(r'\s+style="[^"]*"', '', lead_match.group(0)).strip() if lead_match else ""
        
        # Build clean header
        header_html = f"""      <header class="slide-header reveal">
        {kicker_html}
        {title_html}
        {lead_html}
      </header>"""

        # Now extract the content body
        cleaned_body = body
        if kicker_match:
            cleaned_body = cleaned_body.replace(kicker_match.group(0), '')
        if title_match:
            cleaned_body = cleaned_body.replace(title_match.group(0), '')
        if lead_match:
            cleaned_body = cleaned_body.replace(lead_match.group(0), '')
        
        # Check for bottom note / footer note in original FIRST (before stripping inline styles)
        footer_note_match = re.search(r'<div style="[^"]*font-size:\s*0\.75rem[^"]*">(.*?)</div>', cleaned_body, re.DOTALL)
        footer_note_text = ""
        if footer_note_match:
            footer_note_text = re.sub(r'<[^>]+>', ' ', footer_note_match.group(1)).strip()
            footer_note_text = re.sub(r'\s+', ' ', footer_note_text)
            cleaned_body = cleaned_body.replace(footer_note_match.group(0), '')
        
        if not footer_note_text:
            footer_note_text = "ALANDAS TEA BERLIN • MASTER COMMERCIAL GROWTH & OPERATING SYSTEM • NATIONWIDE GERMANY"

        # Remove empty <div></div> from the top if left behind
        cleaned_body = re.sub(r'^\s*<div>\s*</div>\s*', '', cleaned_body, flags=re.DOTALL)
        
        # Clean any stray footer div left behind
        cleaned_body = re.sub(r'<div style="[^"]*JetBrains Mono[^"]*">.*?</div>', '', cleaned_body, flags=re.DOTALL)
        
        # Clean inline font sizes that shrink text on cards and paragraphs
        cleaned_body = re.sub(r'style="font-size:\s*0\.[789]\d*rem;?\s*(.*?)"', r'style="\1"', cleaned_body)
        cleaned_body = re.sub(r'style="font-size:\s*1[0-4]px;?\s*(.*?)"', r'style="\1"', cleaned_body)
        cleaned_body = re.sub(r'style="\s*"', '', cleaned_body)
        
        # Ground-Truth Strategic Synchronizations (Sidy Sow Discovery Session)
        cleaned_body = re.sub(r'€9\.90|\b9\.90\b', '€19.00', cleaned_body)
        cleaned_body = cleaned_body.replace(
            'credited 5-blend discovery box',
            '€19 credited trial box (ultra-thick shatter-resistant teapot + tray + spoon + 5 blends)'
        )
        cleaned_body = cleaned_body.replace(
            '25 accounts generate €2,500–€5,000 predictable monthly baseline',
            'Phase 1: 25 accounts (€2,500–€5k/mo) → Master Goal: 100 accounts (€15,000–€30,000/mo freedom milestone)'
        )
        cleaned_body = cleaned_body.replace(
            '25 active accounts = €75,000+ recurring annual',
            'Phase 1: 25 accounts (€75k ARR) • Master Goal: 100 accounts (€180k–€360k recurring ARR)'
        )
        cleaned_body = cleaned_body.replace(
            'HubSpot / Brevo CRM',
            'Dolibarr CRM (System of Record) + Hermes AI Order Parser'
        )
        cleaned_body = cleaned_body.replace(
            'Engaged Instagram audience on @alandastea',
            'Dual Instagram Channels (@alandastea B2C + dedicated B2B hospitality page)'
        )
        cleaned_body = cleaned_body.replace(
            'Orders written in WhatsApp chats without formal inventory sync',
            'Clients send paper order photos & voice notes via WhatsApp; manual invoicing bogs Sidy down'
        )
        cleaned_body = cleaned_body.replace(
            'Founder spends 15+ hours texting cafes',
            'Sidy manages 10–20 WhatsApp chats daily while working day job in Switzerland'
        )
        cleaned_body = cleaned_body.replace(
            '100 Target Venues',
            '100 Target Venues (Sprint to 100 Active Accounts)'
        )
        
        # Add reveal classes to cards and stat boxes for staggered smooth animations
        def add_reveal_to_cards(grid_match):
            grid_html = grid_match.group(0)
            card_matches = re.split(r'(<div class="(?:card|stat-box)[^"]*">)', grid_html)
            out = []
            delay_idx = 1
            for part in card_matches:
                if part.startswith('<div class="card') or part.startswith('<div class="stat-box'):
                    part = part.replace('class="', f'class="reveal reveal-delay-{min(delay_idx, 6)} ')
                    delay_idx += 1
                out.append(part)
            return "".join(out)
        
        # Process grids
        cleaned_body = re.sub(r'<div class="grid grid-\d+">.*?</div>\s*(?=(?:<div class="grid|<div class="table|<div style|$))', add_reveal_to_cards, cleaned_body, flags=re.DOTALL)
        
        # If table, add reveal to table-container
        cleaned_body = cleaned_body.replace('<div class="table-container">', '<div class="table-container reveal reveal-delay-2">')

        # Format slide HTML
        slide_block = f"""    <!-- SLIDE {num}: {name} -->
    <section class="slide{active_class}" id="slide-{num}">
{header_html}
      <div class="slide-body">
{cleaned_body.strip()}
      </div>
      <footer class="slide-footer reveal">
        <span class="footer-meta">{footer_note_text}</span>
        <span class="footer-counter">{str(num).zfill(2)} / {str(total_slides).zfill(2)}</span>
      </footer>
    </section>"""
        slide_html_list.append(slide_block)

    all_slides_html = "\n\n".join(slide_html_list)

    # Read viewport-base.css contents
    with open('.agents/skills/frontend-slides/viewport-base.css', 'r', encoding='utf-8') as f:
        viewport_base_css = f.read()

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alandas Tea Berlin — Master Commercial Growth & Operating System</title>

  <!-- Typography: Luxury Artisanal Editorial & Precision Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    /* ===========================================
       CSS CUSTOM PROPERTIES (THEME TOKENS)
       Bespoke Artisanal Luxury for Alandas Tea Berlin
       =========================================== */
    :root {{
      /* Viewport Stage & Canvas */
      --stage-bg: #0C0F0C; /* Deep botanical obsidian letterboxing */
      --slide-bg: #F9F7F2; /* Warm organic ivory/parchment */
      --slide-gradient: radial-gradient(1300px 900px at 50% 0%, #FFFFFF 0%, #F9F7F2 65%, #F2EEE4 100%);

      /* Typography */
      --font-display: 'Playfair Display', Georgia, serif;
      --font-body: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      /* Primary Brand Colors */
      --olive: #444C32;
      --olive-dark: #2E3422;
      --olive-light: #EEF2E8;
      --olive-border: #D1D9C5;

      --ochre: #C48737;
      --ochre-dark: #9A6622;
      --ochre-light: #FCF4E8;
      --ochre-border: #F0DFC2;

      --forest: #2F5339;
      --forest-dark: #1E3725;
      --forest-light: #EDF5EF;
      --forest-border: #C8DEC2;

      /* Neutrals & Surfaces */
      --text-main: #181916;
      --text-muted: #5C5950;
      --text-subtle: #8C887C;
      --card-bg: #FFFFFF;
      --card-alt: #F3EFE6;
      --border: #E4DFD3;
      --border-light: #EFECE4;
      --border-focus: #C8BFAD;

      /* Elevation & Shadows */
      --shadow-sm: 0 4px 16px rgba(24, 25, 22, 0.04), 0 1px 3px rgba(24, 25, 22, 0.02);
      --shadow-md: 0 10px 30px rgba(24, 25, 22, 0.07), 0 2px 6px rgba(24, 25, 22, 0.03);
      --shadow-lg: 0 20px 48px rgba(24, 25, 22, 0.10), 0 4px 12px rgba(24, 25, 22, 0.04);

      /* Motion */
      --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
      --duration-normal: 0.55s;
    }}

    /* Global resets */
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    /* ===========================================
       MANDATORY VIEWPORT BASE STYLES
       (From .agents/skills/frontend-slides/viewport-base.css)
       =========================================== */
{viewport_base_css}

    /* ===========================================
       SLIDE CANVAS & TYPOGRAPHY (1920x1080 STAGE)
       Authored at 1920x1080 design size
       =========================================== */
    .deck-stage {{
      background: var(--slide-bg);
      background-image: var(--slide-gradient);
    }}

    .slide {{
      background: var(--slide-bg);
      background-image: var(--slide-gradient);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 56px 88px 36px 88px;
      font-family: var(--font-body);
      color: var(--text-main);
      -webkit-font-smoothing: antialiased;
    }}

    /* Slide Header */
    .slide-header {{
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      margin-bottom: 12px;
    }}

    .kicker {{
      font-family: var(--font-mono);
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--olive);
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }}

    .kicker::before {{
      content: '';
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--ochre);
      box-shadow: 0 0 12px rgba(196, 135, 55, 0.5);
    }}

    h1.slide-title {{
      font-family: var(--font-display);
      font-size: 56px;
      font-weight: 600;
      letter-spacing: -0.02em;
      line-height: 1.14;
      color: var(--text-main);
      margin-bottom: 12px;
    }}

    #slide-1 h1.slide-title {{
      font-size: 70px;
      line-height: 1.1;
      margin-top: 10px;
      margin-bottom: 18px;
    }}

    p.slide-lead {{
      font-size: 24px;
      line-height: 1.45;
      color: var(--text-muted);
      max-width: 1560px;
      font-weight: 400;
    }}

    #slide-1 p.slide-lead {{
      font-size: 26px;
      line-height: 1.45;
      margin-bottom: 24px;
    }}

    /* Slide Body (Center Canvas) */
    .slide-body {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 0;
      width: 100%;
      margin: 10px 0 12px 0;
    }}

    /* Slide Footer / Meta */
    .slide-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--border);
      padding-top: 14px;
      margin-bottom: 14px;
      flex-shrink: 0;
    }}

    .footer-meta {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-subtle);
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}

    .footer-counter {{
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 700;
      color: var(--olive);
      letter-spacing: 0.1em;
    }}

    /* ===========================================
       GRIDS & CARD ARCHITECTURE (1920x1080 OPTIMIZED)
       =========================================== */
    .grid {{
      display: grid;
      width: 100%;
      box-sizing: border-box;
    }}

    .grid-2 {{
      grid-template-columns: repeat(2, 1fr);
      gap: 40px;
    }}

    .grid-3 {{
      grid-template-columns: repeat(3, 1fr);
      gap: 32px;
    }}

    .grid-4 {{
      grid-template-columns: repeat(4, 1fr);
      gap: 24px;
    }}

    .grid-5 {{
      grid-template-columns: repeat(5, 1fr);
      gap: 20px;
    }}

    .grid-6 {{
      grid-template-columns: repeat(6, 1fr);
      gap: 18px;
    }}

    /* Base Cards */
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 38px 36px;
      box-shadow: var(--shadow-sm);
      transition: transform 0.25s var(--ease-out-expo), box-shadow 0.25s var(--ease-out-expo), border-color 0.25s var(--ease-out-expo);
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      position: relative;
    }}

    .card:hover {{
      box-shadow: var(--shadow-md);
      border-color: var(--border-focus);
      transform: translateY(-3px);
    }}

    .card.highlight {{
      background: var(--card-alt);
      border-color: var(--border-focus);
    }}

    .card-tag {{
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 700;
      color: var(--olive);
      text-transform: uppercase;
      letter-spacing: 0.14em;
      margin-bottom: 12px;
    }}

    .card-tag.ochre {{ color: var(--ochre); }}
    .card-tag.forest {{ color: var(--forest); }}

    .card h3 {{
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 16px;
      line-height: 1.25;
    }}

    .card p {{
      font-size: 19px;
      color: var(--text-muted);
      line-height: 1.55;
    }}

    .card ul {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .card li {{
      font-size: 19px;
      color: var(--text-muted);
      line-height: 1.55;
      position: relative;
      padding-left: 24px;
    }}

    .card li::before {{
      content: '•';
      position: absolute;
      left: 0;
      color: var(--olive);
      font-weight: bold;
      font-size: 22px;
      line-height: 1;
    }}

    .card li strong {{
      color: var(--text-main);
      font-weight: 600;
    }}

    /* 1-Row Grid-2 Cards (Slides 5, 9, 14, 16, 17, 18, 19, 20, 25, 28) */
    .grid-2 .card {{
      padding: 46px 46px;
      min-height: 520px;
    }}
    .grid-2 .card h3 {{
      font-size: 32px;
      margin-bottom: 20px;
    }}
    .grid-2 .card li {{
      font-size: 20px;
      line-height: 1.6;
    }}
    .grid-2 .card ul {{
      gap: 16px;
    }}

    /* 1-Row Grid-3 Cards (Slides 7, 12, 22) */
    .grid-3 .card {{
      padding: 42px 36px;
      min-height: 520px;
    }}
    .grid-3 .card h3 {{
      font-size: 28px;
      margin-bottom: 18px;
    }}
    .grid-3 .card li {{
      font-size: 19px;
      line-height: 1.55;
    }}
    .grid-3 .card ul {{
      gap: 14px;
    }}

    /* 1-Row Grid-4 Cards (Slides 2, 21, 23) */
    .grid-4 .card {{
      padding: 36px 28px;
      min-height: 520px;
    }}
    .grid-4 .card h3 {{
      font-size: 26px;
      margin-bottom: 16px;
    }}
    .grid-4 .card li {{
      font-size: 17.5px;
      line-height: 1.5;
    }}
    .grid-4 .card ul {{
      gap: 12px;
    }}

    /* 1-Row Grid-5 Cards (Slides 6, 10, 15) */
    .grid-5 .card {{
      padding: 32px 22px;
      min-height: 520px;
    }}
    .grid-5 .card h3 {{
      font-size: 23px;
      margin-bottom: 14px;
    }}
    .grid-5 .card li {{
      font-size: 16.5px;
      line-height: 1.45;
    }}
    .grid-5 .card p {{
      font-size: 16.5px;
      line-height: 1.45;
    }}
    .grid-5 .card ul {{
      gap: 10px;
    }}

    /* Slide 1 Sprints Cards */
    #slide-1 .grid-5 .card {{
      padding: 38px 26px;
      min-height: 240px;
    }}
    #slide-1 .grid-5 .card .card-tag {{
      font-size: 15px;
      margin-bottom: 12px;
    }}
    #slide-1 .grid-5 .card h3 {{
      font-size: 26px;
      margin-bottom: 14px;
    }}
    #slide-1 .grid-5 .card p {{
      font-size: 17.5px;
      line-height: 1.5;
    }}

    /* 1-Row Grid-6 Cards (Slide 27 Roadmap) */
    .grid-6 .card {{
      padding: 28px 20px;
      min-height: 520px;
    }}
    .grid-6 .card-tag {{
      font-size: 13.5px;
      margin-bottom: 8px;
    }}
    .grid-6 .card h3 {{
      font-size: 21px;
      margin-bottom: 12px;
    }}
    .grid-6 .card li {{
      font-size: 15.5px;
      line-height: 1.45;
    }}
    .grid-6 .card ul {{
      gap: 8px;
    }}

    /* Special 2-row grid-3 on Slide 13 (The Evidence-Based Intervention Loop) */
    #slide-13 .grid-3 {{
      gap: 28px;
    }}
    #slide-13 .card {{
      padding: 40px 38px;
      min-height: 240px;
      justify-content: center;
    }}
    #slide-13 .card-tag {{
      font-size: 15px;
      margin-bottom: 10px;
    }}
    #slide-13 .card h3 {{
      font-size: 30px;
      margin-bottom: 14px;
    }}
    #slide-13 .card p {{
      font-size: 20px;
      line-height: 1.55;
    }}

    /* Special 2-row grid-3 on Slide 4 (6 Gaps) */
    #slide-4 .grid-3 {{
      gap: 24px;
    }}
    #slide-4 .card {{
      padding: 28px 30px;
      min-height: 240px;
    }}
    #slide-4 .card-tag {{
      font-size: 14px;
      margin-bottom: 8px;
    }}
    #slide-4 .card h3 {{
      font-size: 24px;
      margin-bottom: 12px;
    }}
    #slide-4 .card li {{
      font-size: 17px;
      line-height: 1.45;
    }}
    #slide-4 .card ul {{
      gap: 9px;
    }}

    /* Special 3-row grid-3 on Slide 8 (9 Stages) */
    #slide-8 .grid-3 {{
      gap: 16px;
    }}
    #slide-8 .card {{
      padding: 20px 24px;
      min-height: 155px;
    }}
    #slide-8 .card-tag {{
      font-size: 13px;
      margin-bottom: 6px;
    }}
    #slide-8 .card h3 {{
      font-size: 22px;
      margin-bottom: 8px;
    }}
    #slide-8 .card p {{
      font-size: 16px;
      line-height: 1.42;
    }}

    /* Special 2-row grid-3 on Slide 26 (What Success Looks Like) */
    #slide-26 .grid-3 {{
      gap: 24px;
    }}
    #slide-26 .card {{
      padding: 36px 34px;
      min-height: 240px;
      justify-content: center;
    }}
    #slide-26 .card h3 {{
      font-size: 26px;
      margin-bottom: 12px;
    }}
    #slide-26 .card p {{
      font-size: 19px;
      line-height: 1.5;
    }}

    /* Stat Box (Slide 3 & Slide 24 metrics) */
    .stat-box {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 26px 28px;
      box-shadow: var(--shadow-sm);
    }}

    .stat-number {{
      font-family: var(--font-display);
      font-size: 58px;
      font-weight: 700;
      color: var(--olive);
      line-height: 1;
      margin-bottom: 8px;
    }}

    .stat-number.ochre {{ color: var(--ochre); }}
    .stat-number.forest {{ color: var(--forest); }}

    .stat-label {{
      font-size: 19px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 4px;
    }}

    .stat-sub {{
      font-size: 16px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    /* Slide 3 Layout Customization */
    #slide-3 .grid-2 .card {{
      min-height: 330px;
      padding: 38px 40px;
    }}

    /* Table Architecture (Slide 11 Scoring Rubric) */
    .table-container {{
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 18px;
      background: var(--card-bg);
      box-shadow: var(--shadow-sm);
      overflow: hidden;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }}

    th {{
      background: var(--olive);
      color: #FFFFFF;
      font-size: 17px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 20px 26px;
    }}

    td {{
      padding: 18px 26px;
      font-size: 17.5px;
      color: var(--text-main);
      border-bottom: 1px solid var(--border-light);
      line-height: 1.5;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    tr:nth-child(even) td {{
      background: var(--card-alt);
    }}

    /* Badges */
    .badge {{
      display: inline-block;
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}

    .badge-olive {{
      background: var(--olive-light);
      color: var(--olive-dark);
      border: 1px solid var(--olive-border);
    }}

    .badge-ochre {{
      background: var(--ochre-light);
      color: var(--ochre-dark);
      border: 1px solid var(--ochre-border);
    }}

    .badge-forest {{
      background: var(--forest-light);
      color: var(--forest-dark);
      border: 1px solid var(--forest-border);
    }}

    /* ===========================================
       ANIMATIONS (REVEAL ON ACTIVE SLIDE)
       =========================================== */
    .reveal {{
      opacity: 0;
      transform: translateY(22px);
      transition: opacity var(--duration-normal) var(--ease-out-expo),
                  transform var(--duration-normal) var(--ease-out-expo);
    }}

    .slide.visible .reveal {{
      opacity: 1;
      transform: translateY(0);
    }}

    .reveal-delay-1 {{ transition-delay: 0.07s; }}
    .reveal-delay-2 {{ transition-delay: 0.14s; }}
    .reveal-delay-3 {{ transition-delay: 0.21s; }}
    .reveal-delay-4 {{ transition-delay: 0.28s; }}
    .reveal-delay-5 {{ transition-delay: 0.35s; }}
    .reveal-delay-6 {{ transition-delay: 0.42s; }}

    /* ===========================================
       PRESENTATION CHROME & CONTROLS (OUTSIDE STAGE)
       =========================================== */
    .viewport-progress-bar {{
      position: fixed;
      top: 0;
      left: 0;
      height: 3.5px;
      background: linear-gradient(90deg, var(--olive) 0%, var(--ochre) 100%);
      width: 0%;
      transition: width 0.3s ease;
      z-index: 9999;
    }}

    .deck-controls {{
      position: fixed;
      bottom: 22px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      display: flex;
      align-items: center;
      gap: 10px;
      background: rgba(14, 18, 15, 0.88);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 7px 18px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.14);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
    }}

    .ctrl-btn {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 999px;
      padding: 5px 13px;
      font-size: 12.5px;
      font-weight: 600;
      color: #FFFFFF;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      font-family: var(--font-body);
    }}

    .ctrl-btn:hover {{
      background: rgba(255, 255, 255, 0.18);
      border-color: rgba(255, 255, 255, 0.35);
      transform: translateY(-1px);
    }}

    .ctrl-counter {{
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: #E8E4DB;
      min-width: 76px;
      text-align: center;
      letter-spacing: 0.08em;
    }}

    /* ===========================================
       INLINE EDITING UI
       =========================================== */
    .edit-hotzone {{
      position: fixed;
      top: 0;
      left: 0;
      width: 80px;
      height: 80px;
      z-index: 10000;
      cursor: pointer;
    }}

    .edit-toggle {{
      position: fixed;
      top: 18px;
      left: 18px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease, transform 0.2s ease;
      z-index: 10001;
      background: #181916;
      color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 0.25);
      border-radius: 999px;
      padding: 7px 15px;
      font-size: 12px;
      font-weight: 700;
      font-family: var(--font-body);
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .edit-toggle.show,
    .edit-toggle.active {{
      opacity: 1;
      pointer-events: auto;
    }}

    .edit-toggle.active {{
      background: var(--ochre);
      color: #181916;
      border-color: #FFFFFF;
    }}

    .edit-banner {{
      position: fixed;
      top: 12px;
      left: 50%;
      transform: translateX(-50%) translateY(-60px);
      background: rgba(24, 25, 22, 0.95);
      backdrop-filter: blur(10px);
      border: 1px solid var(--ochre);
      color: #FFFFFF;
      padding: 8px 24px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 600;
      z-index: 10002;
      display: flex;
      align-items: center;
      gap: 16px;
      transition: transform 0.35s var(--ease-out-expo);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    .edit-banner.active {{
      transform: translateX(-50%) translateY(0);
    }}

    .edit-banner-badge {{
      background: var(--ochre);
      color: #181916;
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }}

    .edit-btn-action {{
      background: rgba(255,255,255,0.12);
      border: 1px solid rgba(255,255,255,0.25);
      color: #FFF;
      border-radius: 999px;
      padding: 3px 10px;
      font-size: 11.5px;
      cursor: pointer;
    }}

    .edit-btn-action:hover {{
      background: rgba(255,255,255,0.22);
    }}

    .editable-active {{
      outline: 2px dashed rgba(196, 135, 55, 0.5) !important;
      outline-offset: 3px;
      border-radius: 4px;
      cursor: text;
    }}

    .editable-active:focus {{
      outline: 2px solid var(--ochre) !important;
      background: rgba(196, 135, 55, 0.05);
    }}

    .edit-toast {{
      position: fixed;
      bottom: 74px;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      background: #181916;
      color: #FFFFFF;
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 8px 18px;
      border-radius: 999px;
      font-size: 12.5px;
      font-weight: 600;
      z-index: 10005;
      opacity: 0;
      pointer-events: none;
      transition: all 0.3s ease;
    }}

    .edit-toast.visible {{
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }}
  </style>
</head>
<body>

  <!-- Top Progress Bar (outside stage) -->
  <div class="viewport-progress-bar" id="viewportProgressBar"></div>

  <!-- Inline Editing Hotzone & Trigger -->
  <div class="edit-hotzone" title="Hover corner or press 'E' for Inline Edit Mode"></div>
  <button class="edit-toggle" id="editToggle" title="Edit mode (E)">
    <span>✏️</span> <span>Edit Deck</span>
  </button>

  <!-- Edit Mode Banner -->
  <div class="edit-banner" id="editBanner">
    <span class="edit-banner-badge">Edit Mode Active</span>
    <span>Click text on slide to edit • Changes auto-save to browser • Press <strong>E</strong> to finish</span>
    <button class="edit-btn-action" id="btnResetEdits">Reset to Original</button>
  </div>

  <!-- Main Presentation Viewport Wrapper -->
  <div class="deck-viewport">
    <!-- Fixed 1920x1080 Design Canvas -->
    <main class="deck-stage" id="deckStage">
{all_slides_html}
    </main>
  </div>

  <!-- External Presentation Chrome Controls -->
  <nav class="deck-controls">
    <button class="ctrl-btn" id="btnPrev" title="Previous Slide (← or PageUp)">
      <span>←</span> Prev
    </button>
    <div class="ctrl-counter" id="slideCounter">01 / {str(total_slides).zfill(2)}</div>
    <button class="ctrl-btn" id="btnNext" title="Next Slide (→, Space, PageDown)">
      Next <span>→</span>
    </button>
    <button class="ctrl-btn" id="btnFullscreen" title="Toggle Fullscreen (F)">
      <span>⛶</span>
    </button>
  </nav>

  <script>
    /* ===========================================
       SLIDE PRESENTATION CONTROLLER
       =========================================== */
    class SlidePresentation {{
      constructor() {{
        this.slides = document.querySelectorAll('.slide');
        this.totalSlides = this.slides.length;
        this.currentSlide = 0;
        this.stage = document.getElementById('deckStage');
        this.progressBar = document.getElementById('viewportProgressBar');
        this.slideCounter = document.getElementById('slideCounter');
        this.isWheelThrottled = false;

        this.setupStageScale();
        this.setupKeyboardNav();
        this.setupTouchNav();
        this.setupWheelNav();
        this.setupControls();
        this.restoreSlideFromHash();
        this.showSlide(this.currentSlide, false);
      }}

      setupStageScale() {{
        const scale = () => {{
          const factor = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
          const x = (window.innerWidth - 1920 * factor) / 2;
          const y = (window.innerHeight - 1080 * factor) / 2;
          this.stage.style.transform = `translate(${{x}}px, ${{y}}px) scale(${{factor}})`;
        }};
        scale();
        window.addEventListener('resize', scale);
      }}

      restoreSlideFromHash() {{
        const hash = window.location.hash;
        if (hash && hash.startsWith('#slide-')) {{
          const num = parseInt(hash.replace('#slide-', ''), 10) - 1;
          if (!isNaN(num) && num >= 0 && num < this.totalSlides) {{
            this.currentSlide = num;
          }}
        }}
      }}

      showSlide(index, updateHash = true) {{
        this.currentSlide = Math.max(0, Math.min(index, this.totalSlides - 1));
        this.slides.forEach((slide, i) => {{
          const isActive = i === this.currentSlide;
          slide.classList.toggle('active', isActive);
          slide.classList.toggle('visible', isActive);
        }});

        // Update counter
        const curPadded = String(this.currentSlide + 1).padStart(2, '0');
        const totPadded = String(this.totalSlides).padStart(2, '0');
        if (this.slideCounter) {{
          this.slideCounter.textContent = `${{curPadded}} / ${{totPadded}}`;
        }}

        // Update progress bar
        if (this.progressBar) {{
          const progress = ((this.currentSlide + 1) / this.totalSlides) * 100;
          this.progressBar.style.width = `${{progress}}%`;
        }}

        // Update hash
        if (updateHash) {{
          history.replaceState(null, '', `#slide-${{this.currentSlide + 1}}`);
        }}
      }}

      next() {{
        if (this.currentSlide < this.totalSlides - 1) {{
          this.showSlide(this.currentSlide + 1);
        }}
      }}

      prev() {{
        if (this.currentSlide > 0) {{
          this.showSlide(this.currentSlide - 1);
        }}
      }}

      setupKeyboardNav() {{
        document.addEventListener('keydown', (e) => {{
          // Don't hijack if user is editing text
          if (document.activeElement && document.activeElement.isContentEditable) {{
            return;
          }}
          if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown') {{
            e.preventDefault();
            this.next();
          }} else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'PageUp') {{
            e.preventDefault();
            this.prev();
          }} else if (e.key === 'Home') {{
            e.preventDefault();
            this.showSlide(0);
          }} else if (e.key === 'End') {{
            e.preventDefault();
            this.showSlide(this.totalSlides - 1);
          }} else if (e.key === 'f' || e.key === 'F') {{
            if (!document.fullscreenElement) {{
              document.documentElement.requestFullscreen().catch(() => {{}});
            }} else {{
              document.exitFullscreen().catch(() => {{}});
            }}
          }}
        }});
      }}

      setupTouchNav() {{
        let startX = 0;
        let startY = 0;
        window.addEventListener('touchstart', (e) => {{
          startX = e.touches[0].clientX;
          startY = e.touches[0].clientY;
        }}, {{ passive: true }});

        window.addEventListener('touchend', (e) => {{
          const deltaX = e.changedTouches[0].clientX - startX;
          const deltaY = e.changedTouches[0].clientY - startY;
          if (Math.abs(deltaX) > 50 && Math.abs(deltaX) > Math.abs(deltaY) * 1.5) {{
            if (deltaX < 0) this.next();
            else this.prev();
          }}
        }}, {{ passive: true }});
      }}

      setupWheelNav() {{
        window.addEventListener('wheel', (e) => {{
          if (this.isWheelThrottled) return;
          if (document.activeElement && document.activeElement.isContentEditable) return;
          if (Math.abs(e.deltaY) > 30) {{
            this.isWheelThrottled = true;
            if (e.deltaY > 0) this.next();
            else this.prev();
            setTimeout(() => {{ this.isWheelThrottled = false; }}, 400);
          }}
        }}, {{ passive: true }});
      }}

      setupControls() {{
        const prevBtn = document.getElementById('btnPrev');
        const nextBtn = document.getElementById('btnNext');
        const fsBtn = document.getElementById('btnFullscreen');
        if (prevBtn) prevBtn.addEventListener('click', () => this.prev());
        if (nextBtn) nextBtn.addEventListener('click', () => this.next());
        if (fsBtn) fsBtn.addEventListener('click', () => {{
          if (!document.fullscreenElement) {{
            document.documentElement.requestFullscreen().catch(() => {{}});
          }} else {{
            document.exitFullscreen().catch(() => {{}});
          }}
        }});
      }}
    }}

    /* ===========================================
       INLINE EDITING SYSTEM
       =========================================== */
    class InlineEditor {{
      constructor() {{
        this.isActive = false;
        this.storageKey = 'alandas_deck_edits_v2';
        this.editableSelectors = 'h1, h2, h3, p, li, .stat-number, .stat-label, .stat-sub, .card-tag, .badge, th, td, .kicker, .footer-meta';
        this.setupElements();
        this.restoreEdits();
        this.setupEvents();
      }}

      setupElements() {{
        this.hotzone = document.querySelector('.edit-hotzone');
        this.toggleBtn = document.getElementById('editToggle');
        this.banner = document.getElementById('editBanner');
        this.hideTimeout = null;
      }}

      setupEvents() {{
        // 1. Click toggle button
        if (this.toggleBtn) {{
          this.toggleBtn.addEventListener('click', () => this.toggleEditMode());
        }}

        // 2. Hotzone hover with 400ms grace period
        if (this.hotzone && this.toggleBtn) {{
          this.hotzone.addEventListener('mouseenter', () => {{
            clearTimeout(this.hideTimeout);
            this.toggleBtn.classList.add('show');
          }});
          this.hotzone.addEventListener('mouseleave', () => {{
            this.hideTimeout = setTimeout(() => {{
              if (!this.isActive) this.toggleBtn.classList.remove('show');
            }}, 400);
          }});
          this.toggleBtn.addEventListener('mouseenter', () => {{
            clearTimeout(this.hideTimeout);
          }});
          this.toggleBtn.addEventListener('mouseleave', () => {{
            this.hideTimeout = setTimeout(() => {{
              if (!this.isActive) this.toggleBtn.classList.remove('show');
            }}, 400);
          }});

          // 3. Hotzone direct click
          this.hotzone.addEventListener('click', () => this.toggleEditMode());
        }}

        // 4. Keyboard shortcut: 'E' key
        document.addEventListener('keydown', (e) => {{
          if ((e.key === 'e' || e.key === 'E') && !e.target.isContentEditable) {{
            e.preventDefault();
            this.toggleEditMode();
          }}
          // Ctrl+S / Cmd+S to explicitly save
          if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {{
            if (this.isActive) {{
              e.preventDefault();
              this.saveEdits();
              this.showSaveToast('Changes saved to LocalStorage!');
            }}
          }}
        }});

        // Auto-save on typing inside stage
        const stage = document.getElementById('deckStage');
        if (stage) {{
          stage.addEventListener('input', (e) => {{
            if (this.isActive && e.target.isContentEditable) {{
              this.saveEdits();
            }}
          }});
        }}

        // Reset button
        const resetBtn = document.getElementById('btnResetEdits');
        if (resetBtn) {{
          resetBtn.addEventListener('click', () => {{
            if (confirm('Reset all inline edits back to original content?')) {{
              localStorage.removeItem(this.storageKey);
              location.reload();
            }}
          }});
        }}
      }}

      toggleEditMode() {{
        this.isActive = !this.isActive;
        if (this.toggleBtn) {{
          this.toggleBtn.classList.toggle('active', this.isActive);
          this.toggleBtn.classList.toggle('show', this.isActive);
        }}
        if (this.banner) {{
          this.banner.classList.toggle('active', this.isActive);
        }}

        const elements = document.querySelectorAll(this.editableSelectors);
        elements.forEach(el => {{
          if (el.closest('.deck-controls') || el.closest('.edit-banner')) return;
          el.contentEditable = this.isActive ? 'true' : 'false';
          el.classList.toggle('editable-active', this.isActive);
        }});

        if (this.isActive) {{
          this.showSaveToast('Edit mode enabled. Click any text to edit.');
        }} else {{
          this.saveEdits();
          this.showSaveToast('Edit mode disabled. All changes saved.');
        }}
      }}

      saveEdits() {{
        const edits = {{}};
        const elements = document.querySelectorAll(this.editableSelectors);
        elements.forEach((el, idx) => {{
          if (el.closest('.deck-controls') || el.closest('.edit-banner')) return;
          edits[idx] = el.innerHTML;
        }});
        try {{
          localStorage.setItem(this.storageKey, JSON.stringify(edits));
        }} catch (err) {{
          console.warn('Could not save to localStorage', err);
        }}
      }}

      restoreEdits() {{
        try {{
          const saved = localStorage.getItem(this.storageKey);
          if (!saved) return;
          const edits = JSON.parse(saved);
          const elements = document.querySelectorAll(this.editableSelectors);
          elements.forEach((el, idx) => {{
            if (el.closest('.deck-controls') || el.closest('.edit-banner')) return;
            if (edits[idx] !== undefined) {{
              el.innerHTML = edits[idx];
            }}
          }});
        }} catch (err) {{
          console.warn('Could not restore from localStorage', err);
        }}
      }}

      showSaveToast(msg) {{
        let toast = document.getElementById('editToast');
        if (!toast) {{
          toast = document.createElement('div');
          toast.id = 'editToast';
          toast.className = 'edit-toast';
          document.body.appendChild(toast);
        }}
        toast.textContent = msg;
        toast.classList.add('visible');
        setTimeout(() => {{
          toast.classList.remove('visible');
        }}, 2200);
      }}
    }}

    // Initialize Presentation & Inline Editor on DOM Load
    document.addEventListener('DOMContentLoaded', () => {{
      window.presentation = new SlidePresentation();
      window.editor = new InlineEditor();
    }});
  </script>
</body>
</html>
"""

    with open('Alandas_Master_Growth_System.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("Successfully wrote reworked Alandas_Master_Growth_System.html!")

if __name__ == '__main__':
    build_presentation()
