"""
finalize_executive_deck_skill.py
Polishes Alandas_Sidy_Cheat_Sheet_Deck.html so every slide is 100% balanced with zero whitespace voids:
- Embeds Tier 2 flowchart in Slide 7 Executive Cards view
- Embeds Tier 3 flowchart in Slide 8 Executive Cards view
- Adds bottom anchor banners to Slides 2, 9, 10
- Enriches Slide 11 step cards with bullet points
- Polishes Slide 4 left card spacing
- Uses the `pdf` skill pipeline to render the definitive, ultra-luxury 16:9 PDF with full metadata.
"""

import os
import re
import subprocess
import pypdf
import pypdfium2 as pdfium

def polish_deck():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck.html")
    pdf_out = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck.pdf")
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Slide 2: Add bottom anchor banner
    slide2_target = r'(<div class="slide" data-slide="2">.*?<div class="slide-body">.*?<div class="grid-2">.*?</div>\s*)(</div>\s*<div class="slide-footer">)'
    slide2_banner = """
        <div class="callout-box" style="margin-top: 18px; padding: 18px 24px; background: var(--olive-light); border: 1.5px solid var(--olive-border); border-radius: 12px; font-size: 16.5px; font-weight: 700; color: var(--olive-dark);">
          THE CORE METRIC: Every system and architecture tier Cyril designs serves ONE metric — Getting Sidy back to Berlin as his own full-time boss.
        </div>
      """
    if "THE CORE METRIC: Every system" not in content:
        content = re.sub(slide2_target, r'\1' + slide2_banner + r'\2', content, flags=re.DOTALL)

    # 2. Slide 4: Perfect spacing for 6 stages
    slide4_old_regex = r'(<div class="slide" data-slide="4">.*?<div class="slide-body">)(.*?)(</div>\s*<div class="slide-footer">)'
    slide4_new_body = """
        <div style="display: grid; grid-template-columns: 1.22fr 1fr; gap: 32px; height: 100%;">
          <div class="card" style="padding: 28px; display: flex; flex-direction: column; justify-content: flex-start; gap: 14px;">
            <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 800; color: var(--olive); letter-spacing: 0.05em; margin-bottom: 4px;">THE 6-STAGE REVENUE PIPELINE</div>
            <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--olive);">
              <div style="font-weight: 700; color: var(--olive); font-size: 16px;">01 // DISCOVER: Specialty Cafe Ingestion</div>
              <div style="font-size: 15px; color: var(--text-muted); margin-top: 2px;">Scans Google Maps &amp; Instagram for &gt;30-seat brunch cafes in Berlin &amp; Munich.</div>
            </div>
            <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--olive);">
              <div style="font-weight: 700; color: var(--olive); font-size: 16px;">02 // ENRICH: Legal Impressum § 5 TMG Waterfall</div>
              <div style="font-size: 15px; color: var(--text-muted); margin-top: 2px;">Extracts verified owner WhatsApp numbers via German public registries for €0.00.</div>
            </div>
            <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--ochre);">
              <div style="font-weight: 700; color: var(--ochre-dark); font-size: 16px;">03 // OFFER: Trojan Horse €19 Trial Starter Kit</div>
              <div style="font-size: 15px; color: var(--text-muted); margin-top: 2px;">Pitches the borosilicate teapot kit (100% credited back on first wholesale crate).</div>
            </div>
            <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--ochre);">
              <div style="font-weight: 700; color: var(--ochre-dark); font-size: 16px;">04 // 1-TAP APPROVAL: Sidy Retains 100% Authority</div>
              <div style="font-size: 15px; color: var(--text-muted); margin-top: 2px;">AI drafts warm personalized message; Sidy reviews on his phone &amp; taps 'Approve'.</div>
            </div>
            <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--forest);">
              <div style="font-weight: 700; color: var(--forest); font-size: 16px;">05 // INVOICE OCR: Automated Dolibarr CRM Sync</div>
              <div style="font-size: 15px; color: var(--text-muted); margin-top: 2px;">AI deciphers handwritten barista notes into draft German tax-compliant invoices.</div>
            </div>
            <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--forest);">
              <div style="font-weight: 700; color: var(--forest); font-size: 16px;">06 // RETENTION: Automated Day-25 Refill Alerts</div>
              <div style="font-size: 15px; color: var(--text-muted); margin-top: 2px;">Automated WhatsApp reminder before cafes run out of tea, ending silent churn.</div>
            </div>
          </div>
          <div class="card" style="padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #FAF8F2;">
            <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 800; color: var(--ochre-dark); letter-spacing: 0.05em; margin-bottom: 12px;">WHAT SIDY SEES ON HIS IPHONE // 1-TAP APPROVAL</div>
            <img src="assets/mockup_whatsapp_tier1.png" alt="WhatsApp 1-Tap Approval Mockup" style="max-height: 590px; width: auto; filter: drop-shadow(0 15px 35px rgba(0,0,0,0.2)); border-radius: 36px;">
          </div>
        </div>
      """
    content = re.sub(slide4_old_regex, r'\1' + slide4_new_body + r'\3', content, flags=re.DOTALL)

    # 3. Slide 7: Embed Tier 2 Flowchart in Cards View
    slide7_cards_old_regex = r'(<div id="slide-7-cards" class="view-panel active">)(.*?)(</div>\s*<!-- View 2: Flowchart Preview -->)'
    slide7_cards_new = """
          <div style="display: grid; grid-template-columns: 1.22fr 1fr; gap: 32px; height: 100%;">
            <div class="card accent-ochre" style="padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-ochre">The Real-World Example</span>
                <h3 class="card-title" style="font-size: 24px;">Increasing Meta Ad Budget by +30%</h3>
                <p class="card-desc" style="font-size: 16px; margin: 8px 0 14px 0;">How the Policy Engine protects Sidy's money and brand:</p>
                <ol style="display: flex; flex-direction: column; gap: 10px; padding-left: 20px; font-size: 15.5px; line-height: 1.45; color: var(--text-main);">
                  <li><strong>AI Observes:</strong> Berlin brunch ad has a 4.2x ROAS. Suggests raising €30 ➔ €39/day (+€9).</li>
                  <li><strong>Hard Ceiling Check:</strong> Is €39 under our maximum €50/day hard cap? (YES).</li>
                  <li><strong>Threshold Check:</strong> Is delta (&gt;€5) requiring human sign-off? (YES).</li>
                  <li><strong>Sidy Notified:</strong> Phone dings: <em>[Approve +€9/day for Berlin Brunch Ad?]</em>.</li>
                  <li><strong>Verify State:</strong> AI calls Meta API, then re-queries Meta to confirm €39.00 (NOT €390.00).</li>
                </ol>
              </div>
              <div class="callout-box" style="margin-top: 14px; font-size: 14.5px;">
                <strong>Commercial Value:</strong> Zero runaway spend • Zero pricing leaks • 40 ➔ 70 Cafes (~€12k/mo).
              </div>
            </div>
            <div class="card" style="padding: 18px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #FAF8F2;">
              <div style="font-family: var(--font-mono); font-size: 11.5px; font-weight: 800; color: var(--ochre-dark); letter-spacing: 0.05em; margin-bottom: 8px;">GOVERNED DECISION CONTRACT GATE</div>
              <img src="assets/tier2_flowchart.png" alt="Tier 2 Decision Contract Flowchart" style="max-height: 590px; width: auto; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
            </div>
          </div>
        """
    content = re.sub(slide7_cards_old_regex, r'\1' + slide7_cards_new + r'\3', content, flags=re.DOTALL)

    # 4. Slide 8: Embed Tier 3 Flowchart in Cards View
    slide8_cards_old_regex = r'(<div id="slide-8-cards" class="view-panel active">)(.*?)(</div>\s*<!-- View 2: Flowchart Preview -->)'
    slide8_cards_new = """
          <div style="display: grid; grid-template-columns: 1.22fr 1fr; gap: 32px; height: 100%;">
            <div class="card accent-forest" style="padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-forest">The Closed-Loop Flywheel</span>
                <h3 class="card-title" style="font-size: 24px;">Munich Terrace Summer Scenario</h3>
                <p class="card-desc" style="font-size: 16px; margin: 8px 0 14px 0;">How departments talk to each other without human friction:</p>
                <ol style="display: flex; flex-direction: column; gap: 10px; padding-left: 20px; font-size: 15.5px; line-height: 1.45; color: var(--text-main);">
                  <li><strong>Reorder Surge:</strong> In July, Munich cafes reorder Earl Grey 2x faster for terrace iced tea.</li>
                  <li><strong>Ops Alerts Marketing:</strong> The system identifies that terrace iced tea is surging in Munich.</li>
                  <li><strong>Automated Campaign:</strong> Marketing Agent writes ad copy: <em>"Serving iced tea on your Munich terrace? Try our €19 kit."</em></li>
                  <li><strong>Autonomous Optimization:</strong> Launches tests, validates conversion, and scales budget without manual work.</li>
                </ol>
              </div>
              <div class="callout-box" style="margin-top: 14px; font-size: 14.5px;">
                <strong>Founder Independence:</strong> Zero linear headcount • Automatic circuit breakers • Sidy is full-time CEO (100+ Cafes, €20k–€30k/mo).
              </div>
            </div>
            <div class="card" style="padding: 18px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #FAF8F2;">
              <div style="font-family: var(--font-mono); font-size: 11.5px; font-weight: 800; color: var(--forest); letter-spacing: 0.05em; margin-bottom: 8px;">AUTONOMOUS COMMERCIAL FLYWHEEL</div>
              <img src="assets/tier3_flowchart.png" alt="Tier 3 Flywheel Flowchart" style="max-height: 590px; width: auto; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
            </div>
          </div>
        """
    content = re.sub(slide8_cards_old_regex, r'\1' + slide8_cards_new + r'\3', content, flags=re.DOTALL)

    # 5. Slide 9: Add bottom architectural banner
    slide9_target = r'(<div class="slide" data-slide="9">.*?<div class="slide-body">.*?<div class="grid-3">.*?</div>\s*)(</div>\s*<div class="slide-footer">)'
    slide9_banner = """
        <div class="callout-box" style="margin-top: 18px; padding: 18px 24px; background: var(--ochre-light); border: 1.5px solid var(--ochre-border); border-radius: 12px; font-size: 16px; font-weight: 700; color: var(--ochre-dark);">
          CORE ARCHITECTURAL DEFENSE: Zero low-code toys. Zero lost data via Temporal state durability. Zero runaway spend via deterministic Policy Engines.
        </div>
      """
    if "CORE ARCHITECTURAL DEFENSE: Zero low-code toys" not in content:
        content = re.sub(slide9_target, r'\1' + slide9_banner + r'\2', content, flags=re.DOTALL)

    # 6. Slide 10: Add bottom freedom destination banner
    slide10_target = r'(<div class="slide" data-slide="10">.*?<div class="slide-body">.*?<div class="grid-3">.*?</div>\s*)(</div>\s*<div class="slide-footer">)'
    slide10_banner = """
        <div class="callout-box" style="margin-top: 18px; padding: 18px 24px; background: var(--forest-light); border: 1.5px solid var(--forest); border-radius: 12px; font-size: 16px; font-weight: 700; color: var(--forest-dark);">
          THE FREEDOM DESTINATION: 100 Partner Cafes across Berlin, Munich &amp; Hamburg = €15,000 to €30,000 / month recurring revenue. Sidy is full-time CEO.
        </div>
      """
    if "THE FREEDOM DESTINATION: 100 Partner Cafes" not in content:
        content = re.sub(slide10_target, r'\1' + slide10_banner + r'\2', content, flags=re.DOTALL)

    # 7. Slide 11: Enriched 4 Step Cards
    slide11_old_regex = r'(<div class="slide" data-slide="11">.*?<div class="slide-body">)(.*?)(</div>\s*<div class="slide-footer">)'
    slide11_new_body = """
        <div style="display: grid; grid-template-columns: 1.22fr 1fr; gap: 32px; height: 100%;">
          <div class="grid-2" style="gap: 18px;">
            <div class="card accent-olive highlight" style="padding: 22px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-olive">Step 01</span>
                <h4 class="card-title" style="font-size: 20px;">Stabilize Dolibarr CRM</h4>
                <ul class="bullet-list" style="margin-top: 10px; font-size: 14.5px;">
                  <li>Set up automated daily cloud database backups.</li>
                  <li>Clean existing 25 cafe customer records.</li>
                  <li>Ensure order history and invoices are never lost.</li>
                </ul>
              </div>
            </div>
            <div class="card accent-olive" style="padding: 22px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-olive">Step 02</span>
                <h4 class="card-title" style="font-size: 20px;">Standardize €19 Trial Kit</h4>
                <ul class="bullet-list" style="margin-top: 10px; font-size: 14.5px;">
                  <li>Box the borosilicate glass teapot with micro-infuser.</li>
                  <li>Include 4 signature organic tins (Earl Grey, Chai, etc.).</li>
                  <li>Insert 100% wholesale crate credit voucher.</li>
                </ul>
              </div>
            </div>
            <div class="card accent-olive" style="padding: 22px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-olive">Step 03</span>
                <h4 class="card-title" style="font-size: 20px;">Run § 5 TMG Scraper</h4>
                <ul class="bullet-list" style="margin-top: 10px; font-size: 14.5px;">
                  <li>Extract 200 brunch cafes in Berlin &amp; Munich for €0.00.</li>
                  <li>Resolve verified owner names &amp; mobile numbers.</li>
                  <li>Zero wasted ad spend or expensive data broker fees.</li>
                </ul>
              </div>
            </div>
            <div class="card accent-olive" style="padding: 22px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-olive">Step 04</span>
                <h4 class="card-title" style="font-size: 20px;">1-Tap WhatsApp Pilot</h4>
                <ul class="bullet-list" style="margin-top: 10px; font-size: 14.5px;">
                  <li>Generate first 10 personalized trial kit drafts.</li>
                  <li>Send to Sidy's WhatsApp for instant review.</li>
                  <li>Sidy taps Approve with one click to initiate pilot.</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="card" style="padding: 24px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: #FAF8F2;">
            <img src="assets/alandas_trial_teapot_kit.jpg" alt="Alandas Trial Teapot Kit" style="width: 100%; max-height: 440px; object-fit: cover; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.12);">
            <div style="margin-top: 14px;">
              <span class="card-tag tag-ochre" style="font-size: 12px;">SPRINT 1 TANGIBLE DELIVERABLE</span>
              <h4 style="font-family: var(--font-display); font-size: 20px; color: var(--text-main); margin: 4px 0;">€19 Trial Kit Ready to Dispatch</h4>
              <p style="font-size: 14.5px; color: var(--text-muted); line-height: 1.4;">Ready to box and send to the first 10 Berlin cafes this week.</p>
            </div>
          </div>
        </div>
      """
    content = re.sub(slide11_old_regex, r'\1' + slide11_new_body + r'\3', content, flags=re.DOTALL)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("[SUCCESS] HTML presentation successfully polished.")

    # Run the PDF build pipeline
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

    print("Rendering PDF via Chromium...")
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

    print("Injecting PDF Metadata with pypdf...")
    reader = pypdf.PdfReader(pdf_out)
    writer = pypdf.PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    writer.add_metadata({
        "/Title": "Alandas Tea Berlin — Sidy's Revenue Roadmap & Cheat Sheet",
        "/Author": "Cyril Uzochukwu & Sidy Sow",
        "/Subject": "Wholesale Growth Architecture: The Path from 25 to 100 Cafes (€15k–€30k/mo)",
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
    print("[ALL DONE] 11 page proofs rendered successfully.")

if __name__ == "__main__":
    polish_deck()
