"""
generate_sidy_cheat_sheet.py
Generates the non-overwhelming, high-impact Executive Cheat Sheet Presentation for Sidy Sow.
Outputs:
1. Alandas_Sidy_Cheat_Sheet_Deck.html (Interactive 16:9 Presentation with large fonts & luxury styling)
2. Alandas_Sidy_Cheat_Sheet_Deck.pptx (Native 16:9 PowerPoint Presentation)
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_cheat_sheet_html(output_path, t1_svg, t2_svg, t3_svg, wf_svg):
    print("Generating Sidy Cheat Sheet HTML Presentation...")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alandas Tea Berlin — Sidy's Revenue Roadmap & Cheat Sheet</title>
  
  <!-- Google Fonts: Luxury Editorial & Clean Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    :root {{
      --stage-bg: #0C0F0C;
      --slide-bg: #F9F7F2;
      --slide-gradient: radial-gradient(1400px 900px at 50% 0%, #FFFFFF 0%, #F9F7F2 60%, #EDE7D8 100%);
      
      --font-display: 'Playfair Display', Georgia, serif;
      --font-body: 'Plus Jakarta Sans', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      --olive: #444C32;
      --olive-dark: #2A301E;
      --olive-light: #EEF2E8;
      --olive-border: #D1D9C5;

      --ochre: #C48737;
      --ochre-dark: #946221;
      --ochre-light: #FCF4E8;
      --ochre-border: #F0DFC2;

      --forest: #2F5339;
      --forest-dark: #1E3725;
      --forest-light: #EDF5EF;

      --text-main: #181916;
      --text-muted: #545148;
      --text-subtle: #848074;
      
      --card-bg: #FFFFFF;
      --card-alt: #F4EFE6;
      --border: #E2DDD0;
      
      --shadow-sm: 0 4px 16px rgba(24, 25, 22, 0.05);
      --shadow-md: 0 12px 32px rgba(24, 25, 22, 0.08);
      --shadow-lg: 0 24px 50px rgba(24, 25, 22, 0.12);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    html, body {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: var(--stage-bg);
      font-family: var(--font-body);
      color: var(--text-main);
      -webkit-font-smoothing: antialiased;
    }}

    /* 16:9 VIEWPORT STAGE */
    .deck-viewport {{
      position: fixed;
      inset: 0;
      overflow: hidden;
      background: var(--stage-bg);
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .deck-stage {{
      position: absolute;
      width: 1920px;
      height: 1080px;
      left: 50%;
      top: 50%;
      transform-origin: center center;
      background: var(--slide-bg);
      background-image: var(--slide-gradient);
      box-shadow: 0 0 100px rgba(0, 0, 0, 0.85);
      border-radius: 4px;
      overflow: hidden;
    }}

    .slide {{
      position: absolute;
      inset: 0;
      width: 1920px;
      height: 1080px;
      padding: 64px 84px 54px 84px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
      transition: opacity 0.4s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.4s;
    }}

    .slide.active {{
      opacity: 1;
      visibility: visible;
      pointer-events: auto;
      z-index: 2;
    }}

    /* TYPOGRAPHY — LARGE PRESENTATION SCALE */
    .slide-header {{
      margin-bottom: 20px;
    }}
    .kicker {{
      font-family: var(--font-mono);
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--olive);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .kicker::before {{
      content: "";
      display: inline-block;
      width: 24px;
      height: 3px;
      background: var(--olive);
      border-radius: 2px;
    }}
    .slide-title {{
      font-family: var(--font-display);
      font-size: 46px;
      font-weight: 700;
      line-height: 1.15;
      color: var(--text-main);
      letter-spacing: -0.01em;
      margin-bottom: 8px;
    }}
    .slide-subtitle {{
      font-size: 21px;
      line-height: 1.45;
      color: var(--text-muted);
      max-width: 1520px;
    }}

    /* FOOTER */
    .slide-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 16px;
      border-top: 1px solid var(--border);
      font-family: var(--font-mono);
      font-size: 14px;
      color: var(--text-subtle);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .footer-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      color: var(--olive-dark);
    }}

    /* LAYOUT GRIDS */
    .slide-body {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 0;
      margin: 10px 0 16px 0;
    }}

    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 30px;
      height: 100%;
    }}
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 26px;
      height: 100%;
    }}
    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 22px;
      height: 100%;
    }}

    /* CARDS */
    .card {{
      background: var(--card-bg);
      border: 1.5px solid var(--border);
      border-radius: 18px;
      padding: 32px 30px;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      box-shadow: var(--shadow-sm);
      position: relative;
    }}
    .card.accent-olive {{ border-top: 6px solid var(--olive); }}
    .card.accent-ochre {{ border-top: 6px solid var(--ochre); }}
    .card.accent-forest {{ border-top: 6px solid var(--forest); }}
    .card.highlight {{
      background: #FFFFFF;
      border: 2px solid var(--olive);
      box-shadow: var(--shadow-md);
    }}

    .card-tag {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-bottom: 10px;
      display: inline-block;
    }}
    .tag-olive {{ color: var(--olive); }}
    .tag-ochre {{ color: var(--ochre); }}
    .tag-forest {{ color: var(--forest); }}

    .card-title {{
      font-family: var(--font-display);
      font-size: 26px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 12px;
      line-height: 1.25;
    }}
    .card-desc {{
      font-size: 18px;
      line-height: 1.5;
      color: var(--text-muted);
      margin-bottom: 18px;
    }}

    /* BULLET LISTS — HIGH READABILITY */
    .bullet-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .bullet-list li {{
      position: relative;
      padding-left: 28px;
      font-size: 18.5px;
      line-height: 1.5;
      color: var(--text-main);
    }}
    .bullet-list li::before {{
      content: "•";
      position: absolute;
      left: 8px;
      top: -1px;
      color: var(--olive);
      font-size: 24px;
    }}
    .bullet-list.ochre li::before {{ color: var(--ochre); }}
    .bullet-list.forest li::before {{ color: var(--forest); }}

    /* STAT CALLOUT BADGES */
    .stat-badge {{
      display: inline-flex;
      align-items: baseline;
      gap: 6px;
      font-family: var(--font-mono);
      font-weight: 800;
      font-size: 32px;
      color: var(--olive-dark);
      margin: 8px 0;
    }}
    .stat-sub {{
      font-size: 15px;
      font-weight: 600;
      color: var(--text-muted);
    }}

    /* HIGHLIGHT BOX */
    .callout-box {{
      background: var(--card-alt);
      border: 1.5px solid var(--border);
      border-radius: 14px;
      padding: 20px 24px;
      margin-top: 16px;
      font-size: 17.5px;
      line-height: 1.5;
    }}

    /* TABLES */
    .table-container {{
      background: #FFFFFF;
      border: 1.5px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }}
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }}
    table.data-table th {{
      background: var(--olive);
      color: #FFFFFF;
      font-size: 17px;
      font-weight: 700;
      padding: 18px 24px;
      letter-spacing: 0.04em;
    }}
    table.data-table td {{
      padding: 18px 24px;
      font-size: 17.5px;
      border-bottom: 1px solid var(--border);
      color: var(--text-main);
      vertical-align: middle;
      line-height: 1.45;
    }}
    table.data-table tr:nth-child(even) td {{
      background: var(--card-alt);
    }}
    table.data-table tr:last-child td {{
      border-bottom: none;
    }}

    /* FLOWCHART VIEW TOGGLE & DRAWER */
    .flowchart-toggle-group {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: #FFFFFF;
      border: 1.5px solid var(--border);
      padding: 4px 6px;
      border-radius: 30px;
      box-shadow: var(--shadow-sm);
    }}
    .toggle-btn {{
      background: transparent;
      border: none;
      font-family: var(--font-body);
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .toggle-btn.active {{
      background: var(--olive);
      color: #FFFFFF;
    }}
    .toggle-btn.ochre.active {{
      background: var(--ochre);
      color: #FFFFFF;
    }}
    .toggle-btn.forest.active {{
      background: var(--forest);
      color: #FFFFFF;
    }}
    .toggle-btn.expand-btn {{
      background: var(--olive-light);
      color: var(--olive-dark);
      font-weight: 700;
      border: 1px solid var(--olive-border);
    }}
    .toggle-btn.link-btn {{
      color: var(--ochre-dark);
      font-weight: 700;
    }}

    .view-panel {{
      display: none;
      width: 100%;
      height: 100%;
    }}
    .view-panel.active {{
      display: flex;
      flex-direction: column;
      animation: panelFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    @keyframes panelFadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .flowchart-panel {{
      height: 100%;
      min-height: 0;
    }}
    .flowchart-canvas-wrapper {{
      background: #FFFFFF;
      border: 1.5px solid var(--border);
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      height: 100%;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }}
    .flowchart-canvas-toolbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 20px;
      background: #F7F5EE;
      border-bottom: 1px solid var(--border);
      flex-shrink: 0;
    }}
    .flowchart-title {{
      font-family: var(--font-mono);
      font-size: 13.5px;
      font-weight: 700;
      color: var(--olive-dark);
    }}
    .toolbar-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .tb-btn {{
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 5px 12px;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--text-main);
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s;
    }}
    .tb-btn:hover {{
      background: var(--olive-light);
      border-color: var(--olive-border);
      color: var(--olive-dark);
    }}
    .tb-btn.highlight {{
      background: var(--ochre-light);
      border-color: var(--ochre-border);
      color: var(--ochre-dark);
      font-weight: 700;
    }}

    .flowchart-scroll-box {{
      flex: 1;
      overflow-y: auto;
      overflow-x: auto;
      padding: 24px;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      background: radial-gradient(circle at 50% 50%, #FAF8F2 0%, #EDE8DC 100%);
    }}
    .svg-container {{
      background: #FFFFFF;
      border: 1px solid #D5CFC2;
      border-radius: 12px;
      box-shadow: 0 12px 36px rgba(0,0,0,0.08);
      transform-origin: top center;
      transition: transform 0.2s ease-out;
    }}
    .svg-container svg {{
      display: block;
      max-width: 100%;
      height: auto;
    }}

    /* MODAL */
    .flowchart-modal {{
      position: fixed;
      inset: 0;
      z-index: 9999;
      display: none;
      align-items: center;
      justify-content: center;
    }}
    .flowchart-modal.open {{ display: flex; }}
    .modal-backdrop {{
      position: absolute;
      inset: 0;
      background: rgba(12, 15, 12, 0.88);
      backdrop-filter: blur(10px);
    }}
    .modal-content {{
      position: relative;
      z-index: 10000;
      width: 94vw;
      height: 92vh;
      background: #181B16;
      border: 1.5px solid #3A3E35;
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 30px 80px rgba(0,0,0,0.8);
    }}
    .modal-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 24px;
      background: #1F231D;
      border-bottom: 1px solid #3A3E35;
    }}
    .modal-title {{
      font-family: var(--font-display);
      font-size: 20px;
      color: #FFF;
    }}
    .modal-controls {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .modal-ctrl-btn {{
      background: #282C25;
      color: #E8E6DF;
      border: 1px solid #3A3E35;
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .modal-ctrl-btn.highlight {{
      background: var(--ochre);
      color: #FFF;
      border-color: #9A6622;
      font-weight: 700;
    }}
    .modal-close-btn {{
      background: #3D2222;
      color: #F87171;
      border: 1px solid #7F1D1D;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      cursor: pointer;
      font-size: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .modal-body {{
      flex: 1;
      overflow: auto;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 32px;
      background: radial-gradient(circle at 50% 50%, #1F231D 0%, #121411 100%);
    }}
    .modal-svg-container {{
      background: #FFFFFF;
      border-radius: 14px;
      border: 2px solid #33382D;
      transform-origin: top center;
      transition: transform 0.2s ease-out;
    }}

    /* ON-SCREEN NAVIGATION BAR */
    .deck-nav {{
      position: fixed;
      bottom: 24px;
      right: 32px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(24, 25, 22, 0.88);
      backdrop-filter: blur(12px);
      padding: 8px 18px;
      border-radius: 40px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      z-index: 100;
      color: #FFF;
      font-family: var(--font-mono);
      font-size: 14px;
    }}
    .nav-btn {{
      background: transparent;
      border: none;
      color: #FFF;
      cursor: pointer;
      font-size: 18px;
      padding: 4px 8px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }}
    .nav-btn:hover {{ background: rgba(255, 255, 255, 0.2); }}
    .nav-link {{
      color: #E8E6DF;
      text-decoration: none;
      font-size: 13px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.1);
      margin-left: 6px;
    }}
    .nav-link:hover {{ background: var(--olive); color: #FFF; }}
  </style>
</head>
<body>

<div class="deck-viewport">
  <div class="deck-stage" id="stage">

    <!-- =================================================================== -->
    <!-- SLIDE 1: Title & Executive Summary -->
    <!-- =================================================================== -->
    <div class="slide active" data-slide="1">
      <div class="slide-header">
        <div class="kicker">Alandas Tea Berlin // Executive Cheat Sheet</div>
        <h1 class="slide-title" style="font-size: 58px; margin-top: 10px;">The Path from 25 to 100 Cafes</h1>
        <p class="slide-subtitle" style="font-size: 24px; max-width: 1400px; margin-top: 8px;">
          A plain-English roadmap for Sidy Sow: How we automate sales grunt work, protect your brand, scale recurring cafe orders, and get you back to being your own boss full-time.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-3">
          <div class="card accent-olive">
            <span class="card-tag tag-olive">1. The Goal</span>
            <h3 class="card-title">Freedom & Scale</h3>
            <p class="card-desc">Grow from 25 active cafes to 100 regular accounts across Germany, unlocking €15,000–€30,000/month recurring income.</p>
            <div class="callout-box" style="margin-top: auto; font-weight: 600; color: var(--olive-dark);">
              Result: Sidy quits the Swiss job permanently and runs Alandas 100% full-time.
            </div>
          </div>

          <div class="card accent-ochre highlight">
            <span class="card-tag tag-ochre">2. The Engine</span>
            <h3 class="card-title">The 24/7 Digital Assistant</h3>
            <p class="card-desc">Finds specialty brunch cafes, reaches decision-makers on WhatsApp, pitches the €19 sample box, and syncs invoices automatically.</p>
            <div class="callout-box" style="margin-top: auto; font-weight: 600; color: var(--ochre-dark);">
              Result: Saves 15+ hours of tedious manual copy-pasting every single week.
            </div>
          </div>

          <div class="card accent-forest">
            <span class="card-tag tag-forest">3. The 3 Tiers</span>
            <h3 class="card-title">Earned Complexity</h3>
            <p class="card-desc">No fragile spaceships on Day 1. We start with safe human-directed automation, add strict guardrails, and scale to full autonomy.</p>
            <div class="callout-box" style="margin-top: auto; font-weight: 600; color: var(--forest-dark);">
              Result: 100% brand safe. Sidy stays in total control of every message and euro.
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 01 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 2: The Big Picture: Why Are We Doing This? -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="2">
      <div class="slide-header">
        <div class="kicker">01 // The Big Picture</div>
        <h2 class="slide-title">Why Are We Doing This? Sidy's Reality vs. The Goal</h2>
        <p class="slide-subtitle">
          Sidy imports and blends world-class organic tea, matcha, and chai. The tea is loved by customers, but current operations demand too much manual time for too little predictable cashflow.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-2">
          <div class="card" style="border-top: 6px solid #D9534F;">
            <span class="card-tag" style="color: #D9534F;">Current Reality // The Founder's Trap</span>
            <h3 class="card-title">Why Sidy Is Stuck Working a Day Job</h3>
            <ul class="bullet-list">
              <li><strong>High Swiss Living Costs:</strong> Sidy moved to Switzerland where expenses are high; the tea business doesn't yet yield steady monthly cashflow.</li>
              <li><strong>Tired & Working for Others:</strong> Trapped in an exhausting job at a Norwegian firm: <em>"It's been a long walk... I'm tired. I want to become again my own boss."</em></li>
              <li><strong>25 Happy Accounts:</strong> He already has ~25 great cafes buying regularly, but customer acquisition is stalled due to lack of time.</li>
              <li><strong>Manual Friction:</strong> Sidy spends his evenings manually messaging cafes on Instagram and deciphering paper orders.</li>
            </ul>
          </div>

          <div class="card accent-olive highlight">
            <span class="card-tag tag-olive">The Target // The 100-Cafe Equation</span>
            <h3 class="card-title">What 100 Accounts Actually Unlocks</h3>
            <div class="stat-badge">100 CAFES <span class="stat-sub">@ €200–€350 / MONTH AVG ORDER</span></div>
            <ul class="bullet-list" style="margin-top: 10px;">
              <li><strong>€15,000 to €30,000 / Month:</strong> Predictable recurring wholesale tea orders month after month.</li>
              <li><strong>90%+ Gross Margin:</strong> Premium tea carries extraordinary margins when ordered in bulk and delivered directly.</li>
              <li><strong>Full-Time Freedom:</strong> Sidy hands in his notice in Switzerland, returns to Berlin as his own boss, and controls his destiny.</li>
              <li><strong>Zero Additional Headcount:</strong> Reaching 100 cafes without hiring expensive administrative staff.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 02 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 3: The 5 Bottlenecks Holding Alandas Back -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="3">
      <div class="slide-header">
        <div class="kicker">02 // Operational Diagnosis</div>
        <h2 class="slide-title">The 5 Bottlenecks Holding Alandas Back Today</h2>
        <p class="slide-subtitle">
          Before building any software, we diagnose the exact friction points stopping Alandas from growing from 25 to 100 cafes.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-3">
          <div class="card">
            <span class="card-tag tag-ochre">Bottleneck 01</span>
            <h3 class="card-title" style="font-size: 23px;">Manual Scraping Sucks Time</h3>
            <p class="card-desc">Searching Google Maps, digging for website owners, and tracking down phone numbers burns <strong>20+ hours a week</strong> of high-effort founder time.</p>
          </div>

          <div class="card">
            <span class="card-tag tag-ochre">Bottleneck 02</span>
            <h3 class="card-title" style="font-size: 23px;">Cafes Ignore Cold Emails</h3>
            <p class="card-desc">Baristas and cafe owners are on their feet serving coffee all morning. They don't check promotional emails—they run their entire business on <strong>WhatsApp</strong>.</p>
          </div>

          <div class="card">
            <span class="card-tag tag-ochre">Bottleneck 03</span>
            <h3 class="card-title" style="font-size: 23px;">Order Processing Is Messy</h3>
            <p class="card-desc">Cafes text Sidy photos of crumpled paper notes: <em>"Send 2kg Earl Grey, 1kg Chai."</em> Typing these into invoices by hand creates errors and eats evening hours.</p>
          </div>

          <div class="card">
            <span class="card-tag tag-ochre">Bottleneck 04</span>
            <h3 class="card-title" style="font-size: 23px;">Silent Cafe Churn</h3>
            <p class="card-desc">A cafe runs out of tea on Day 28. If Sidy doesn't text them on Day 25, they panic-buy generic supermarket tea in an emergency, and Alandas quietly loses the account.</p>
          </div>

          <div class="card" style="border-top: 6px solid #D9534F;">
            <span class="card-tag" style="color: #D9534F;">Bottleneck 05 // The Trauma</span>
            <h3 class="card-title" style="font-size: 23px;">Burned by Fragile AI (Hermes)</h3>
            <p class="card-desc">Sidy previously set up an AI bot called "Hermes". It crashed, lost its memory, wiped prompts and order data. <strong>He rightly refuses fragile low-code tools that break.</strong></p>
          </div>

          <div class="card accent-olive highlight">
            <span class="card-tag tag-olive">The Opportunity</span>
            <h3 class="card-title" style="font-size: 23px;">The Automated Remedy</h3>
            <p class="card-desc">Replace manual hustle and fragile bots with a <strong>durable, crash-resilient revenue machine</strong> backed by solid engineering standards.</p>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 03 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 4: What We Are Building -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="4">
      <div class="slide-header">
        <div class="kicker">03 // The Solution</div>
        <h2 class="slide-title">What We Are Building: Your 24/7 Digital Revenue Machine</h2>
        <p class="slide-subtitle">
          Think of it like hiring an unpaid, tireless digital sales and operations team that handles the tedious grunt work while Sidy retains total authority.
        </p>
      </div>

      <div class="slide-body">
        <div class="card" style="padding: 36px;">
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;">
            <div style="background: var(--card-alt); padding: 22px; border-radius: 14px; border-left: 5px solid var(--olive);">
              <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--olive);">STAGE 01 // DISCOVER</div>
              <h4 style="font-size: 21px; font-weight: 700; margin: 8px 0;">Finds Ideal Cafes</h4>
              <p style="font-size: 16px; color: var(--text-muted); line-height: 1.45;">Scans Google Maps & Instagram across Berlin, Munich, Hamburg, and Frankfurt for venues with &gt;30 seats and premium coffee.</p>
            </div>

            <div style="background: var(--card-alt); padding: 22px; border-radius: 14px; border-left: 5px solid var(--olive);">
              <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--olive);">STAGE 02 // ENRICH</div>
              <h4 style="font-size: 21px; font-weight: 700; margin: 8px 0;">Gets Direct WhatsApps</h4>
              <p style="font-size: 16px; color: var(--text-muted); line-height: 1.45;">Uses the German Impressum legal notice trick to find the owner's name and mobile number for almost zero cost.</p>
            </div>

            <div style="background: var(--card-alt); padding: 22px; border-radius: 14px; border-left: 5px solid var(--ochre);">
              <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--ochre-dark);">STAGE 03 // OFFER</div>
              <h4 style="font-size: 21px; font-weight: 700; margin: 8px 0;">Pitches €19 Teapot Kit</h4>
              <p style="font-size: 16px; color: var(--text-muted); line-height: 1.45;">Offers a heavy borosilicate cafe teapot + 4 top blends for €19 (100% credited back when they buy their first wholesale crate).</p>
            </div>

            <div style="background: var(--card-alt); padding: 22px; border-radius: 14px; border-left: 5px solid var(--ochre);">
              <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--ochre-dark);">STAGE 04 // 1-TAP APPROVE</div>
              <h4 style="font-size: 21px; font-weight: 700; margin: 8px 0;">Sidy Taps "Send"</h4>
              <p style="font-size: 16px; color: var(--text-muted); line-height: 1.45;">AI writes a personalized, warm WhatsApp message. Sidy glances at his phone and taps <strong>Approve</strong>. 100% brand safe.</p>
            </div>

            <div style="background: var(--card-alt); padding: 22px; border-radius: 14px; border-left: 5px solid var(--forest);">
              <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--forest);">STAGE 05 // INVOICE</div>
              <h4 style="font-size: 21px; font-weight: 700; margin: 8px 0;">OCR Reads Order Photos</h4>
              <p style="font-size: 16px; color: var(--text-muted); line-height: 1.45;">When a cafe texts a photo of a handwritten note, the system parses line items and creates a draft invoice in Dolibarr CRM.</p>
            </div>

            <div style="background: var(--card-alt); padding: 22px; border-radius: 14px; border-left: 5px solid var(--forest);">
              <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--forest);">STAGE 06 // RETENTION</div>
              <h4 style="font-size: 21px; font-weight: 700; margin: 8px 0;">Day-25 Refill Alerts</h4>
              <p style="font-size: 16px; color: var(--text-muted); line-height: 1.45;">Automated WhatsApp reminder on Day 25: <em>"Hey Marco, your Earl Grey is running low. Want me to send your usual refill?"</em></p>
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 04 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 5: Why Structure It in 3 Tiers? -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="5">
      <div class="slide-header">
        <div class="kicker">04 // Architectural Law</div>
        <h2 class="slide-title">Why 3 Tiers? "Don't Build a Spaceship on Day 1"</h2>
        <p class="slide-subtitle">
          The biggest mistake in AI automation is trying to make a machine fully autonomous on Day 1. That leads to hallucinations, blown budgets, and broken trust. We earn complexity tier by tier.
        </p>
      </div>

      <div class="slide-body">
        <div class="card" style="padding: 36px; height: 100%; justify-content: space-between;">
          <!-- 3-Tier Step Ladder -->
          <div style="display: flex; flex-direction: column; gap: 16px;">
            <!-- Tier 3 -->
            <div style="background: var(--forest-light); border: 2px solid var(--forest); border-radius: 14px; padding: 22px 28px; display: flex; align-items: center; justify-content: space-between;">
              <div style="display: flex; align-items: center; gap: 20px;">
                <span style="font-family: var(--font-mono); font-size: 16px; font-weight: 800; background: var(--forest); color: #FFF; padding: 6px 14px; border-radius: 6px;">TIER 3</span>
                <div>
                  <h4 style="font-size: 22px; font-weight: 700; color: var(--forest-dark);">Autonomous Revenue Platform (100+ Cafes)</h4>
                  <p style="font-size: 16px; color: var(--text-muted); margin-top: 4px;">The closed-loop commercial machine. Live cafe replenishment rates automatically trigger and optimize Meta Ad campaigns.</p>
                </div>
              </div>
              <span style="font-family: var(--font-mono); font-size: 14px; font-weight: 700; color: var(--forest);">EARNED AT SCALE</span>
            </div>

            <!-- Tier 2 -->
            <div style="background: var(--ochre-light); border: 2px solid var(--ochre); border-radius: 14px; padding: 22px 28px; display: flex; align-items: center; justify-content: space-between;">
              <div style="display: flex; align-items: center; gap: 20px;">
                <span style="font-family: var(--font-mono); font-size: 16px; font-weight: 800; background: var(--ochre); color: #FFF; padding: 6px 14px; border-radius: 6px;">TIER 2</span>
                <div>
                  <h4 style="font-size: 22px; font-weight: 700; color: var(--ochre-dark);">Governed Intelligence (40–70 Cafes)</h4>
                  <p style="font-size: 16px; color: var(--text-muted); margin-top: 4px;">The smart assistant with financial guardrails. Policy engines verify ad budgets, wholesale discounts, and prices before execution.</p>
                </div>
              </div>
              <span style="font-family: var(--font-mono); font-size: 14px; font-weight: 700; color: var(--ochre-dark);">EARNED AFTER PROVING TIER 1</span>
            </div>

            <!-- Tier 1 -->
            <div style="background: var(--olive-light); border: 2.5px solid var(--olive); border-radius: 14px; padding: 22px 28px; display: flex; align-items: center; justify-content: space-between; box-shadow: var(--shadow-sm);">
              <div style="display: flex; align-items: center; gap: 20px;">
                <span style="font-family: var(--font-mono); font-size: 16px; font-weight: 800; background: var(--olive); color: #FFF; padding: 6px 14px; border-radius: 6px;">TIER 1</span>
                <div>
                  <h4 style="font-size: 22px; font-weight: 700; color: var(--olive-dark);">Essential Automation (25–40 Cafes) — START HERE</h4>
                  <p style="font-size: 16px; color: var(--text-muted); margin-top: 4px;">The tireless grunt worker. Machine handles prospecting, enrichment, and invoice drafting; Sidy retains 100% approval authority.</p>
                </div>
              </div>
              <span style="font-family: var(--font-mono); font-size: 14px; font-weight: 800; color: var(--olive);">START TODAY (ZERO RISK)</span>
            </div>
          </div>

          <div class="callout-box" style="margin-top: 14px; display: flex; align-items: center; justify-content: space-between;">
            <div><strong>The Governing Rule:</strong> You do not pay for complexity until business volume justifies it. Each tier builds cleanly on top of the last without throwing away a single line of code.</div>
            <a href="excalidraw_canvas_viewer.html" target="_blank" class="toggle-btn link-btn" style="white-space:nowrap; margin-left:20px;">Open Canvas Viewer ↗</a>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 05 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 6: Tier 1 in Plain English -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="6">
      <div class="slide-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div class="kicker">Tier 1 Deep Dive // Human-Directed</div>
            <h2 class="slide-title">Tier 1: "The Tireless Assistant" (Sidy is Pilot)</h2>
            <p class="slide-subtitle">
              Sidy is in 100% control. The machine gathers facts and proposes actions; Sidy taps Approve before anything happens.
            </p>
          </div>
          <div class="flowchart-toggle-group">
            <button class="toggle-btn active" onclick="setSlideView(6, 'cards')">Executive View</button>
            <button class="toggle-btn" onclick="setSlideView(6, 'flowchart')">⚡ View Flowchart</button>
            <button class="toggle-btn expand-btn" onclick="openFlowchartModal('tier1')">⛶ Fullscreen</button>
          </div>
        </div>
      </div>

      <div class="slide-body">
        <!-- View 1: Executive Cards -->
        <div id="slide-6-cards" class="view-panel active">
          <div class="grid-2">
            <div class="card accent-olive">
              <span class="card-tag tag-olive">How the 5 Steps Work</span>
              <h3 class="card-title">Read ➔ Analyze ➔ Propose ➔ Approve ➔ Execute</h3>
              <ol style="display: flex; flex-direction: column; gap: 14px; padding-left: 22px; font-size: 17.5px; line-height: 1.45; color: var(--text-main);">
                <li><strong>Read:</strong> Scans Google Maps / Instagram for cafes with &gt;30 seats.</li>
                <li><strong>Analyze:</strong> Scores beverage menu, seating, and specialty coffee focus.</li>
                <li><strong>Propose:</strong> Drafts personalized WhatsApp message pitching the €19 teapot kit.</li>
                <li><strong>Human Approves (The Safety Gate):</strong> Message lands on Sidy's WhatsApp. Sidy taps <strong>Approve</strong>. Bot never sends unreviewed messages.</li>
                <li><strong>Execute:</strong> Dispatches message, creates Dolibarr card, and sets Day-4 follow-up.</li>
              </ol>
            </div>

            <div class="card highlight">
              <span class="card-tag tag-olive">Commercial Value for Sidy</span>
              <h3 class="card-title">What Sidy Experiences</h3>
              <ul class="bullet-list">
                <li><strong>Zero Brand Risk:</strong> It is impossible for an AI to hallucinate, insult a chef, or make illegal health claims. Sidy sees everything first.</li>
                <li><strong>Saves 15+ Hours/Week:</strong> Sidy stops doing repetitive internet searches and address typing late at night.</li>
                <li><strong>Target:</strong> Scales Alandas from <strong>25 to 40 accounts</strong>, generating <strong>~€5,000/month</strong> in steady wholesale revenue.</li>
                <li><strong>Durable:</strong> Built with Temporal so power outages or server reboots never lose a single lead or order.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- View 2: Flowchart Preview -->
        <div id="slide-6-flowchart" class="view-panel flowchart-panel">
          <div class="flowchart-canvas-wrapper">
            <div class="flowchart-canvas-toolbar">
              <span class="flowchart-title">Tier 1 State Machine (Google Maps ➔ Dedup ➔ §5 TMG ➔ Agent 1 ➔ Sidy WhatsApp ➔ Dolibarr)</span>
              <div class="toolbar-actions">
                <button class="tb-btn highlight" onclick="openFlowchartModal('tier1')">⛶ Expand Fullscreen</button>
                <a href="tier1_essential_automation_flowchart.excalidraw" download class="tb-btn">Download .excalidraw</a>
              </div>
            </div>
            <div class="flowchart-scroll-box" id="flowchart-box-6">
              <div class="svg-container" id="svg-wrap-6">
{t1_svg}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 06 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 7: Tier 2 in Plain English -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="7">
      <div class="slide-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div class="kicker">Tier 2 Deep Dive // Governed Intelligence</div>
            <h2 class="slide-title">Tier 2: "The Smart Assistant with Guardrails"</h2>
            <p class="slide-subtitle">
              As volume grows, the machine suggests smart business moves, but unbreakable safety rules prevent it from ever burning cash or making mistakes.
            </p>
          </div>
          <div class="flowchart-toggle-group">
            <button class="toggle-btn ochre active" onclick="setSlideView(7, 'cards')">Executive View</button>
            <button class="toggle-btn ochre" onclick="setSlideView(7, 'flowchart')">⚡ View Flowchart</button>
            <button class="toggle-btn expand-btn" onclick="openFlowchartModal('tier2')">⛶ Fullscreen</button>
          </div>
        </div>
      </div>

      <div class="slide-body">
        <!-- View 1: Executive Cards -->
        <div id="slide-7-cards" class="view-panel active">
          <div class="grid-2">
            <div class="card accent-ochre">
              <span class="card-tag tag-ochre">The Real-World Example</span>
              <h3 class="card-title">Increasing Meta Ad Budget by +30%</h3>
              <p class="card-desc">How the Policy Engine protects Sidy's money:</p>
              <ol style="display: flex; flex-direction: column; gap: 12px; padding-left: 22px; font-size: 17px; line-height: 1.45; color: var(--text-main);">
                <li><strong>AI Observes:</strong> Berlin brunch ad has a 4.2x ROAS. AI recommends raising budget from €30 to €39/day (+€9).</li>
                <li><strong>Policy Check 1 (Ceiling):</strong> Is €39 under our maximum €50/day cap? (YES).</li>
                <li><strong>Policy Check 2 (Threshold):</strong> Is the delta (&gt;€5) requiring human sign-off? (YES).</li>
                <li><strong>Sidy Notified:</strong> Phone dings: <em>[Approve +€9/day for Berlin Brunch Ad?]</em>.</li>
                <li><strong>Verify State:</strong> AI calls Meta API, then re-queries Meta to confirm it is €39.00 and NOT €390.00.</li>
              </ol>
            </div>

            <div class="card highlight">
              <span class="card-tag tag-ochre">Commercial Value for Sidy</span>
              <h3 class="card-title">Why Tier 2 Commands Premium Pricing</h3>
              <ul class="bullet-list ochre">
                <li><strong>Zero Runaway Spend:</strong> Mathematically impossible for an AI glitch or bug to drain Sidy's bank account or ad credit.</li>
                <li><strong>Zero Pricing Leaks:</strong> B2B volume wholesale discounts follow strict math tables, not model hallucinations.</li>
                <li><strong>Automated Day-25 Refills:</strong> Automatically reminds cafes when their tea tins are low, stopping quiet churn in its tracks.</li>
                <li><strong>Target:</strong> Scales Alandas from <strong>40 to 70 accounts</strong>, generating <strong>~€12,000/month</strong> in recurring revenue.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- View 2: Flowchart Preview -->
        <div id="slide-7-flowchart" class="view-panel flowchart-panel">
          <div class="flowchart-canvas-wrapper">
            <div class="flowchart-canvas-toolbar">
              <span class="flowchart-title">Tier 2 Governed Decision Flow (Ad Telemetry ➔ Contract ➔ Policy Gate ➔ Meta Dispatch ➔ Audit)</span>
              <div class="toolbar-actions">
                <button class="tb-btn highlight" onclick="openFlowchartModal('tier2')">⛶ Expand Fullscreen</button>
                <a href="tier2_governed_intelligence_flowchart.excalidraw" download class="tb-btn">Download .excalidraw</a>
              </div>
            </div>
            <div class="flowchart-scroll-box" id="flowchart-box-7">
              <div class="svg-container" id="svg-wrap-7">
{t2_svg}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 07 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 8: Tier 3 in Plain English -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="8">
      <div class="slide-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div class="kicker">Tier 3 Deep Dive // Autonomous Operations</div>
            <h2 class="slide-title">Tier 3: "The Self-Running Business Machine"</h2>
            <p class="slide-subtitle">
              At 100+ accounts, Alandas operates like a multi-million-euro beverage brand with zero extra office staff. Sales data trains marketing automatically.
            </p>
          </div>
          <div class="flowchart-toggle-group">
            <button class="toggle-btn forest active" onclick="setSlideView(8, 'cards')">Executive View</button>
            <button class="toggle-btn forest" onclick="setSlideView(8, 'flowchart')">⚡ View Flowchart</button>
            <button class="toggle-btn expand-btn" onclick="openFlowchartModal('tier3')">⛶ Fullscreen</button>
          </div>
        </div>
      </div>

      <div class="slide-body">
        <!-- View 1: Executive Cards -->
        <div id="slide-8-cards" class="view-panel active">
          <div class="grid-2">
            <div class="card accent-forest">
              <span class="card-tag tag-forest">The Closed-Loop Flywheel</span>
              <h3 class="card-title">Real-World Munich Summer Scenario</h3>
              <p class="card-desc">How departments talk to each other without human friction:</p>
              <ul class="bullet-list forest">
                <li><strong>Reorder Surge:</strong> In July, Munich cafes reorder Earl Grey and Berry Hibiscus 2x faster than normal for outdoor cold brew.</li>
                <li><strong>Operations Alerts Marketing:</strong> The system identifies that terrace iced tea is surging in Munich.</li>
                <li><strong>Automated Campaign:</strong> Marketing Agent writes new ad copy: <em>"Serving iced tea on your Munich terrace? Get our €19 barista kit."</em></li>
                <li><strong>Autonomous Optimization:</strong> Launches small tests, validates conversion, and allocates budget without Sidy lifting a finger.</li>
              </ul>
            </div>

            <div class="card highlight">
              <span class="card-tag tag-forest">Commercial Value for Sidy</span>
              <h3 class="card-title">Total Founder Independence</h3>
              <ul class="bullet-list forest">
                <li><strong>Zero Linear Headcount:</strong> Scales across Germany, Austria, and Switzerland without hiring secretaries or sales reps.</li>
                <li><strong>Automated Circuit Breakers:</strong> Any anomaly (supplier delay, payment hiccup) halts operations instantly and alerts Sidy.</li>
                <li><strong>Sidy Acts as Chairman:</strong> Sidy reviews a weekly digest while sipping tea, rather than grinding on phone calls.</li>
                <li><strong>Target:</strong> <strong>100+ active accounts, €20,000–€30,000/month recurring income. Sidy is 100% his own boss.</strong></li>
              </ul>
            </div>
          </div>
        </div>

        <!-- View 2: Flowchart Preview -->
        <div id="slide-8-flowchart" class="view-panel flowchart-panel">
          <div class="flowchart-canvas-wrapper">
            <div class="flowchart-canvas-toolbar">
              <span class="flowchart-title">Tier 3 Flywheel (Event Stream ➔ Shared Revenue State ➔ Specialist Agents ➔ MCP ➔ Multi-City)</span>
              <div class="toolbar-actions">
                <button class="tb-btn highlight" onclick="openFlowchartModal('tier3')">⛶ Expand Fullscreen</button>
                <a href="tier3_autonomous_platform_flowchart.excalidraw" download class="tb-btn">Download .excalidraw</a>
              </div>
            </div>
            <div class="flowchart-scroll-box" id="flowchart-box-8">
              <div class="svg-container" id="svg-wrap-8">
{t3_svg}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 08 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 9: The 3 Technical Secret Weapons -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="9">
      <div class="slide-header">
        <div class="kicker">05 // Technical Defense Made Simple</div>
        <h2 class="slide-title">The 3 Technical "Secret Weapons" (In Plain English)</h2>
        <p class="slide-subtitle">
          When explaining the tech to Sidy or investors, use these three simple metaphors instead of confusing acronyms.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-3">
          <div class="card accent-olive">
            <span class="card-tag tag-olive">Secret Weapon 01</span>
            <h3 class="card-title">Temporal vs. n8n</h3>
            <div style="font-size: 16px; font-weight: 700; color: var(--olive); margin-bottom: 8px;">"Carving in Stone vs. Sticky Notes"</div>
            <p style="font-size: 17.5px; line-height: 1.5; color: var(--text-muted);">
              <strong>n8n</strong> writes orders on sticky notes. When the server crashes, notes blow away and data is lost (why Hermes died).<br><br>
              <strong>Temporal</strong> carves every step into solid rock. If the power dies or an API crashes for 3 hours, it resumes at the exact line of code when restored. Zero lost orders.
            </p>
          </div>

          <div class="card accent-ochre">
            <span class="card-tag tag-ochre">Secret Weapon 02</span>
            <h3 class="card-title">German Impressum Waterfall</h3>
            <div style="font-size: 16px; font-weight: 700; color: var(--ochre-dark); margin-bottom: 8px;">"Cheapest Tool First (87% Savings)"</div>
            <p style="font-size: 17.5px; line-height: 1.5; color: var(--text-muted);">
              Normal agencies waste €80 looking up 1,000 leads.<br><br>
              In Germany, § 5 TMG requires all business sites to publish owner names & emails for free. Our custom scraper grabs <strong>48% of leads for €0.00</strong>. We only use paid tools for the few missed leads. Total cost: €10 instead of €80.
            </p>
          </div>

          <div class="card accent-forest">
            <span class="card-tag tag-forest">Secret Weapon 03</span>
            <h3 class="card-title">The Policy Engine Bouncer</h3>
            <div style="font-size: 16px; font-weight: 700; color: var(--forest); margin-bottom: 8px;">"The Guardrail at the Bank Vault"</div>
            <p style="font-size: 17.5px; line-height: 1.5; color: var(--text-muted);">
              No AI is ever handed Sidy's credit card or pricing authority.<br><br>
              The AI must write a typed proposal (Decision Contract). The bouncer (Policy Engine) checks: <em>Is discount allowed? Is budget safe?</em> If unusual, it rings Sidy's phone for 1-tap confirmation.
            </p>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 09 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 10: Sidy's 12-Month Roadmap to Freedom -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="10">
      <div class="slide-header">
        <div class="kicker">06 // Financial & Personal Roadmap</div>
        <h2 class="slide-title">Sidy's 12-Month Roadmap to Freedom</h2>
        <p class="slide-subtitle">
          How Cyril and Sidy execute this strategy step by step: from surviving in Switzerland to building a full-time €25k/month tea enterprise.
        </p>
      </div>

      <div class="slide-body">
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th style="width: 20%;">Phase & Timeline</th>
                <th style="width: 32%;">What We Build & Launch</th>
                <th style="width: 26%;">Sidy's Daily Reality</th>
                <th style="width: 22%;">Target Account & Revenue</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Months 1–3</strong><br><span style="font-size: 14px; color: var(--olive); font-weight: 700;">Tier 1: Essential</span></td>
                <td>Stabilize Dolibarr CRM with daily cloud backups, automate German cafe scraping, deploy WhatsApp OCR order parser, standardize €19 teapot discovery kit.</td>
                <td>Still works Swiss job, but spends just <strong>30 mins/day</strong> reviewing qualified cafe outreach drafts on WhatsApp.</td>
                <td><strong style="color: var(--olive);">25 ➔ 40 Cafes</strong><br>~€5,000 / month</td>
              </tr>
              <tr>
                <td><strong>Months 4–6</strong><br><span style="font-size: 14px; color: var(--ochre-dark); font-weight: 700;">Tier 2: Governed</span></td>
                <td>Deploy Policy Engine for Meta Ads (+30% rule), automate Day-25 predictive refill alerts on WhatsApp, implement structured audit logging.</td>
                <td>Admin time drops to <strong>&lt; 4 hours/week</strong>. Cafes reorder on clockwork. Sidy sees the finish line of his day job.</td>
                <td><strong style="color: var(--ochre-dark);">40 ➔ 70 Cafes</strong><br>~€12,000 / month</td>
              </tr>
              <tr>
                <td><strong>Months 7–12</strong><br><span style="font-size: 14px; color: var(--forest); font-weight: 700;">Tier 3: Platform</span></td>
                <td>Turn on closed-loop flywheel connecting cafe reorders to Meta ad creative, coordinate multi-city accounts across Germany, Austria & Switzerland.</td>
                <td><strong>Sidy hands in his notice at the Swiss firm.</strong> Returns to Berlin as 100% full-time independent founder & CEO.</td>
                <td><strong style="color: var(--forest);">100+ Cafes</strong><br>€20,000–€30,000 / month</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 10 / 11</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 11: Starting Sprint 1 Today -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="11">
      <div class="slide-header">
        <div class="kicker">07 // Immediate Next Steps</div>
        <h2 class="slide-title">Starting Sprint 1 Today: The First 4 Concrete Steps</h2>
        <p class="slide-subtitle">
          We don't need months of preparation. We can initiate the Tier 1 foundation immediately with 4 clear deliverables.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-4">
          <div class="card accent-olive highlight">
            <span class="card-tag tag-olive">Step 01</span>
            <h4 class="card-title" style="font-size: 22px;">Stabilize Dolibarr CRM</h4>
            <p class="card-desc" style="font-size: 16.5px;">Set up automated daily cloud database backups and clean existing 25 cafe customer records so data is never lost again.</p>
          </div>

          <div class="card accent-olive">
            <span class="card-tag tag-olive">Step 02</span>
            <h4 class="card-title" style="font-size: 22px;">Standardize €19 Trial Kit</h4>
            <p class="card-desc" style="font-size: 16.5px;">Package the shatter-resistant borosilicate glass teapot with 4 signature blends and 100% wholesale credit voucher.</p>
          </div>

          <div class="card accent-olive">
            <span class="card-tag tag-olive">Step 03</span>
            <h4 class="card-title" style="font-size: 22px;">Run § 5 TMG Scraper</h4>
            <p class="card-desc" style="font-size: 16.5px;">Extract 200 high-potential brunch cafes in Berlin & Munich for €0.00 using the legal Impressum waterfall scraper.</p>
          </div>

          <div class="card accent-olive">
            <span class="card-tag tag-olive">Step 04</span>
            <h4 class="card-title" style="font-size: 22px;">1-Tap WhatsApp Pilot</h4>
            <p class="card-desc" style="font-size: 16.5px;">Send Sidy the first batch of 10 AI-drafted trial kit outreach messages on WhatsApp for 1-tap review and dispatch.</p>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  EXECUTIVE CHEAT SHEET</div>
        <div>SLIDE 11 / 11</div>
      </div>
    </div>

  </div> <!-- /deck-stage -->
</div> <!-- /deck-viewport -->

<!-- ON-SCREEN NAVIGATION CONTROLS -->
<div class="deck-nav">
  <button class="nav-btn" id="prevBtn" title="Previous Slide (←)">◀</button>
  <span id="slideCounter" style="margin: 0 4px; font-weight: 700;">1 / 11</span>
  <button class="nav-btn" id="nextBtn" title="Next Slide (→)">▶</button>
  <a href="excalidraw_canvas_viewer.html" target="_blank" class="nav-link" title="Open Multi-Tab Excalidraw Canvas Viewer">📐 Architecture Canvas</a>
</div>

<!-- FULLSCREEN FLOWCHART MODAL -->
<div id="flowchartModal" class="flowchart-modal">
  <div class="modal-backdrop" onclick="closeFlowchartModal()"></div>
  <div class="modal-content">
    <div class="modal-header">
      <div>
        <h3 id="modalTitle" class="modal-title">Flowchart Title</h3>
      </div>
      <div class="modal-controls">
        <button class="modal-ctrl-btn" onclick="zoomModal(1.25)">Zoom In (+)</button>
        <button class="modal-ctrl-btn" onclick="zoomModal(0.8)">Zoom Out (-)</button>
        <button class="modal-ctrl-btn" onclick="resetModalZoom()">Reset (↺)</button>
        <a id="modalDownloadBtn" href="#" download class="modal-ctrl-btn highlight">Download .excalidraw</a>
        <a id="modalExternalBtn" href="excalidraw_canvas_viewer.html" target="_blank" class="modal-ctrl-btn">Canvas Viewer ↗</a>
        <button class="modal-close-btn" onclick="closeFlowchartModal()" title="Close (Esc)">✕</button>
      </div>
    </div>
    <div class="modal-body" id="modalScrollBody">
      <div id="modalSvgContainer" class="modal-svg-container"></div>
    </div>
  </div>
</div>

<script>
  (function() {{
    const stage = document.getElementById('stage');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const slideCounter = document.getElementById('slideCounter');
    
    let currentSlide = 0;
    const totalSlides = slides.length;

    // 16:9 Scale to Fit Viewport
    function scaleStage() {{
      const designWidth = 1920;
      const designHeight = 1080;
      const windowWidth = window.innerWidth;
      const windowHeight = window.innerHeight;

      const scaleX = windowWidth / designWidth;
      const scaleY = windowHeight / designHeight;
      const scale = Math.min(scaleX, scaleY);

      stage.style.transform = `translate(-50%, -50%) scale(${{scale}})`;
    }}

    window.addEventListener('resize', scaleStage);
    scaleStage();

    function showSlide(index) {{
      if (index < 0) index = 0;
      if (index >= totalSlides) index = totalSlides - 1;
      
      slides[currentSlide].classList.remove('active');
      currentSlide = index;
      slides[currentSlide].classList.add('active');

      slideCounter.textContent = `${{currentSlide + 1}} / ${{totalSlides}}`;
    }}

    prevBtn.addEventListener('click', () => showSlide(currentSlide - 1));
    nextBtn.addEventListener('click', () => showSlide(currentSlide + 1));

    window.addEventListener('keydown', (e) => {{
      const modal = document.getElementById('flowchartModal');
      if (e.key === 'Escape' && modal && modal.classList.contains('open')) {{
        closeFlowchartModal();
        return;
      }}
      if (modal && modal.classList.contains('open')) return;

      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        e.preventDefault();
        showSlide(currentSlide + 1);
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        e.preventDefault();
        showSlide(currentSlide - 1);
      }} else if (e.key === 'Home') {{
        e.preventDefault();
        showSlide(0);
      }} else if (e.key === 'End') {{
        e.preventDefault();
        showSlide(totalSlides - 1);
      }}
    }});

    // Slide View Switcher
    window.setSlideView = function(slideNum, viewType) {{
      const cardsPanel = document.getElementById(`slide-${{slideNum}}-cards`);
      const flowPanel = document.getElementById(`slide-${{slideNum}}-flowchart`);
      const slideElem = document.querySelector(`.slide[data-slide="${{slideNum}}"]`);
      if (!slideElem) return;
      const btns = slideElem.querySelectorAll('.flowchart-toggle-group .toggle-btn:not(.expand-btn):not(.link-btn)');

      if (viewType === 'cards') {{
        if (cardsPanel) cardsPanel.classList.add('active');
        if (flowPanel) flowPanel.classList.remove('active');
        if (btns[0]) btns[0].classList.add('active');
        if (btns[1]) btns[1].classList.remove('active');
      }} else {{
        if (cardsPanel) cardsPanel.classList.remove('active');
        if (flowPanel) flowPanel.classList.add('active');
        if (btns[0]) btns[0].classList.remove('active');
        if (btns[1]) btns[1].classList.add('active');
      }}
    }};

    // Fullscreen Modal Controller
    let modalZoom = 1;
    const flowchartData = {{
      tier1: {{
        title: "Tier 1: Essential Revenue Automation Flowchart (2,275px Full Vision)",
        download: "tier1_essential_automation_flowchart.excalidraw",
        svgId: "svg-wrap-6"
      }},
      tier2: {{
        title: "Tier 2: Governed Decision Flow & Decision Contract Gate",
        download: "tier2_governed_intelligence_flowchart.excalidraw",
        svgId: "svg-wrap-7"
      }},
      tier3: {{
        title: "Tier 3: Autonomous Revenue Platform Flowchart (Closed-Loop Flywheel)",
        download: "tier3_autonomous_platform_flowchart.excalidraw",
        svgId: "svg-wrap-8"
      }}
    }};

    window.openFlowchartModal = function(key) {{
      const data = flowchartData[key];
      if (!data) return;
      const modal = document.getElementById('flowchartModal');
      const title = document.getElementById('modalTitle');
      const dlBtn = document.getElementById('modalDownloadBtn');
      const container = document.getElementById('modalSvgContainer');

      if (title) title.textContent = data.title;
      if (dlBtn) dlBtn.href = data.download;
      const sourceSvg = document.getElementById(data.svgId);
      if (sourceSvg && container) {{
        container.innerHTML = sourceSvg.innerHTML;
      }}
      modalZoom = 1;
      if (container) container.style.transform = "scale(1)";
      if (modal) modal.classList.add('open');
    }};

    window.closeFlowchartModal = function() {{
      const modal = document.getElementById('flowchartModal');
      if (modal) modal.classList.remove('open');
    }};

    window.zoomModal = function(factor) {{
      modalZoom = Math.min(3.0, Math.max(0.3, modalZoom * factor));
      const container = document.getElementById('modalSvgContainer');
      if (container) container.style.transform = `scale(${{modalZoom}})`;
    }};

    window.resetModalZoom = function() {{
      modalZoom = 1;
      const container = document.getElementById('modalSvgContainer');
      if (container) container.style.transform = "scale(1)";
    }};
  }})();
</script>

</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[SUCCESS] Cheat Sheet HTML presentation generated: {output_path}")


def build_cheat_sheet_pptx(output_path):
    print("Generating Sidy Cheat Sheet PowerPoint Presentation...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    COLOR_BG = RGBColor(0xF9, 0xF7, 0xF2)
    COLOR_TEXT_MAIN = RGBColor(0x18, 0x19, 0x16)
    COLOR_TEXT_MUTED = RGBColor(0x54, 0x51, 0x48)
    COLOR_OLIVE = RGBColor(0x44, 0x4C, 0x32)
    COLOR_OCHRE = RGBColor(0xC4, 0x87, 0x37)
    COLOR_FOREST = RGBColor(0x2F, 0x53, 0x39)
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
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = kicker.upper()
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE
        p0.space_after = Pt(3)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(3)

        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.name = FONT_BODY
            p2.font.size = Pt(13)
            p2.font.color.rgb = COLOR_TEXT_MUTED

    def add_footer(slide, curr, total=11):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
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

    def add_formatted_card(slide, left, top, width, height, tag, title, bullets, tag_color=COLOR_OLIVE, bg_color=COLOR_CARD_BG, title_size=18, bullet_size=12.5):
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
        p0.space_after = Pt(3)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(title_size)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(8)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(bullet_size)
            pb.font.color.rgb = COLOR_TEXT_MUTED
            pb.space_after = Pt(6)

    # -------------------------------------------------------------
    # Slide 1: Title
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    create_card(s1, Inches(0.8), Inches(0.75), Inches(11.733), Inches(6.0))
    tb = s1.shapes.add_textbox(Inches(1.4), Inches(1.2), Inches(10.5), Inches(2.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "ALANDAS TEA BERLIN // EXECUTIVE CHEAT SHEET"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_OLIVE
    p0.space_after = Pt(8)

    p1 = tf.add_paragraph()
    p1.text = "The Path from 25 to 100 Cafes"
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "A plain-English roadmap for Sidy Sow: How we automate sales grunt work, protect your brand, scale recurring cafe orders, and get you back to being your own boss full-time."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(14)
    p2.font.color.rgb = COLOR_TEXT_MUTED

    cards_s1 = [
        ("1. THE GOAL", "Freedom & Scale", ["Grow from 25 to 100 active cafes", "€15,000–€30,000/month recurring income", "Sidy quits Swiss job to be his own boss"]),
        ("2. THE ENGINE", "24/7 Digital Assistant", ["Scrapes cafes & gets owner WhatsApps", "Pitches €19 trial teapot box", "Parses order photos into invoices"]),
        ("3. THE 3 TIERS", "Earned Complexity", ["Tier 1: Safe automation (Sidy is pilot)", "Tier 2: Governed rules protect budget", "Tier 3: Autonomous loop at maturity"])
    ]
    w = Inches(3.68)
    gap = Inches(0.34)
    for i, (tag, title, bullets) in enumerate(cards_s1):
        add_formatted_card(s1, Inches(1.4) + i * (w + gap), Inches(4.3), w, Inches(2.1), tag, title, bullets, tag_color=COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST), title_size=15, bullet_size=11)

    # -------------------------------------------------------------
    # Slide 2: Why Are We Doing This?
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "01 // The Big Picture", "Why Are We Doing This? Sidy's Reality vs. The Goal",
               "Sidy imports exceptional organic tea, but current manual operations demand too much time for too little predictable cashflow.")
    add_footer(s2, 2)
    add_formatted_card(s2, Inches(0.8), Inches(1.9), Inches(5.68), Inches(4.9), "CURRENT REALITY // THE FOUNDER'S TRAP", "Why Sidy Is Stuck in a Day Job", [
        "High Swiss Living Costs: Moved to Switzerland; tea business doesn't yet yield steady monthly cashflow.",
        "Exhausting Day Job: Working for a Norwegian firm: 'It's been a long walk... I'm tired. I want to become again my own boss.'",
        "25 Happy Accounts: Already has ~25 great cafes buying regularly, but customer acquisition is stalled due to lack of time.",
        "Manual Friction: Sidy spends evenings manually messaging cafes on Instagram and deciphering paper orders."
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=13)

    add_formatted_card(s2, Inches(6.85), Inches(1.9), Inches(5.68), Inches(4.9), "THE TARGET // THE 100-CAFE EQUATION", "What 100 Accounts Actually Unlocks", [
        "100 Cafes @ €200–€350 / Month: Generates €15,000 to €30,000 every month in predictable wholesale orders.",
        "90%+ Gross Margin: Premium tea carries extraordinary margins when shipped directly in wholesale volume.",
        "Full-Time Freedom: Sidy hands in his notice in Switzerland and returns to Berlin as his own boss.",
        "Zero Additional Headcount: Operates the entire 100-cafe network without hiring expensive administrative staff."
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=13)

    # -------------------------------------------------------------
    # Slide 3: The 5 Bottlenecks
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "02 // Operational Diagnosis", "The 5 Bottlenecks Holding Alandas Back Today",
               "The exact friction points stopping Alandas from scaling from 25 to 100 cafes.")
    add_footer(s3, 3)
    bottlenecks = [
        ("BOTTLENECK 01", "Manual Scraping Sucks Time", ["Searching Google Maps & digging for owners burns 20+ hours/week."]),
        ("BOTTLENECK 02", "Cafes Ignore Cold Emails", ["Baristas are busy serving coffee. They run their business on WhatsApp."]),
        ("BOTTLENECK 03", "Order Processing Is Messy", ["Crumpled paper order photos texted late at night cause invoice errors."]),
        ("BOTTLENECK 04", "Silent Cafe Churn", ["Cafes run out on Day 28. If Sidy doesn't text on Day 25, they panic-buy supermarket tea."]),
        ("BOTTLENECK 05", "Burned by Hermes AI", ["Previous bot crashed and wiped memory. Sidy rightly refuses fragile low-code tools."]),
        ("THE OPPORTUNITY", "The Durable Solution", ["Replace manual hustle with a crash-resilient revenue machine backed by solid code."])
    ]
    w_b = Inches(3.72)
    h_b = Inches(2.3)
    gap_x = Inches(0.28)
    gap_y = Inches(0.3)
    for i, (tag, title, bullets) in enumerate(bottlenecks):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * (w_b + gap_x)
        y = Inches(1.9) + row * (h_b + gap_y)
        add_formatted_card(s3, x, y, w_b, h_b, tag, title, bullets, tag_color=COLOR_OLIVE if i==5 else COLOR_OCHRE, title_size=16, bullet_size=11.5)

    # -------------------------------------------------------------
    # Slide 4: What We Are Building
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "03 // The Solution", "What We Are Building: Your 24/7 Digital Revenue Machine",
               "A tireless digital sales and operations assistant that handles the tedious grunt work while Sidy retains total authority.")
    add_footer(s4, 4)
    stages = [
        ("STAGE 01 // DISCOVER", "Finds Ideal Cafes", ["Scans Google Maps & IG in Berlin, Munich, Hamburg for >30-seat brunch spots."]),
        ("STAGE 02 // ENRICH", "Gets Owner WhatsApps", ["Uses German Impressum legal trick to get verified mobile numbers for €0.00."]),
        ("STAGE 03 // OFFER", "Pitches €19 Teapot Kit", ["Offers shatter-resistant borosilicate teapot + 4 teas (100% credited back on crate)."]),
        ("STAGE 04 // APPROVAL", "Sidy Taps 'Send'", ["AI drafts warm WhatsApp message. Sidy reviews on phone & taps Approve."]),
        ("STAGE 05 // INVOICE", "OCR Reads Order Photos", ["Deciphers barista handwritten note photos into draft Dolibarr CRM invoices."]),
        ("STAGE 06 // RETENTION", "Day-25 Refill Alerts", ["Automated WhatsApp reminder on Day 25 stops cafe churn before it happens."])
    ]
    for i, (tag, title, bullets) in enumerate(stages):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * (w_b + gap_x)
        y = Inches(1.9) + row * (h_b + gap_y)
        add_formatted_card(s4, x, y, w_b, h_b, tag, title, bullets, tag_color=COLOR_OLIVE if col==0 else (COLOR_OCHRE if col==1 else COLOR_FOREST), title_size=16, bullet_size=11.5)

    # -------------------------------------------------------------
    # Slide 5: Why 3 Tiers?
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "04 // Architectural Law", "Why 3 Tiers? 'Don't Build a Spaceship on Day 1'",
               "We do not give AI full control on Day 1. Each tier earns complexity based on proven business scale.")
    add_footer(s5, 5)
    tiers_ladder = [
        ("TIER 3 // AUTONOMOUS PLATFORM (100+ CAFES)", "The Self-Running Business Machine",
         ["Closed-loop commercial machine across Germany, Austria & Switzerland.", "Cafe reorder velocity automatically triggers and refines Meta Ad experiments.", "Sidy acts as Chairman reviewing weekly revenue digests."]),
        ("TIER 2 // GOVERNED INTELLIGENCE (40–70 CAFES)", "The Smart Assistant with Guardrails",
         ["AI recommends smart moves (e.g. +30% ad budget), but strict Policy Engines enforce rules.", "Any budget delta > €5 requires Sidy's 1-tap WhatsApp sign-off.", "Mathematically impossible for an AI bug to drain bank accounts or leak pricing."]),
        ("TIER 1 // ESSENTIAL AUTOMATION (25–40 CAFES) — START HERE", "The Tireless Grunt Worker (Sidy is Pilot)",
         ["Machine scrapes cafes, gets WhatsApps, drafts pitches, and parses order notes.", "Sidy retains 100% approval authority on every outbound message and invoice.", "100% brand safe. Saves 15+ hours/week. Starts today with ZERO fragility."])
    ]
    h_ladder = Inches(1.5)
    gap_ladder = Inches(0.2)
    for i, (tag, title, bullets) in enumerate(tiers_ladder):
        y = Inches(1.9) + i * (h_ladder + gap_ladder)
        add_formatted_card(s5, Inches(0.8), y, Inches(11.733), h_ladder, tag, title, bullets,
                           tag_color=COLOR_FOREST if i==0 else (COLOR_OCHRE if i==1 else COLOR_OLIVE),
                           title_size=16, bullet_size=11.5)

    # -------------------------------------------------------------
    # Slide 6: Tier 1 Deep Dive
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "05 // Tier 1 in Plain English", "Tier 1: 'The Tireless Assistant' (Sidy is Pilot)",
               "The machine gathers facts and proposes actions; Sidy taps Approve before anything is dispatched.")
    s6.notes_slide.notes_text_frame.text = "Excalidraw Specification: tier1_essential_automation_flowchart.excalidraw\nInspect in canvas viewer: excalidraw_canvas_viewer.html#t1"
    add_footer(s6, 6)
    add_formatted_card(s6, Inches(0.8), Inches(1.9), Inches(5.68), Inches(4.9), "THE 5-STAGE WORKFLOW", "Read ➔ Analyze ➔ Propose ➔ Approve ➔ Execute", [
        "1. Read: Scans Google Maps and Instagram for cafes with >30 seats.",
        "2. Analyze: Evaluates menu pricing and specialty coffee/food aesthetic.",
        "3. Propose: Drafts personalized WhatsApp message pitching the €19 teapot kit.",
        "4. Human Approves: Message appears on Sidy's WhatsApp. Sidy taps Approve.",
        "5. Execute: Temporal sends message, creates Dolibarr card, schedules Day-4 follow-up."
    ], tag_color=COLOR_OLIVE, title_size=18, bullet_size=12.5)

    add_formatted_card(s6, Inches(6.85), Inches(1.9), Inches(5.68), Inches(4.9), "COMMERCIAL VALUE FOR SIDY", "What Sidy Experiences Today", [
        "Zero Brand Risk: AI cannot hallucinate or make false botanical claims. Sidy sees everything first.",
        "Saves 15+ Hours Every Week: No more manual copy-pasting or deciphering crumpled notes late at night.",
        "Target: 25 ➔ 40 Cafes | ~€5,000/month in steady wholesale revenue.",
        "Temporal Durability: Power outages or server reboots never lose a single lead or order."
    ], tag_color=COLOR_OLIVE, title_size=18, bullet_size=12.5)

    # -------------------------------------------------------------
    # Slide 7: Tier 2 Deep Dive
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "06 // Tier 2 in Plain English", "Tier 2: 'The Smart Assistant with Guardrails'",
               "AI suggests business optimizations, but unbreakable Policy Engines prevent errors or runaway spend.")
    s7.notes_slide.notes_text_frame.text = "Excalidraw Specification: tier2_governed_intelligence_flowchart.excalidraw\nInspect in canvas viewer: excalidraw_canvas_viewer.html#t2"
    add_footer(s7, 7)
    add_formatted_card(s7, Inches(0.8), Inches(1.9), Inches(5.68), Inches(4.9), "REAL-WORLD EXAMPLE", "Increasing Meta Ad Budget by +30%", [
        "1. AI Observes: Berlin brunch ad has 4.2x ROAS. AI suggests raising budget from €30 to €39/day.",
        "2. Policy Check 1 (Ceiling): Is €39 under our maximum €50/day cap? (YES).",
        "3. Policy Check 2 (Threshold): Does delta (>€5) require human sign-off? (YES).",
        "4. Sidy Notified: Phone dings: [Approve +€9/day for Berlin Brunch Ad?].",
        "5. Verify State: AI calls Meta API, then re-queries Meta to confirm it is €39.00 and NOT €390.00."
    ], tag_color=COLOR_OCHRE, title_size=18, bullet_size=12.5)

    add_formatted_card(s7, Inches(6.85), Inches(1.9), Inches(5.68), Inches(4.9), "COMMERCIAL VALUE FOR SIDY", "Why Tier 2 Commands Premium Value", [
        "Zero Runaway Spend: Mathematically impossible for an AI glitch to drain bank accounts.",
        "Zero Pricing Leaks: Wholesale volume discounts follow strict tables, not model whims.",
        "Automated Day-25 Refills: Alerts cafes before they run out of tea, stopping quiet churn.",
        "Target: 40 ➔ 70 Cafes | ~€12,000/month in recurring revenue."
    ], tag_color=COLOR_OCHRE, title_size=18, bullet_size=12.5)

    # -------------------------------------------------------------
    # Slide 8: Tier 3 Deep Dive
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "07 // Tier 3 in Plain English", "Tier 3: 'The Self-Running Business Machine'",
               "Alandas runs like a multi-million-euro beverage brand with zero extra office staff.")
    s8.notes_slide.notes_text_frame.text = "Excalidraw Specification: tier3_autonomous_platform_flowchart.excalidraw\nInspect in canvas viewer: excalidraw_canvas_viewer.html#t3"
    add_footer(s8, 8)
    add_formatted_card(s8, Inches(0.8), Inches(1.9), Inches(5.68), Inches(4.9), "THE CLOSED-LOOP FLYWHEEL", "Munich Terrace Summer Scenario", [
        "1. Reorder Surge: In July, Munich cafes reorder Earl Grey 2x faster for iced tea.",
        "2. Operations Alerts Marketing: System detects Munich terrace surge in real time.",
        "3. Automated Ad Copy: Marketing Agent writes: 'Serving iced tea on your terrace? Try our €19 kit.'",
        "4. Closed-Loop Optimization: Launches tests and scales ad spend without manual human effort."
    ], tag_color=COLOR_FOREST, title_size=18, bullet_size=12.5)

    add_formatted_card(s8, Inches(6.85), Inches(1.9), Inches(5.68), Inches(4.9), "TOTAL FOUNDER INDEPENDENCE", "What Tier 3 Delivers", [
        "Zero Linear Headcount: Operates across Germany, Austria & Switzerland without hiring reps.",
        "Automated Circuit Breakers: Any anomaly halts the system instantly and alerts Sidy.",
        "Sidy Acts as Chairman: Reviews weekly digests while enjoying tea instead of grinding phone calls.",
        "Target: 100+ Cafes | €20k–€30k/month recurring revenue. Sidy is 100% his own boss."
    ], tag_color=COLOR_FOREST, title_size=18, bullet_size=12.5)

    # -------------------------------------------------------------
    # Slide 9: The 3 Secret Weapons
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "08 // Technical Defense Made Simple", "The 3 Technical 'Secret Weapons' (In Plain English)",
               "Three simple metaphors to explain the architecture to Sidy or investors without confusing jargon.")
    add_footer(s9, 9)
    weapons = [
        ("SECRET WEAPON 01", "Temporal vs. n8n", "Carving in Stone vs. Sticky Notes", [
            "n8n writes orders on sticky notes. When the server crashes, notes blow away and data is lost.",
            "Temporal carves every step into solid rock. If the server reboots, it resumes at the exact line of code.",
            "Zero lost invoices, zero lost leads."
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
        create_card(s9, x, Inches(1.9), w_w, Inches(4.9))
        tb = s9.shapes.add_textbox(x + Inches(0.24), Inches(2.1), w_w - Inches(0.48), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = tag
        p0.font.name = FONT_BODY
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST)
        p0.space_after = Pt(3)

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
            pb.space_after = Pt(6)

    # -------------------------------------------------------------
    # Slide 10: 12-Month Roadmap
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "09 // Financial & Personal Roadmap", "Sidy's 12-Month Roadmap to Freedom",
               "From surviving in Switzerland to building a full-time €25,000/month tea enterprise.")
    add_footer(s10, 10)
    phases = [
        ("MONTHS 1–3 // TIER 1: ESSENTIAL", "Stabilize & Save Time", [
            "What We Build: Stabilize Dolibarr CRM, automated cafe scraping, WhatsApp OCR order parser, standardize €19 teapot kit.",
            "Sidy's Life: Works Swiss job, but spends just 30 mins/day reviewing qualified cafe leads on WhatsApp.",
            "Target Accounts: 25 ➔ 40 Cafes",
            "Target Revenue: ~€5,000 / month"
        ]),
        ("MONTHS 4–6 // TIER 2: GOVERNED", "Scale & Protect Margins", [
            "What We Build: Deploy Policy Engine for Meta Ads (+30% rule), Day-25 refill alerts, structured audit logging.",
            "Sidy's Life: Admin time drops to < 4 hours/week. Cafes reorder on clockwork. Sidy prepares his notice.",
            "Target Accounts: 40 ➔ 70 Cafes",
            "Target Revenue: ~€12,000 / month"
        ]),
        ("MONTHS 7–12 // TIER 3: PLATFORM", "Flywheel & Full Freedom", [
            "What We Build: Closed-loop flywheel connecting cafe reorders to Meta ad creative; multi-city expansion.",
            "Sidy's Life: Hands in notice at Swiss firm. Returns to Berlin as 100% full-time independent founder & CEO.",
            "Target Accounts: 100+ Cafes",
            "Target Revenue: €20,000–€30,000 / month"
        ])
    ]
    for i, (tag, title, bullets) in enumerate(phases):
        x = Inches(0.8) + i * (w_w + Inches(0.28))
        add_formatted_card(s10, x, Inches(1.9), w_w, Inches(4.9), tag, title, bullets,
                           tag_color=COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST),
                           title_size=18, bullet_size=12)

    # -------------------------------------------------------------
    # Slide 11: Next Steps
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10 // Immediate Next Steps", "Starting Sprint 1 Today: The First 4 Concrete Steps",
               "We do not need months of planning. We kick off Tier 1 immediately with 4 clear deliverables.")
    add_footer(s11, 11)
    steps = [
        ("STEP 01", "Stabilize Dolibarr CRM", ["Automate daily cloud backups", "Clean existing 25 cafe accounts", "Ensure order history is never lost"]),
        ("STEP 02", "Standardize €19 Trial Kit", ["Assemble borosilicate teapot kit", "Pack 4 signature tea blends", "Include 100% wholesale credit voucher"]),
        ("STEP 03", "Run § 5 TMG Scraper", ["Extract 200 brunch cafes in Berlin & Munich", "Resolve owner names & emails for €0.00", "Zero wasted lead spend"]),
        ("STEP 04", "1-Tap WhatsApp Pilot", ["Generate first 10 personalized drafts", "Send to Sidy's WhatsApp for review", "Sidy taps Approve with one click"])
    ]
    w_s = Inches(2.72)
    gap_s = Inches(0.28)
    for i, (tag, title, bullets) in enumerate(steps):
        x = Inches(0.8) + i * (w_s + gap_s)
        add_formatted_card(s11, x, Inches(1.9), w_s, Inches(4.9), tag, title, bullets, tag_color=COLOR_OLIVE, title_size=17, bullet_size=12)

    prs.save(output_path)
    print(f"[SUCCESS] Cheat Sheet PowerPoint presentation generated: {output_path}")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load SVGs
    with open(os.path.join(base_dir, "tier1_flowchart.svg"), "r", encoding="utf-8") as f:
        t1_svg = f.read()
    with open(os.path.join(base_dir, "tier2_flowchart.svg"), "r", encoding="utf-8") as f:
        t2_svg = f.read()
    with open(os.path.join(base_dir, "tier3_flowchart.svg"), "r", encoding="utf-8") as f:
        t3_svg = f.read()
    with open(os.path.join(base_dir, "waterfall_enrichment.svg"), "r", encoding="utf-8") as f:
        wf_svg = f.read()

    output_html = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck.html")
    output_pptx = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck.pptx")

    build_cheat_sheet_html(output_html, t1_svg, t2_svg, t3_svg, wf_svg)
    build_cheat_sheet_pptx(output_pptx)
    print("\n[COMPLETE] Both Cheat Sheet decks generated successfully!")

if __name__ == "__main__":
    main()
