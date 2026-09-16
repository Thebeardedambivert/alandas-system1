"""
inject_flowcharts_into_deck.py
Injects native Excalidraw flowcharts, interactive view toggles, canvas controls, and fullscreen modals
into Alandas_Tiered_Architecture_Presentation.html and Alandas_Tiered_Architecture_System.pptx
"""

import os
import re

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gen_script_path = os.path.join(base_dir, "scripts", "generate_tiered_presentation.py")

    # Load SVG contents
    with open(os.path.join(base_dir, "tier1_flowchart.svg"), "r", encoding="utf-8") as f:
        t1_svg = f.read()
    with open(os.path.join(base_dir, "waterfall_enrichment.svg"), "r", encoding="utf-8") as f:
        wf_svg = f.read()
    with open(os.path.join(base_dir, "tier2_flowchart.svg"), "r", encoding="utf-8") as f:
        t2_svg = f.read()
    with open(os.path.join(base_dir, "tier3_flowchart.svg"), "r", encoding="utf-8") as f:
        t3_svg = f.read()

    with open(gen_script_path, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. CSS Injection: Add flowcharts and modal styles before </style>
    flowchart_css = """
    /* FLOWCHART VIEW SWITCHER & INTERACTIVE CANVAS */
    .flowchart-toggle-group {
      display: flex;
      align-items: center;
      gap: 6px;
      background: #FFFFFF;
      border: 1.5px solid var(--border);
      padding: 4px 6px;
      border-radius: 30px;
      box-shadow: var(--shadow-sm);
    }
    .toggle-btn {
      background: transparent;
      border: none;
      font-family: var(--font-body);
      font-size: 13px;
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
    }
    .toggle-btn:hover {
      color: var(--text-main);
      background: var(--card-alt);
    }
    .toggle-btn.active {
      background: var(--olive);
      color: #FFFFFF;
    }
    .toggle-btn.ochre.active {
      background: var(--ochre);
      color: #FFFFFF;
    }
    .toggle-btn.forest.active {
      background: var(--forest);
      color: #FFFFFF;
    }
    .toggle-btn.expand-btn {
      background: var(--olive-light);
      color: var(--olive-dark);
      font-weight: 700;
      border: 1px solid var(--olive-border);
    }
    .toggle-btn.expand-btn:hover {
      background: var(--olive);
      color: #FFFFFF;
    }
    .toggle-btn.link-btn {
      color: var(--ochre-dark);
      font-weight: 700;
    }
    .toggle-btn.link-btn:hover {
      color: var(--ochre);
      background: var(--ochre-light);
    }

    /* VIEW PANELS INSIDE SLIDE BODY */
    .view-panel {
      display: none;
      width: 100%;
      height: 100%;
    }
    .view-panel.active {
      display: flex;
      flex-direction: column;
      animation: panelFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes panelFadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* FLOWCHART CANVAS CONTAINER */
    .flowchart-panel {
      height: 100%;
      min-height: 0;
    }
    .flowchart-canvas-wrapper {
      background: #FFFFFF;
      border: 1.5px solid var(--border);
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      height: 100%;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }
    .flowchart-canvas-toolbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 20px;
      background: #F7F5EE;
      border-bottom: 1px solid var(--border);
      flex-shrink: 0;
    }
    .flowchart-title {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      color: var(--olive-dark);
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .toolbar-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .tb-btn {
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
    }
    .tb-btn:hover {
      background: var(--olive-light);
      border-color: var(--olive-border);
      color: var(--olive-dark);
    }
    .tb-btn.highlight {
      background: var(--ochre-light);
      border-color: var(--ochre-border);
      color: var(--ochre-dark);
      font-weight: 700;
    }
    .tb-btn.highlight:hover {
      background: var(--ochre);
      color: #FFFFFF;
    }

    .flowchart-scroll-box {
      flex: 1;
      overflow-y: auto;
      overflow-x: auto;
      padding: 24px;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      background: radial-gradient(circle at 50% 50%, #FAF8F2 0%, #EDE8DC 100%);
    }
    .svg-container {
      background: #FFFFFF;
      border: 1px solid #D5CFC2;
      border-radius: 12px;
      box-shadow: 0 12px 36px rgba(0,0,0,0.08);
      transform-origin: top center;
      transition: transform 0.2s ease-out;
    }
    .svg-container svg {
      display: block;
      max-width: 100%;
      height: auto;
    }

    /* FULLSCREEN INTERACTIVE MODAL */
    .flowchart-modal {
      position: fixed;
      inset: 0;
      z-index: 9999;
      display: none;
      align-items: center;
      justify-content: center;
    }
    .flowchart-modal.open {
      display: flex;
    }
    .modal-backdrop {
      position: absolute;
      inset: 0;
      background: rgba(12, 15, 12, 0.88);
      backdrop-filter: blur(10px);
    }
    .modal-content {
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
    }
    .modal-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 24px;
      background: #1F231D;
      border-bottom: 1px solid #3A3E35;
      flex-shrink: 0;
    }
    .modal-badge {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      background: var(--olive);
      color: #FFF;
      padding: 3px 8px;
      border-radius: 4px;
      letter-spacing: 0.08em;
    }
    .modal-title {
      font-family: var(--font-display);
      font-size: 20px;
      color: #FFF;
      margin-top: 3px;
    }
    .modal-controls {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .modal-ctrl-btn {
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
    }
    .modal-ctrl-btn:hover {
      background: #343A30;
      color: #FFF;
    }
    .modal-ctrl-btn.highlight {
      background: var(--ochre);
      color: #FFF;
      border-color: #9A6622;
      font-weight: 700;
    }
    .modal-close-btn {
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
      transition: background 0.2s;
    }
    .modal-close-btn:hover {
      background: #7F1D1D;
      color: #FFF;
    }
    .modal-body {
      flex: 1;
      overflow: auto;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 32px;
      background: radial-gradient(circle at 50% 50%, #1F231D 0%, #121411 100%);
    }
    .modal-svg-container {
      background: #FFFFFF;
      border-radius: 14px;
      box-shadow: 0 25px 60px rgba(0,0,0,0.6);
      border: 2px solid #33382D;
      transform-origin: top center;
      transition: transform 0.2s ease-out;
    }
  </style>"""

    if "/* FLOWCHART VIEW SWITCHER & INTERACTIVE CANVAS */" not in code:
        code = code.replace("  </style>", flowchart_css)

    # 2. Update Slide 7
    slide7_pattern = r'(<!-- SLIDE 7: Tier 1 Deep Dive -->\s*<!-- =================================================================== -->\s*<div class="slide" data-slide="7">)(.*?)(<div class="slide-footer">)'
    
    new_slide7_content = f"""
      <div class="slide-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div class="kicker">Tier 1 Execution Flow</div>
            <h2 class="slide-title">The Human-Directed Autonomy Model</h2>
            <p class="slide-subtitle">
              The safest entry tier for any business: the machine gathers information and proposes actions, but the human retains complete authority over all consequential decisions.
            </p>
          </div>
          <div class="flowchart-toggle-group">
            <button class="toggle-btn active" onclick="setSlideView(7, 'cards')">Executive View</button>
            <button class="toggle-btn" onclick="setSlideView(7, 'flowchart')">⚡ Excalidraw State Machine</button>
            <button class="toggle-btn expand-btn" onclick="openFlowchartModal('tier1')" title="Open Fullscreen Interactive Flowchart">⛶ Fullscreen</button>
            <a href="excalidraw_canvas_viewer.html#t1" target="_blank" class="toggle-btn link-btn" title="Open in Multi-Tab Canvas Viewer">Canvas Viewer ↗</a>
          </div>
        </div>
      </div>

      <div class="slide-body">
        <!-- View 1: Executive 5-Stage Cards -->
        <div id="slide-7-cards" class="view-panel active">
          <div class="card" style="padding: 36px; height: 100%; justify-content: space-around;">
            <div style="display: flex; align-items: stretch; justify-content: space-between; gap: 18px;">
              <!-- Step 1 -->
              <div style="flex: 1; background: var(--card-alt); border: 1.5px solid var(--border); border-radius: 12px; padding: 20px;">
                <div style="font-family: var(--font-mono); font-size: 13px; color: var(--olive); font-weight: 700;">STAGE 01</div>
                <h4 style="font-family: var(--font-display); font-size: 22px; font-weight: 700; margin: 6px 0 10px 0;">READ</h4>
                <p style="font-size: 14.5px; color: var(--text-muted); line-height: 1.45;">System detects inbound Instagram comment or scrapes target cafe on Google Maps.</p>
              </div>
              <div style="display: flex; align-items: center; font-size: 24px; color: var(--olive);">➔</div>

              <!-- Step 2 -->
              <div style="flex: 1; background: var(--card-alt); border: 1.5px solid var(--border); border-radius: 12px; padding: 20px;">
                <div style="font-family: var(--font-mono); font-size: 13px; color: var(--olive); font-weight: 700;">STAGE 02</div>
                <h4 style="font-family: var(--font-display); font-size: 22px; font-weight: 700; margin: 6px 0 10px 0;">ANALYZE</h4>
                <p style="font-size: 14.5px; color: var(--text-muted); line-height: 1.45;">LLM extracts menu items, beverage prices, and seating capacity; calculates ICP score.</p>
              </div>
              <div style="display: flex; align-items: center; font-size: 24px; color: var(--olive);">➔</div>

              <!-- Step 3 -->
              <div style="flex: 1; background: var(--ochre-light); border: 1.5px solid var(--ochre-border); border-radius: 12px; padding: 20px;">
                <div style="font-family: var(--font-mono); font-size: 13px; color: var(--ochre-dark); font-weight: 700;">STAGE 03</div>
                <h4 style="font-family: var(--font-display); font-size: 22px; font-weight: 700; margin: 6px 0 10px 0;">PROPOSE</h4>
                <p style="font-size: 14.5px; color: var(--ochre-dark); line-height: 1.45;">Generates hyper-personalized outreach emphasizing €19 trial kit and 96% gross profit.</p>
              </div>
              <div style="display: flex; align-items: center; font-size: 24px; color: var(--olive);">➔</div>

              <!-- Step 4 -->
              <div style="flex: 1.2; background: #FFFFFF; border: 2.5px solid var(--olive); border-radius: 12px; padding: 20px; box-shadow: var(--shadow-sm);">
                <div style="font-family: var(--font-mono); font-size: 13px; color: var(--olive); font-weight: 700;">HUMAN GATE</div>
                <h4 style="font-family: var(--font-display); font-size: 22px; font-weight: 700; margin: 6px 0 10px 0; color: var(--olive-dark);">APPROVE</h4>
                <p style="font-size: 14.5px; color: var(--text-main); line-height: 1.45;"><strong>Sidy reviews in 1 tap on WhatsApp.</strong> Zero risk of bot hallucinating botanical claims.</p>
              </div>
              <div style="display: flex; align-items: center; font-size: 24px; color: var(--olive);">➔</div>

              <!-- Step 5 -->
              <div style="flex: 1; background: var(--olive-light); border: 1.5px solid var(--olive-border); border-radius: 12px; padding: 20px;">
                <div style="font-family: var(--font-mono); font-size: 13px; color: var(--olive-dark); font-weight: 700;">STAGE 05</div>
                <h4 style="font-family: var(--font-display); font-size: 22px; font-weight: 700; margin: 6px 0 10px 0;">EXECUTE</h4>
                <p style="font-size: 14.5px; color: var(--text-muted); line-height: 1.45;">Temporal dispatches message, creates Dolibarr lead card, and schedules Day-4 follow-up.</p>
              </div>
            </div>

            <div style="background: var(--card-alt); border-radius: 12px; padding: 18px 24px; margin-top: 20px; display: flex; align-items: center; justify-content: space-between;">
              <div style="font-size: 16px; color: var(--text-main);">
                <strong>The Crucial Distinction:</strong> At no point is an LLM allowed to send unreviewed communication or modify financial ledger balances. Sidy gets 90% time savings with 100% brand control.
              </div>
              <span class="badge-pill badge-olive" style="font-size: 14px;">100% Brand Safe</span>
            </div>
          </div>
        </div>

        <!-- View 2: Native Excalidraw Flowchart -->
        <div id="slide-7-flowchart" class="view-panel flowchart-panel">
          <div class="flowchart-canvas-wrapper">
            <div class="flowchart-canvas-toolbar">
              <span class="flowchart-title">⚡ Tier 1: Essential Revenue Automation Flowchart (2,275px Full Vision)</span>
              <div class="toolbar-actions">
                <button class="tb-btn" onclick="zoomCanvas(7, 1.2)">Zoom In (+)</button>
                <button class="tb-btn" onclick="zoomCanvas(7, 0.8)">Zoom Out (-)</button>
                <button class="tb-btn" onclick="resetCanvas(7)">Reset (↺)</button>
                <button class="tb-btn highlight" onclick="openFlowchartModal('tier1')">⛶ Expand Fullscreen</button>
                <a href="tier1_essential_automation_flowchart.excalidraw" download class="tb-btn">Download .excalidraw</a>
              </div>
            </div>
            <div class="flowchart-scroll-box" id="flowchart-box-7">
              <div class="svg-container" id="svg-wrap-7">
{t1_svg}
              </div>
            </div>
          </div>
        </div>
      </div>
      """

    code = re.sub(slide7_pattern, r'\1' + new_slide7_content + r'\3', code, flags=re.DOTALL)

    # 3. Update Slide 8
    slide8_pattern = r'(<!-- SLIDE 8: Waterfall Enrichment Engine -->\s*<!-- =================================================================== -->\s*<div class="slide" data-slide="8">)(.*?)(<div class="slide-footer">)'
    
    new_slide8_content = f"""
      <div class="slide-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div class="kicker">Tier 1 Lead Intelligence // Waterfall Architecture</div>
            <h2 class="slide-title">Waterfall Enrichment: "Cheapest Tool First"</h2>
            <p class="slide-subtitle">
              Each tool only gets what the last one missed. How Alandas achieves a ~92% decision-maker find rate with direct WhatsApp numbers at an 87% data cost reduction.
            </p>
          </div>
          <div class="flowchart-toggle-group">
            <button class="toggle-btn active" onclick="setSlideView(8, 'cards')">Waterfall Breakdown & ROI</button>
            <button class="toggle-btn" onclick="setSlideView(8, 'flowchart')">⚡ Excalidraw Waterfall State Machine</button>
            <button class="toggle-btn expand-btn" onclick="openFlowchartModal('waterfall')" title="Open Fullscreen Interactive Flowchart">⛶ Fullscreen</button>
            <a href="excalidraw_canvas_viewer.html#wf" target="_blank" class="toggle-btn link-btn" title="Open in Multi-Tab Canvas Viewer">Canvas Viewer ↗</a>
          </div>
        </div>
      </div>

      <div class="slide-body">
        <!-- View 1: 5-Stage Waterfall Cards -->
        <div id="slide-8-cards" class="view-panel active">
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

        <!-- View 2: Excalidraw Waterfall Flowchart -->
        <div id="slide-8-flowchart" class="view-panel flowchart-panel">
          <div class="flowchart-canvas-wrapper">
            <div class="flowchart-canvas-toolbar">
              <span class="flowchart-title">⚡ Waterfall Enrichment Pipeline — Cheapest Tool First (State Machine)</span>
              <div class="toolbar-actions">
                <button class="tb-btn" onclick="zoomCanvas(8, 1.2)">Zoom In (+)</button>
                <button class="tb-btn" onclick="zoomCanvas(8, 0.8)">Zoom Out (-)</button>
                <button class="tb-btn" onclick="resetCanvas(8)">Reset (↺)</button>
                <button class="tb-btn highlight" onclick="openFlowchartModal('waterfall')">⛶ Expand Fullscreen</button>
                <a href="waterfall_enrichment_engine.excalidraw" download class="tb-btn">Download .excalidraw</a>
              </div>
            </div>
            <div class="flowchart-scroll-box" id="flowchart-box-8">
              <div class="svg-container" id="svg-wrap-8">
{wf_svg}
              </div>
            </div>
          </div>
        </div>
      </div>
      """

    code = re.sub(slide8_pattern, r'\1' + new_slide8_content + r'\3', code, flags=re.DOTALL)

    # 4. Update Slide 10
    slide10_pattern = r'(<!-- SLIDE 10: Tier 2 Decision Contract in Action -->\s*<!-- =================================================================== -->\s*<div class="slide" data-slide="10">)(.*?)(<div class="slide-footer">)'

    new_slide10_content = f"""
      <div class="slide-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div class="kicker">Tier 2 Governance in Action</div>
            <h2 class="slide-title">The Decision Contract Walkthrough</h2>
            <p class="slide-subtitle">
              Example: The AI ad agent observes that the Berlin Cafe Meta campaign is converting well and recommends increasing the budget by 30%. How the system governs this safely:
            </p>
          </div>
          <div class="flowchart-toggle-group">
            <button class="toggle-btn ochre active" onclick="setSlideView(10, 'cards')">8-Stage Governance Gate</button>
            <button class="toggle-btn ochre" onclick="setSlideView(10, 'flowchart')">⚡ Excalidraw Governed Flowchart</button>
            <button class="toggle-btn expand-btn" onclick="openFlowchartModal('tier2')" title="Open Fullscreen Interactive Flowchart">⛶ Fullscreen</button>
            <a href="excalidraw_canvas_viewer.html#t2" target="_blank" class="toggle-btn link-btn" title="Open in Multi-Tab Canvas Viewer">Canvas Viewer ↗</a>
          </div>
        </div>
      </div>

      <div class="slide-body">
        <!-- View 1: 8-Stage Gate Cards -->
        <div id="slide-10-cards" class="view-panel active">
          <div class="grid-2">
            <!-- Flow Steps -->
            <div class="card">
              <span class="card-tag tag-ochre">The 8-Stage Governance Gate</span>
              <ol style="display: flex; flex-direction: column; gap: 14px; padding-left: 20px; font-size: 16px; color: var(--text-main); line-height: 1.45;">
                <li><strong>AI Recommendation:</strong> "Increase Berlin Brunch Ad budget from €30/day to €39/day (+30%)."</li>
                <li><strong>Validity Check:</strong> Is campaign ID active? Does the ad set exist?</li>
                <li><strong>Eligibility Check:</strong> Has campaign run > 7 days? Is ROAS > 3.0x? (Yes: 4.2x).</li>
                <li><strong>Policy Evaluation:</strong> Does €39 exceed the daily ceiling (€50)? (Compliant).</li>
                <li><strong>Approval Threshold:</strong> Does budget delta > €5 require human sign-off? (Policy: YES).</li>
                <li><strong>Human Approval:</strong> Sidy receives 1-tap notification: <em>[Approve +€9/day]</em>.</li>
                <li><strong>Execute & Verify:</strong> Meta API called; system re-queries Meta to confirm new budget = €39.00.</li>
                <li><strong>Audit Logging:</strong> Immutable record written with reasoning, timestamp, and Sidy's ID.</li>
              </ol>
            </div>

            <!-- Why This Matters -->
            <div class="card accent-olive">
              <span class="card-tag tag-olive">Commercial Value</span>
              <h3 class="card-title">What the Customer Is Actually Paying For</h3>
              <p class="card-desc">This is why Tier 2 commands 3x to 5x higher pricing than simple webhook automations:</p>
              <ul class="bullet-list">
                <li><strong>Zero Runaway Spend:</strong> An AI bug or hallucination can never drain the customer's bank account or ad budget.</li>
                <li><strong>Zero Pricing Leaks:</strong> B2B wholesale volume discounts follow strict mathematical tables, not model whims.</li>
                <li><strong>Regulatory Compliance:</strong> Strict policy checks guarantee botanical and organic labeling compliance under German food regulations.</li>
                <li><strong>Complete Auditability:</strong> In any dispute, the customer has an exact chronological record of every AI decision.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- View 2: Excalidraw Governed Intelligence Flowchart -->
        <div id="slide-10-flowchart" class="view-panel flowchart-panel">
          <div class="flowchart-canvas-wrapper">
            <div class="flowchart-canvas-toolbar">
              <span class="flowchart-title">⚡ Tier 2: Governed Decision Flow & Policy Enforcement Gate (State Machine)</span>
              <div class="toolbar-actions">
                <button class="tb-btn" onclick="zoomCanvas(10, 1.2)">Zoom In (+)</button>
                <button class="tb-btn" onclick="zoomCanvas(10, 0.8)">Zoom Out (-)</button>
                <button class="tb-btn" onclick="resetCanvas(10)">Reset (↺)</button>
                <button class="tb-btn highlight" onclick="openFlowchartModal('tier2')">⛶ Expand Fullscreen</button>
                <a href="tier2_governed_intelligence_flowchart.excalidraw" download class="tb-btn">Download .excalidraw</a>
              </div>
            </div>
            <div class="flowchart-scroll-box" id="flowchart-box-10">
              <div class="svg-container" id="svg-wrap-10">
{t2_svg}
              </div>
            </div>
          </div>
        </div>
      </div>
      """

    code = re.sub(slide10_pattern, r'\1' + new_slide10_content + r'\3', code, flags=re.DOTALL)

    # 5. Update Slide 12
    slide12_pattern = r'(<!-- SLIDE 12: Tier 3 Closed-Loop Flywheel -->\s*<!-- =================================================================== -->\s*<div class="slide" data-slide="12">)(.*?)(<div class="slide-footer">)'

    new_slide12_content = f"""
      <div class="slide-header">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div class="kicker">Tier 3 Operational Flywheel</div>
            <h2 class="slide-title">The Closed-Loop Commercial Flywheel</h2>
            <p class="slide-subtitle">
              Instead of automating disconnected tasks, Tier 3 connects top-of-funnel acquisition directly to post-purchase retention and lifetime value in a continuous feedback loop.
            </p>
          </div>
          <div class="flowchart-toggle-group">
            <button class="toggle-btn forest active" onclick="setSlideView(12, 'cards')">Operational Flywheel & LTV</button>
            <button class="toggle-btn forest" onclick="setSlideView(12, 'flowchart')">⚡ Excalidraw Autonomous Platform</button>
            <button class="toggle-btn expand-btn" onclick="openFlowchartModal('tier3')" title="Open Fullscreen Interactive Flowchart">⛶ Fullscreen</button>
            <a href="excalidraw_canvas_viewer.html#t3" target="_blank" class="toggle-btn link-btn" title="Open in Multi-Tab Canvas Viewer">Canvas Viewer ↗</a>
          </div>
        </div>
      </div>

      <div class="slide-body">
        <!-- View 1: Flywheel Cards -->
        <div id="slide-12-cards" class="view-panel active">
          <div class="card" style="padding: 36px; height: 100%; justify-content: space-between;">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
              <div style="background: var(--card-alt); border-radius: 12px; padding: 20px; border-left: 4px solid var(--olive);">
                <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--olive);">STAGE 01 // DISCOVER</div>
                <h4 style="font-size: 18px; font-weight: 700; margin: 8px 0 6px 0;">Market Signals</h4>
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.4;">Scrapes German dining clusters, tracks Instagram engagement, and identifies active beverage buyers.</p>
              </div>

              <div style="background: var(--card-alt); border-radius: 12px; padding: 20px; border-left: 4px solid var(--ochre);">
                <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--ochre);">STAGE 02 // CONVERT</div>
                <h4 style="font-size: 18px; font-weight: 700; margin: 8px 0 6px 0;">€19 Trial Box</h4>
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.4;">Automated qualification routes heavy borosilicate teapot to verified cafe baristas with 100% credit.</p>
              </div>

              <div style="background: var(--card-alt); border-radius: 12px; padding: 20px; border-left: 4px solid var(--forest);">
                <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--forest);">STAGE 03 // ONBOARD</div>
                <h4 style="font-size: 18px; font-weight: 700; margin: 8px 0 6px 0;">Starter Crate</h4>
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.4;">€249 Starter Crate deployed. Counter display installed. Barista brewing cheat sheets automated.</p>
              </div>

              <div style="background: var(--card-alt); border-radius: 12px; padding: 20px; border-left: 4px solid var(--olive-dark);">
                <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--olive-dark);">STAGE 04 // REFILL</div>
                <h4 style="font-size: 18px; font-weight: 700; margin: 8px 0 6px 0;">Predictive Refills</h4>
                <p style="font-size: 14px; color: var(--text-muted); line-height: 1.4;">Day-25 consumption alerts dispatch 1-click WhatsApp reorders with automated Dolibarr PDF invoicing.</p>
              </div>
            </div>

            <div style="background: var(--olive-light); border: 2px dashed var(--olive-border); border-radius: 14px; padding: 24px; display: flex; align-items: center; justify-content: space-between; gap: 24px;">
              <div style="flex: 1;">
                <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: var(--olive-dark); text-transform: uppercase;">The Feedback Loop // What Makes It Autonomous</div>
                <div style="font-size: 17px; color: var(--text-main); margin-top: 6px; line-height: 1.5;">
                  Actual cafe replenishment rates feed back into the <strong>Ads Agent</strong>. If brunch cafes in Munich reorder Earl Grey 2x faster than average, the system automatically writes new ad copy, allocates budget to Munich brunch clusters, and tests new creative hypotheses.
                </div>
              </div>
              <div style="text-align: right; white-space: nowrap;">
                <span class="badge-pill badge-olive" style="font-size: 16px; padding: 8px 16px;">Self-Reinforcing LTV</span>
              </div>
            </div>
          </div>
        </div>

        <!-- View 2: Excalidraw Autonomous Platform Flowchart -->
        <div id="slide-12-flowchart" class="view-panel flowchart-panel">
          <div class="flowchart-canvas-wrapper">
            <div class="flowchart-canvas-toolbar">
              <span class="flowchart-title">⚡ Tier 3: Autonomous Revenue Platform Flowchart (Closed-Loop Flywheel)</span>
              <div class="toolbar-actions">
                <button class="tb-btn" onclick="zoomCanvas(12, 1.2)">Zoom In (+)</button>
                <button class="tb-btn" onclick="zoomCanvas(12, 0.8)">Zoom Out (-)</button>
                <button class="tb-btn" onclick="resetCanvas(12)">Reset (↺)</button>
                <button class="tb-btn highlight" onclick="openFlowchartModal('tier3')">⛶ Expand Fullscreen</button>
                <a href="tier3_autonomous_platform_flowchart.excalidraw" download class="tb-btn">Download .excalidraw</a>
              </div>
            </div>
            <div class="flowchart-scroll-box" id="flowchart-box-12">
              <div class="svg-container" id="svg-wrap-12">
{t3_svg}
              </div>
            </div>
          </div>
        </div>
      </div>
      """

    code = re.sub(slide12_pattern, r'\1' + new_slide12_content + r'\3', code, flags=re.DOTALL)

    # 6. Add Modal HTML and Nav Link before </body>
    modal_html = """
<!-- FULLSCREEN FLOWCHART MODAL -->
<div id="flowchartModal" class="flowchart-modal">
  <div class="modal-backdrop" onclick="closeFlowchartModal()"></div>
  <div class="modal-content">
    <div class="modal-header">
      <div>
        <span class="modal-badge">EXCALIDRAW ARCHITECTURE CANVAS</span>
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
"""

    if 'id="flowchartModal"' not in code:
        code = code.replace("</body>", modal_html + "\n</body>")

    # Update deck navigation
    if 'class="nav-btn canvas-link"' not in code:
        code = code.replace('<span id="slideCounter" style="margin: 0 4px; font-weight: 700;">1 / 19</span>',
                            '<span id="slideCounter" style="margin: 0 4px; font-weight: 700;">1 / 19</span>\n  <a href="excalidraw_canvas_viewer.html" target="_blank" class="nav-btn canvas-link" title="Open Multi-Tab Excalidraw Canvas Viewer" style="text-decoration:none; font-size:12px; margin-left:6px; color:#E8E6DF;">📐 Canvas</a>')

    # 7. Add JS functions for flowcharts and modal controller
    js_controllers = """
    // FLOWCHART VIEW SWITCHER
    window.setSlideView = function(slideNum, viewType) {
      const cardsPanel = document.getElementById(`slide-${slideNum}-cards`);
      const flowPanel = document.getElementById(`slide-${slideNum}-flowchart`);
      const slideElem = document.querySelector(`.slide[data-slide="${slideNum}"]`);
      if (!slideElem) return;
      const btns = slideElem.querySelectorAll('.flowchart-toggle-group .toggle-btn:not(.expand-btn):not(.link-btn)');

      if (viewType === 'cards') {
        if (cardsPanel) cardsPanel.classList.add('active');
        if (flowPanel) flowPanel.classList.remove('active');
        if (btns[0]) btns[0].classList.add('active');
        if (btns[1]) btns[1].classList.remove('active');
      } else {
        if (cardsPanel) cardsPanel.classList.remove('active');
        if (flowPanel) flowPanel.classList.add('active');
        if (btns[0]) btns[0].classList.remove('active');
        if (btns[1]) btns[1].classList.add('active');
      }
    };

    // IN-SLIDE CANVAS ZOOM CONTROLLER
    const zoomLevels = { 7: 1, 8: 1, 10: 1, 12: 1 };
    window.zoomCanvas = function(slideNum, factor) {
      zoomLevels[slideNum] = Math.min(2.5, Math.max(0.4, (zoomLevels[slideNum] || 1) * factor));
      const el = document.getElementById(`svg-wrap-${slideNum}`);
      if (el) el.style.transform = `scale(${zoomLevels[slideNum]})`;
    };
    window.resetCanvas = function(slideNum) {
      zoomLevels[slideNum] = 1;
      const el = document.getElementById(`svg-wrap-${slideNum}`);
      if (el) el.style.transform = `scale(1)`;
    };

    // FULLSCREEN MODAL CONTROLLER
    let modalZoom = 1;
    const flowchartModal = document.getElementById('flowchartModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalDownloadBtn = document.getElementById('modalDownloadBtn');
    const modalSvgContainer = document.getElementById('modalSvgContainer');

    const flowchartData = {
      tier1: {
        title: "Tier 1: Essential Revenue Automation Flowchart (2,275px Full Vision)",
        download: "tier1_essential_automation_flowchart.excalidraw",
        svgId: "svg-wrap-7"
      },
      waterfall: {
        title: "Tier 1 Lead Intelligence // Waterfall Enrichment Pipeline (State Machine)",
        download: "waterfall_enrichment_engine.excalidraw",
        svgId: "svg-wrap-8"
      },
      tier2: {
        title: "Tier 2: Governed Decision Flow & Decision Contract Gate",
        download: "tier2_governed_intelligence_flowchart.excalidraw",
        svgId: "svg-wrap-10"
      },
      tier3: {
        title: "Tier 3: Autonomous Revenue Platform Flowchart (Closed-Loop Flywheel)",
        download: "tier3_autonomous_platform_flowchart.excalidraw",
        svgId: "svg-wrap-12"
      }
    };

    window.openFlowchartModal = function(key) {
      const data = flowchartData[key];
      if (!data) return;
      modalTitle.textContent = data.title;
      modalDownloadBtn.href = data.download;
      const sourceSvg = document.getElementById(data.svgId);
      if (sourceSvg) {
        modalSvgContainer.innerHTML = sourceSvg.innerHTML;
      }
      modalZoom = 1;
      modalSvgContainer.style.transform = "scale(1)";
      flowchartModal.classList.add('open');
    };

    window.closeFlowchartModal = function() {
      flowchartModal.classList.remove('open');
    };

    window.zoomModal = function(factor) {
      modalZoom = Math.min(3.0, Math.max(0.3, modalZoom * factor));
      modalSvgContainer.style.transform = `scale(${modalZoom})`;
    };

    window.resetModalZoom = function() {
      modalZoom = 1;
      modalSvgContainer.style.transform = "scale(1)";
    };

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && flowchartModal && flowchartModal.classList.contains('open')) {
        closeFlowchartModal();
      }
    });
"""

    if "window.setSlideView" not in code:
        code = code.replace("showSlide(totalSlides - 1);\n      }\n    });",
                            "showSlide(totalSlides - 1);\n      }\n    });\n" + js_controllers)

    # 8. Update PowerPoint slides notes and diagram specifications
    pptx_updates = [
        ("s7.notes_slide",
         "EXCALIDRAW STATE-MACHINE SPECIFICATION: tier1_essential_automation_flowchart.excalidraw\\n"
         "Architecture: Terminal Start (Raw Lead) -> Deduplication -> Circuit Breaker (Rate Limit) -> "
         "Section 5 TMG Legal Impressum -> 3-Stage Waterfall -> ICP Qualification Agent -> "
         "Personalization Agent -> Sidy WhatsApp 1-Tap Gate -> Dolibarr CRM Sync -> Temporal Day-4 & Day-25 Timers.\\n"
         "Inspect in browser: excalidraw_canvas_viewer.html#t1"),
        ("s8.notes_slide",
         "EXCALIDRAW STATE-MACHINE SPECIFICATION: waterfall_enrichment_engine.excalidraw\\n"
         "Stage 0 (Section 5 TMG Impressum, 0 EUR, 48% find) -> Stage 1 (GitLeads bulk, 0.005 EUR, 24%) -> "
         "Stage 2 (Prospeo, 0.02 EUR, 18%) -> Stage 3 (LeadMagic Mobile, 0.05 EUR) -> Deliverability Gate (<1.5% bounce).\\n"
         "Inspect in browser: excalidraw_canvas_viewer.html#wf"),
        ("s10.notes_slide",
         "EXCALIDRAW STATE-MACHINE SPECIFICATION: tier2_governed_intelligence_flowchart.excalidraw\\n"
         "Signal Ingest -> LangGraph Creative Loop -> Typed Decision Contract -> Schema Gate -> "
         "Policy Engine Check -> Budget Delta Gate (>5 EUR requires Sidy 1-tap sign-off) -> "
         "Meta API Dispatch -> Post-Action Query Verification -> Immutable PostgreSQL Audit Ledger.\\n"
         "Inspect in browser: excalidraw_canvas_viewer.html#t2"),
        ("s12.notes_slide",
         "EXCALIDRAW STATE-MACHINE SPECIFICATION: tier3_autonomous_platform_flowchart.excalidraw\\n"
         "Commercial Event Bus -> Shared Revenue State Graph -> Multi-Agent Domain Team (Acquisition, Creative, RevOps) -> "
         "Continuous Experimentation -> Automated Circuit Breakers -> MCP Dynamic Tool Layer -> Closed-Loop Flywheel.\\n"
         "Inspect in browser: excalidraw_canvas_viewer.html#t3")
    ]

    for target, note in pptx_updates:
        marker = f"add_footer({target.split('.')[0]}, "
        note_code = f"    {target}.notes_text_frame.text = '''{note}'''\n"
        if note_code not in code and marker in code:
            code = code.replace(marker, note_code + "    " + marker)

    with open(gen_script_path, "w", encoding="utf-8") as f:
        f.write(code)
    
    print("[SUCCESS] generate_tiered_presentation.py successfully updated with Excalidraw flowcharts and modal controllers!")

if __name__ == "__main__":
    main()
