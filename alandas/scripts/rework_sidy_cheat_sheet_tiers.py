"""
rework_sidy_cheat_sheet_tiers.py
Applies Cyril's feedback:
1. Slide 10: Remove the 12-month timeline. Present Tier 1, Tier 2, Tier 3 choices clearly so Sidy gets to pick.
2. Slide 7 (and Slides 6 & 8): Even out writing across the whitespace, increase font size significantly so Sidy can read effortlessly without squinting.
3. Rebuilds the PDF using the `pdf` skill toolset (Chromium print + pypdf metadata + pypdfium2 verification).
4. Rebuilds the PowerPoint deck (PPTX).
"""

import os
import re
import subprocess
import pypdf
import pypdfium2 as pdfium

def rework_deck():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck.html")
    pdf_out = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck.pdf")
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # =========================================================================
    # 1. SLIDE 6: Even out vertical spacing & increase text size (Tier 1)
    # =========================================================================
    slide6_old_regex = r'(<div id="slide-6-cards" class="view-panel active">)(.*?)(</div>\s*<!-- View 2: Flowchart Preview -->)'
    slide6_new = """
          <div style="display: grid; grid-template-columns: 1.22fr 1fr; gap: 32px; height: 100%;">
            <div class="card accent-olive" style="padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-olive" style="font-size: 14px;">How the 5 Steps Work // 100% Human-in-the-Loop</span>
                <h3 class="card-title" style="font-size: 28px; margin-top: 4px;">Read ➔ Analyze ➔ Propose ➔ Approve ➔ Execute</h3>
                <p style="font-size: 18px; color: var(--text-muted); margin: 6px 0 16px 0;">Sidy is in full control. The bot gathers facts, but Sidy taps Approve before anything happens.</p>
              </div>

              <div style="display: flex; flex-direction: column; justify-content: space-between; flex: 1; gap: 12px; margin-bottom: 16px;">
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--olive);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">1. Read: Public Cafe Ingestion</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Scans Google Maps &amp; Instagram for cafes with &gt;30 seats in Berlin &amp; Munich.</div>
                </div>
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--olive);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">2. Analyze: ICP Concept Fit</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Evaluates beverage menu, terrace seating, specialty coffee focus, and owner names.</div>
                </div>
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--olive);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">3. Propose: Warm Personalized Pitch</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">AI drafts warm WhatsApp message offering the €19 teapot kit with 100% crate credit.</div>
                </div>
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--olive);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">4. Human Approves: Sidy's Safety Gate</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Draft lands on Sidy's phone. Sidy taps <strong>Approve</strong>. The bot never sends unreviewed messages.</div>
                </div>
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--olive);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">5. Execute: Temporal &amp; Dolibarr Sync</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Dispatches WhatsApp via API, creates Dolibarr CRM lead, and sets Day-4 follow-up.</div>
                </div>
              </div>

              <div class="callout-box" style="padding: 14px 18px; font-size: 15.5px; font-weight: 700; background: var(--olive-light); border: 1.5px solid var(--olive-border); border-radius: 10px; color: var(--olive-dark);">
                Commercial Impact: Zero brand risk • Saves 15+ hrs/week • Target: 25 ➔ 40 Cafes (~€5,000/mo).
              </div>
            </div>

            <div class="card" style="padding: 24px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #FAF8F2;">
              <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 800; color: var(--olive); letter-spacing: 0.05em; margin-bottom: 12px;">WHAT DOLIBARR CRM LOOKS LIKE // NOTE ➔ INVOICE</div>
              <img src="assets/mockup_dolibarr_crm.png" alt="Dolibarr CRM Mockup" style="width: 100%; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.12);">
            </div>
          </div>
        """
    content = re.sub(slide6_old_regex, r'\1' + slide6_new + r'\3', content, flags=re.DOTALL)

    # =========================================================================
    # 2. SLIDE 7: Even out vertical spacing & increase text size (Tier 2)
    # =========================================================================
    slide7_cards_old_regex = r'(<div id="slide-7-cards" class="view-panel active">)(.*?)(</div>\s*<!-- View 2: Flowchart Preview -->)'
    slide7_cards_new = """
          <div style="display: grid; grid-template-columns: 1.22fr 1fr; gap: 32px; height: 100%;">
            <div class="card accent-ochre" style="padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-ochre" style="font-size: 14px;">The Real-World Example // Financial Guardrails</span>
                <h3 class="card-title" style="font-size: 28px; margin-top: 4px;">Increasing Meta Ad Budget by +30%</h3>
                <p style="font-size: 18px; color: var(--text-muted); margin: 6px 0 16px 0;">How unbreakable Policy Engines protect Sidy's bank account and brand integrity:</p>
              </div>

              <div style="display: flex; flex-direction: column; justify-content: space-between; flex: 1; gap: 12px; margin-bottom: 16px;">
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--ochre);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">1. AI Observes Campaign Telemetry</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Berlin brunch ad achieves 4.2x ROAS. System proposes raising daily budget from €30 ➔ €39/day (+€9).</div>
                </div>
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--ochre);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">2. Hard Policy Ceiling Check</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Policy Engine checks safety rules: Is €39 under our maximum €50/day hard cap? (PASSED).</div>
                </div>
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--ochre);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">3. Human Sign-Off Threshold Check</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Rule triggers: Any budget increase &gt;€5 strictly requires human sign-off. (TRIGGERED).</div>
                </div>
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--ochre);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">4. Sidy Receives 1-Tap WhatsApp Ping</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Sidy's phone dings: <em>"Approve +€9/day for Berlin Brunch ad?"</em> Sidy taps Approve.</div>
                </div>
                <div style="background: var(--card-alt); padding: 13px 18px; border-radius: 10px; border-left: 5px solid var(--ochre);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">5. Post-Action State Verification</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">AI updates Meta API, then immediately re-queries Meta to confirm state is €39.00 and NOT €390.00.</div>
                </div>
              </div>

              <div class="callout-box" style="padding: 14px 18px; font-size: 15.5px; font-weight: 700; background: var(--ochre-light); border: 1.5px solid var(--ochre-border); border-radius: 10px; color: var(--ochre-dark);">
                Commercial Value: Zero runaway spend • Zero pricing leaks • Target: 40 ➔ 70 Cafes (~€12,000/mo).
              </div>
            </div>

            <div class="card" style="padding: 18px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #FAF8F2;">
              <div style="font-family: var(--font-mono); font-size: 11.5px; font-weight: 800; color: var(--ochre-dark); letter-spacing: 0.05em; margin-bottom: 8px;">GOVERNED DECISION CONTRACT GATE</div>
              <img src="assets/tier2_flowchart.png" alt="Tier 2 Decision Contract Flowchart" style="max-height: 590px; width: auto; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
            </div>
          </div>
        """
    content = re.sub(slide7_cards_old_regex, r'\1' + slide7_cards_new + r'\3', content, flags=re.DOTALL)

    # =========================================================================
    # 3. SLIDE 8: Even out vertical spacing & increase text size (Tier 3)
    # =========================================================================
    slide8_cards_old_regex = r'(<div id="slide-8-cards" class="view-panel active">)(.*?)(</div>\s*<!-- View 2: Flowchart Preview -->)'
    slide8_cards_new = """
          <div style="display: grid; grid-template-columns: 1.22fr 1fr; gap: 32px; height: 100%;">
            <div class="card accent-forest" style="padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-forest" style="font-size: 14px;">The Closed-Loop Flywheel // Cross-City Operations</span>
                <h3 class="card-title" style="font-size: 28px; margin-top: 4px;">Munich Terrace Summer Scenario</h3>
                <p style="font-size: 18px; color: var(--text-muted); margin: 6px 0 16px 0;">How sales, inventory, and marketing coordinate automatically without human friction:</p>
              </div>

              <div style="display: flex; flex-direction: column; justify-content: space-between; flex: 1; gap: 14px; margin-bottom: 16px;">
                <div style="background: var(--card-alt); padding: 15px 18px; border-radius: 10px; border-left: 5px solid var(--forest);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">1. Reorder Velocity Spike Trigger</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">In July, Munich cafes reorder Earl Grey and Berry Hibiscus 2x faster for outdoor iced tea.</div>
                </div>
                <div style="background: var(--card-alt); padding: 15px 18px; border-radius: 10px; border-left: 5px solid var(--forest);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">2. Ops Signals Marketing Agent</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">The system flags that terrace iced tea demand is surging in Munich and triggers ad creative generation.</div>
                </div>
                <div style="background: var(--card-alt); padding: 15px 18px; border-radius: 10px; border-left: 5px solid var(--forest);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">3. Targeted Creative Deployment</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Marketing Agent writes ad copy: <em>"Serving iced tea on your Munich terrace? Try our €19 barista kit."</em></div>
                </div>
                <div style="background: var(--card-alt); padding: 15px 18px; border-radius: 10px; border-left: 5px solid var(--forest);">
                  <div style="font-size: 18px; font-weight: 700; color: var(--text-main);">4. Autonomous Scaling &amp; Warehouse Sync</div>
                  <div style="font-size: 15.5px; color: var(--text-muted); margin-top: 2px;">Launches tests, validates high conversion, allocates ad budget, and reserves warehouse stock automatically.</div>
                </div>
              </div>

              <div class="callout-box" style="padding: 14px 18px; font-size: 15.5px; font-weight: 700; background: var(--forest-light); border: 1.5px solid var(--forest); border-radius: 10px; color: var(--forest-dark);">
                Founder Independence: Zero linear headcount • Automatic circuit breakers • Sidy is full-time CEO (100+ Cafes, €20k–€30k/mo).
              </div>
            </div>

            <div class="card" style="padding: 18px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #FAF8F2;">
              <div style="font-family: var(--font-mono); font-size: 11.5px; font-weight: 800; color: var(--forest); letter-spacing: 0.05em; margin-bottom: 8px;">AUTONOMOUS COMMERCIAL FLYWHEEL</div>
              <img src="assets/tier3_flowchart.png" alt="Tier 3 Flywheel Flowchart" style="max-height: 590px; width: auto; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
            </div>
          </div>
        """
    content = re.sub(slide8_cards_old_regex, r'\1' + slide8_cards_new + r'\3', content, flags=re.DOTALL)

    # =========================================================================
    # 4. SLIDE 10: Rework to Tier Selection (NO 12-Month Timeline)
    # =========================================================================
    slide10_old_regex = r'(<div class="slide" data-slide="10">)(.*?)(<div class="slide-footer">)'
    slide10_new = """
      <div class="slide-header">
        <div class="kicker">06 // Architecture Comparison &amp; Selection</div>
        <h2 class="slide-title">Choose Your Tier: Modular Revenue Architecture</h2>
        <p class="slide-subtitle">
          Sidy gets to choose which tier fits his current stage and comfort. Every tier is modular—you never discard code or rebuild from scratch.
        </p>
      </div>

      <div class="slide-body" style="display: flex; flex-direction: column; justify-content: space-between;">
        <div class="grid-3" style="gap: 28px; flex: 1;">
          <!-- Tier 1 Card -->
          <div class="card accent-olive highlight" style="padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <span class="card-tag tag-olive" style="font-size: 13.5px;">Option 01 // Recommended Start</span>
              <h3 class="card-title" style="font-size: 26px; margin-top: 4px; color: var(--olive-dark);">Tier 1: Essential</h3>
              <div style="font-size: 16px; font-weight: 700; color: var(--olive); margin-bottom: 12px;">The Tireless Assistant (Sidy is Pilot)</div>
              
              <ul class="bullet-list" style="font-size: 15.5px; line-height: 1.5; gap: 8px;">
                <li><strong>What It Solves:</strong> Stops 20+ hours of manual Google Maps scraping &amp; Instagram messaging.</li>
                <li><strong>Core Engine:</strong> Legal Impressum § 5 TMG scraper, AI draft generator, Dolibarr CRM invoice OCR.</li>
                <li><strong>Human Control:</strong> Sidy approves every outbound message and invoice on WhatsApp.</li>
                <li><strong>Sidy's Routine:</strong> Spends just <strong>30 mins/day</strong> on WhatsApp reviews.</li>
              </ul>
            </div>

            <div style="margin-top: 16px; padding: 14px 18px; background: var(--olive-light); border-radius: 10px; border: 1.5px solid var(--olive-border);">
              <div style="font-size: 13px; font-weight: 700; color: var(--olive); text-transform: uppercase;">Target Scale &amp; Cashflow</div>
              <div style="font-size: 20px; font-weight: 800; color: var(--olive-dark); margin-top: 2px;">25 ➔ 40 Partner Cafes</div>
              <div style="font-size: 15px; color: var(--text-muted);">~€5,000 / month recurring cashflow</div>
            </div>
          </div>

          <!-- Tier 2 Card -->
          <div class="card accent-ochre" style="padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <span class="card-tag tag-ochre" style="font-size: 13.5px;">Option 02 // Growth &amp; Protection</span>
              <h3 class="card-title" style="font-size: 26px; margin-top: 4px; color: var(--ochre-dark);">Tier 2: Governed</h3>
              <div style="font-size: 16px; font-weight: 700; color: var(--ochre-dark); margin-bottom: 12px;">Smart Assistant with Guardrails</div>
              
              <ul class="bullet-list" style="font-size: 15.5px; line-height: 1.5; gap: 8px;">
                <li><strong>What It Solves:</strong> Eliminates silent cafe churn and prevents runaway ad spend.</li>
                <li><strong>Core Engine:</strong> Policy Engine (+30% ad budget rules, hard caps), Day-25 predictive refill alerts.</li>
                <li><strong>Human Control:</strong> Any budget change &gt;€5 requires Sidy's 1-tap WhatsApp sign-off.</li>
                <li><strong>Sidy's Routine:</strong> Admin drops to <strong>&lt; 4 hours/week</strong>. Sidy prepares his notice.</li>
              </ul>
            </div>

            <div style="margin-top: 16px; padding: 14px 18px; background: var(--ochre-light); border-radius: 10px; border: 1.5px solid var(--ochre-border);">
              <div style="font-size: 13px; font-weight: 700; color: var(--ochre-dark); text-transform: uppercase;">Target Scale &amp; Cashflow</div>
              <div style="font-size: 20px; font-weight: 800; color: var(--ochre-dark); margin-top: 2px;">40 ➔ 70 Partner Cafes</div>
              <div style="font-size: 15px; color: var(--text-muted);">~€12,000 / month recurring cashflow</div>
            </div>
          </div>

          <!-- Tier 3 Card -->
          <div class="card accent-forest" style="padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <span class="card-tag tag-forest" style="font-size: 13.5px;">Option 03 // Enterprise Scale</span>
              <h3 class="card-title" style="font-size: 26px; margin-top: 4px; color: var(--forest-dark);">Tier 3: Autonomous</h3>
              <div style="font-size: 16px; font-weight: 700; color: var(--forest); margin-bottom: 12px;">Self-Running Multi-City Flywheel</div>
              
              <ul class="bullet-list" style="font-size: 15.5px; line-height: 1.5; gap: 8px;">
                <li><strong>What It Solves:</strong> Scales across Germany, Austria &amp; Switzerland without hiring sales reps.</li>
                <li><strong>Core Engine:</strong> Closed-loop flywheel connecting cafe reorders to Meta ad creative; warehouse sync.</li>
                <li><strong>Human Control:</strong> Automatic circuit breakers halt anomalies; Sidy acts as Chairman.</li>
                <li><strong>Sidy's Routine:</strong> 100% full-time independent founder &amp; CEO (&lt; 2 hrs/week oversight).</li>
              </ul>
            </div>

            <div style="margin-top: 16px; padding: 14px 18px; background: var(--forest-light); border-radius: 10px; border: 1.5px solid var(--forest); border-radius: 10px;">
              <div style="font-size: 13px; font-weight: 700; color: var(--forest); text-transform: uppercase;">Target Scale &amp; Cashflow</div>
              <div style="font-size: 20px; font-weight: 800; color: var(--forest-dark); margin-top: 2px;">100+ Partner Cafes</div>
              <div style="font-size: 15px; color: var(--text-muted);">€20,000–€30,000 / month recurring</div>
            </div>
          </div>
        </div>

        <div class="callout-box" style="margin-top: 20px; padding: 16px 24px; background: var(--card-bg); border: 1.5px solid var(--border); border-radius: 12px; font-size: 16.5px; font-weight: 700; color: var(--text-main); display: flex; justify-content: space-between; align-items: center;">
          <span>THE FREEDOM PRINCIPLE: Sidy chooses where to begin. No time lock-in. Tier 1 gives immediate relief on Day 1; higher tiers unlock whenever Sidy wants to scale.</span>
          <span style="color: var(--olive); font-family: var(--font-mono); font-size: 14px;">100% MODULAR ARCHITECTURE</span>
        </div>
      </div>
    """
    content = re.sub(slide10_old_regex, r'\1' + slide10_new + r'\3', content, flags=re.DOTALL)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] HTML presentation successfully updated.")

    # =========================================================================
    # 5. RENDER PDF WITH CHROMIUM & INJECT METADATA VIA PYPDF
    # =========================================================================
    html_print = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck_Print.html")
    
    print_css = """
    <style id="print-perfect-styles">
      @page {
        size: 1920px 1080px;
        margin: 0;
      }
      @media print, screen {
        html, body {
          width: 1920px !important;
          height: auto !important;
          overflow: visible !important;
          background: #0C0F0C !important;
          margin: 0 !important;
          padding: 0 !important;
        }
        .deck-viewport {
          position: static !important;
          display: block !important;
          overflow: visible !important;
          width: 1920px !important;
          height: auto !important;
          background: #0C0F0C !important;
        }
        .deck-stage {
          position: static !important;
          width: 1920px !important;
          height: auto !important;
          transform: none !important;
          box-shadow: none !important;
          border-radius: 0 !important;
          display: block !important;
          background: transparent !important;
        }
        .slide {
          position: relative !important;
          width: 1920px !important;
          height: 1080px !important;
          display: flex !important;
          opacity: 1 !important;
          visibility: visible !important;
          pointer-events: auto !important;
          page-break-after: always !important;
          break-after: page !important;
          page-break-inside: avoid !important;
          break-inside: avoid !important;
          margin: 0 !important;
          padding: 64px 84px 54px 84px !important;
          background: #F9F7F2 !important;
          background-image: radial-gradient(1400px 900px at 50% 0%, #FFFFFF 0%, #F9F7F2 60%, #EDE7D8 100%) !important;
          box-sizing: border-box !important;
        }
        .deck-nav, .flowchart-modal, .flowchart-toggle-group, .modal-backdrop {
          display: none !important;
        }
        .view-panel {
          display: none !important;
        }
        .view-panel.active, #slide-6-cards, #slide-7-cards, #slide-8-cards {
          display: flex !important;
        }
      }
    </style>
    """
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    html_print_content = html_content.replace("</head>", f"{print_css}\n</head>")
    with open(html_print, "w", encoding="utf-8") as f:
        f.write(html_print_content)

    print("Rendering updated PDF via Chromium Engine...")
    url = "file:///" + html_print.replace(os.sep, "/")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=5000",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_out}",
        url
    ]
    subprocess.run(cmd, check=True)

    print("Injecting Executive Metadata with pypdf...")
    reader = pypdf.PdfReader(pdf_out)
    writer = pypdf.PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    writer.add_metadata({
        "/Title": "Alandas Tea Berlin — Sidy's Revenue Roadmap & Cheat Sheet",
        "/Author": "Cyril Uzochukwu & Sidy Sow",
        "/Subject": "Architecture Comparison: Choose Between Tier 1, Tier 2, and Tier 3",
        "/Creator": "Alandas Executive Architecture System (PDF Skill)",
        "/Producer": "Google Antigravity & PDF Skill Toolset",
        "/Keywords": "Alandas, B2B Tea, Dolibarr CRM, Temporal, WhatsApp Copilot, Berlin, Munich"
    })
    with open(pdf_out, "wb") as f_out:
        writer.write(f_out)

    if os.path.exists(html_print):
        os.remove(html_print)

    print("Rendering Proof Images with pypdfium2...")
    pdf_doc = pdfium.PdfDocument(pdf_out)
    for i, page in enumerate(pdf_doc):
        bmp = page.render(scale=1.0)
        bmp.to_pil().save(os.path.join(base_dir, f"page_proof_{i+1}.png"), "PNG")
    print(f"[ALL DONE] Updated PDF exported ({os.path.getsize(pdf_out)} bytes). Proofs rendered.")

if __name__ == "__main__":
    rework_deck()
