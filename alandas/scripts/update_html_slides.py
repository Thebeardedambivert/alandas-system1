import os
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html_path = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck.html")

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Slide 1
slide1_old_regex = r'(<div class="slide active" data-slide="1">.*?<div class="slide-body">)(.*?)(</div>\s*<div class="slide-footer">)'
slide1_new_body = """
        <div style="display: grid; grid-template-columns: 1.25fr 1fr; gap: 32px; height: 100%;">
          <div style="display: flex; flex-direction: column; gap: 16px;">
            <div class="card accent-olive" style="padding: 20px 24px;">
              <span class="card-tag tag-olive">1. The Target</span>
              <h3 class="card-title" style="font-size: 22px;">100 Partner Cafes</h3>
              <p class="card-desc" style="font-size: 16px;">€15,000–€30,000/month recurring income so Sidy quits his Swiss job permanently.</p>
            </div>
            <div class="card accent-ochre highlight" style="padding: 20px 24px;">
              <span class="card-tag tag-ochre">2. The Engine</span>
              <h3 class="card-title" style="font-size: 22px;">24/7 Digital Copilot</h3>
              <p class="card-desc" style="font-size: 16px;">Scrapes cafe leads, drafts WhatsApp pitches, and parses crumpled order notes automatically.</p>
            </div>
            <div class="card accent-forest" style="padding: 20px 24px;">
              <span class="card-tag tag-forest">3. The Control</span>
              <h3 class="card-title" style="font-size: 22px;">3 Governed Tiers</h3>
              <p class="card-desc" style="font-size: 16px;">Sidy retains 100% authority via WhatsApp 1-tap approval. Zero brand risk.</p>
            </div>
          </div>
          <div class="card" style="padding: 24px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: #FAF8F2;">
            <img src="assets/alandas_trial_teapot_kit.jpg" alt="Alandas Trial Teapot Kit" style="width: 100%; max-height: 440px; object-fit: cover; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.12);">
            <div style="margin-top: 18px;">
              <span class="card-tag tag-ochre" style="font-size: 13px;">THE B2B CONVERSION WEAPON</span>
              <h4 style="font-family: var(--font-display); font-size: 22px; color: var(--text-main); margin: 6px 0;">€19 Borosilicate Teapot Starter Kit</h4>
              <p style="font-size: 15px; color: var(--text-muted); line-height: 1.4;">The physical Trojan Horse that turns cold Berlin cafes into lifelong wholesale accounts (100% credited on first crate).</p>
            </div>
          </div>
        </div>
      """

content = re.sub(slide1_old_regex, r'\1' + slide1_new_body + r'\3', content, flags=re.DOTALL)

# 2. Update Slide 4
slide4_old_regex = r'(<div class="slide" data-slide="4">.*?<div class="slide-body">)(.*?)(</div>\s*<div class="slide-footer">)'
slide4_new_body = """
        <div style="display: grid; grid-template-columns: 1.25fr 1fr; gap: 32px; height: 100%;">
          <div class="card" style="padding: 28px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 800; color: var(--olive); letter-spacing: 0.05em; margin-bottom: 12px;">THE 6-STAGE REVENUE PIPELINE</div>
            <div style="display: flex; flex-direction: column; gap: 14px;">
              <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--olive);">
                <strong style="color: var(--olive);">01 // DISCOVER:</strong> Scans Google Maps &amp; Instagram for &gt;30-seat brunch cafes in Berlin &amp; Munich.
              </div>
              <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--olive);">
                <strong style="color: var(--olive);">02 // ENRICH:</strong> Extracts verified owner WhatsApp numbers via German § 5 TMG Impressum for €0.00.
              </div>
              <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--ochre);">
                <strong style="color: var(--ochre-dark);">03 // OFFER:</strong> Pitches the €19 Teapot Starter Kit (100% credited back on wholesale crate).
              </div>
              <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--ochre);">
                <strong style="color: var(--ochre-dark);">04 // 1-TAP APPROVAL:</strong> AI drafts warm message; Sidy reviews on his phone &amp; taps 'Approve'.
              </div>
              <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--forest);">
                <strong style="color: var(--forest);">05 // INVOICE OCR:</strong> AI deciphers handwritten barista notes into draft Dolibarr CRM invoices.
              </div>
              <div style="background: var(--card-alt); padding: 14px 18px; border-radius: 10px; border-left: 5px solid var(--forest);">
                <strong style="color: var(--forest);">06 // DAY-25 REFILL:</strong> Automated WhatsApp refill alert before cafes run dry, ending silent churn.
              </div>
            </div>
          </div>
          <div class="card" style="padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #FAF8F2;">
            <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 800; color: var(--ochre-dark); letter-spacing: 0.05em; margin-bottom: 12px;">WHAT SIDY SEES ON HIS IPHONE // 1-TAP APPROVAL</div>
            <img src="assets/mockup_whatsapp_tier1.png" alt="WhatsApp 1-Tap Approval Mockup" style="max-height: 600px; width: auto; filter: drop-shadow(0 15px 35px rgba(0,0,0,0.2)); border-radius: 36px;">
          </div>
        </div>
      """

content = re.sub(slide4_old_regex, r'\1' + slide4_new_body + r'\3', content, flags=re.DOTALL)

# 3. Update Slide 6 Executive Cards view
slide6_cards_old_regex = r'(<div id="slide-6-cards" class="view-panel active">)(.*?)(</div>\s*<!-- View 2: Flowchart Preview -->)'
slide6_cards_new = """
          <div class="grid-2">
            <div class="card accent-olive" style="padding: 30px; display: flex; flex-direction: column; justify-content: space-between;">
              <div>
                <span class="card-tag tag-olive">How the 5 Steps Work</span>
                <h3 class="card-title">Read ➔ Analyze ➔ Propose ➔ Approve ➔ Execute</h3>
                <ol style="display: flex; flex-direction: column; gap: 12px; padding-left: 20px; font-size: 16.5px; line-height: 1.45; color: var(--text-main); margin-top: 14px;">
                  <li><strong>Read:</strong> Scans Google Maps / Instagram for cafes with &gt;30 seats.</li>
                  <li><strong>Analyze:</strong> Scores beverage menu, seating, and specialty coffee focus.</li>
                  <li><strong>Propose:</strong> Drafts personalized WhatsApp message pitching the €19 teapot kit.</li>
                  <li><strong>Human Approves:</strong> Message lands on Sidy's WhatsApp. Sidy taps <strong>Approve</strong>. Zero unreviewed messages.</li>
                  <li><strong>Execute:</strong> Dispatches message, creates Dolibarr card, and sets Day-4 follow-up.</li>
                </ol>
              </div>
              <div class="callout-box" style="margin-top: 16px; font-size: 15px;">
                <strong>Commercial Impact:</strong> Zero brand risk • Saves 15+ hrs/week • Target: 25 ➔ 40 cafes (~€5k/mo).
              </div>
            </div>
            <div class="card" style="padding: 24px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #FAF8F2;">
              <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 800; color: var(--olive); letter-spacing: 0.05em; margin-bottom: 12px;">WHAT DOLIBARR CRM LOOKS LIKE // NOTE ➔ INVOICE</div>
              <img src="assets/mockup_dolibarr_crm.png" alt="Dolibarr CRM Mockup" style="width: 100%; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.12);">
            </div>
          </div>
        """

content = re.sub(slide6_cards_old_regex, r'\1' + slide6_cards_new + r'\3', content, flags=re.DOTALL)

# 4. Update Slide 11
slide11_old_regex = r'(<div class="slide" data-slide="11">.*?<div class="slide-body">)(.*?)(</div>\s*<div class="slide-footer">)'
slide11_new_body = """
        <div style="display: grid; grid-template-columns: 1.25fr 1fr; gap: 32px; height: 100%;">
          <div class="grid-2" style="gap: 18px;">
            <div class="card accent-olive highlight" style="padding: 22px;">
              <span class="card-tag tag-olive">Step 01</span>
              <h4 class="card-title" style="font-size: 20px;">Stabilize Dolibarr CRM</h4>
              <p class="card-desc" style="font-size: 15px;">Set up automated daily cloud database backups and clean existing 25 cafe customer records so data is never lost again.</p>
            </div>
            <div class="card accent-olive" style="padding: 22px;">
              <span class="card-tag tag-olive">Step 02</span>
              <h4 class="card-title" style="font-size: 20px;">Standardize €19 Trial Kit</h4>
              <p class="card-desc" style="font-size: 15px;">Package the shatter-resistant borosilicate glass teapot with 4 signature blends and 100% wholesale credit voucher.</p>
            </div>
            <div class="card accent-olive" style="padding: 22px;">
              <span class="card-tag tag-olive">Step 03</span>
              <h4 class="card-title" style="font-size: 20px;">Run § 5 TMG Scraper</h4>
              <p class="card-desc" style="font-size: 15px;">Extract 200 high-potential brunch cafes in Berlin &amp; Munich for €0.00 using the legal Impressum waterfall scraper.</p>
            </div>
            <div class="card accent-olive" style="padding: 22px;">
              <span class="card-tag tag-olive">Step 04</span>
              <h4 class="card-title" style="font-size: 20px;">1-Tap WhatsApp Pilot</h4>
              <p class="card-desc" style="font-size: 15px;">Send Sidy the first batch of 10 AI-drafted trial kit outreach messages on WhatsApp for 1-tap review and dispatch.</p>
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

print("[SUCCESS] HTML presentation updated with embedded UI mockups and product photo.")
