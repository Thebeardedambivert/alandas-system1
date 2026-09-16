"""
build_visual_mockups.py
Generates razor-sharp UI and workflow mockup images for Alandas Cheat Sheet:
1. WhatsApp 1-Tap Approval Screen (iPhone Mockup)
2. WhatsApp Day-25 Predictive Refill Screen
3. Dolibarr CRM Automated Invoice & Lead Card Screen
"""

import os
import subprocess

def create_html_mockups():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # 1. WhatsApp 1-Tap Mobile UI Mockup
    whatsapp_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
  body { background: transparent; display: flex; align-items: center; justify-content: center; width: 620px; height: 920px; }
  .phone {
    width: 540px;
    height: 860px;
    background: #0B141A;
    border-radius: 44px;
    border: 8px solid #2A2F32;
    box-shadow: 0 25px 60px rgba(0,0,0,0.35);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }
  .notch {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 180px;
    height: 24px;
    background: #2A2F32;
    border-bottom-left-radius: 16px;
    border-bottom-right-radius: 16px;
    z-index: 10;
  }
  .status-bar {
    height: 36px;
    background: #202C33;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 24px 0 24px;
    color: #AEBAC1;
    font-size: 13px;
    font-weight: 600;
  }
  .header {
    background: #202C33;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    border-bottom: 1px solid #111B21;
  }
  .avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: #444C32;
    color: #FFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 18px;
    border: 2px solid #C48737;
  }
  .header-info h4 { color: #E9EDEF; font-size: 16px; font-weight: 600; display: flex; align-items: center; gap: 6px; }
  .badge-check { background: #00A884; color: #FFF; font-size: 10px; padding: 2px 6px; border-radius: 10px; }
  .header-info p { color: #8696A0; font-size: 12px; margin-top: 2px; }

  .chat-body {
    flex: 1;
    background: #0B141A;
    background-image: radial-gradient(#1B262C 1.5px, transparent 1.5px);
    background-size: 20px 20px;
    padding: 20px 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    overflow: hidden;
  }
  .bubble {
    background: #202C33;
    border-radius: 12px;
    border-top-left-radius: 2px;
    padding: 14px 16px;
    color: #E9EDEF;
    font-size: 14px;
    line-height: 1.45;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    border: 1px solid #2A3942;
  }
  .lead-badge {
    display: inline-block;
    background: rgba(196, 135, 55, 0.2);
    color: #C48737;
    font-size: 11.5px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    margin-bottom: 8px;
    border: 1px solid rgba(196, 135, 55, 0.4);
    letter-spacing: 0.05em;
  }
  .lead-title {
    font-size: 16px;
    font-weight: 700;
    color: #FFF;
    margin-bottom: 6px;
  }
  .lead-meta {
    font-size: 13px;
    color: #8696A0;
    margin-bottom: 12px;
    line-height: 1.4;
  }
  .quote-box {
    background: #111B21;
    border-left: 4px solid #00A884;
    padding: 10px 12px;
    border-radius: 6px;
    font-size: 13.5px;
    color: #D1D7DB;
    margin-bottom: 14px;
    line-height: 1.4;
  }
  .action-buttons {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .btn-approve {
    background: #00A884;
    color: #FFF;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-size: 14.5px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(0, 168, 132, 0.3);
  }
  .btn-secondary-row {
    display: flex;
    gap: 8px;
  }
  .btn-sec {
    flex: 1;
    background: #2A3942;
    color: #AEBAC1;
    border: none;
    border-radius: 6px;
    padding: 8px;
    font-size: 12.5px;
    font-weight: 600;
    text-align: center;
  }

  .status-confirmed {
    background: rgba(0, 168, 132, 0.15);
    border: 1px dashed #00A884;
    border-radius: 8px;
    padding: 10px 12px;
    color: #25D366;
    font-size: 12px;
    font-weight: 600;
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
</style>
</head>
<body>

<div class="phone">
  <div class="notch"></div>
  <div class="status-bar">
    <span>09:41</span>
    <span>📶 5G • 98%</span>
  </div>
  <div class="header">
    <div class="avatar">A</div>
    <div class="header-info">
      <h4>Alandas Revenue Copilot <span class="badge-check">SYSTEM</span></h4>
      <p>Automated B2B Outbound • Dolibarr Synced</p>
    </div>
  </div>
  <div class="chat-body">
    <div class="bubble">
      <span class="lead-badge">QUALIFIED CAFE LEAD • ICP 94/100</span>
      <div class="lead-title">Cafe Einstein Stammhaus</div>
      <div class="lead-meta">
        📍 Kurfürstenstraße 58, Berlin-Schöneberg<br>
        ☕ Specialty Brunch • 65 Terrace Seats • Coffee €4.20<br>
        👤 Owner: Herr Christian Schmidt (Verified via § 5 TMG)
      </div>

      <div style="font-size:12px; color:#8696A0; margin-bottom:4px; font-weight:600;">PROPOSED OUTREACH (DRAFT):</div>
      <div class="quote-box">
        "Hallo Christian, euer Terrassen-Brunch sieht fantastisch aus! 🌿 Viele Berliner Cafés wechseln gerade auf unseren 96% Marge Bio-Tee.<br><br>
        Ich würde dir gerne unser €19 Barista-Teekannen-Set (inkl. bruchsicherer Teekanne &amp; 4 Proben) vorbeibringen – die €19 schreiben wir deiner ersten Großpackung zu 100% gut. Passt dir Dienstag?"
      </div>

      <div class="action-buttons">
        <button class="btn-approve">✅ TAP TO APPROVE &amp; DISPATCH</button>
        <div class="btn-secondary-row">
          <div class="btn-sec">✏️ Edit Pitch</div>
          <div class="btn-sec">❌ Discard Lead</div>
        </div>
      </div>

      <div class="status-confirmed">
        ✓ 1-Tap sends via WhatsApp API • Syncs to Dolibarr CRM • Schedules Day-4 tasting call
      </div>
    </div>
  </div>
</div>

</body>
</html>"""
    
    with open(os.path.join(assets_dir, "mockup_whatsapp_tier1.html"), "w", encoding="utf-8") as f:
        f.write(whatsapp_html)

    # 2. Dolibarr CRM & Invoice Mockup
    dolibarr_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
  body { background: transparent; display: flex; align-items: center; justify-content: center; width: 840px; height: 640px; }
  .window {
    width: 800px;
    height: 600px;
    background: #FFFFFF;
    border-radius: 16px;
    border: 1.5px solid #D1D9C5;
    box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .win-header {
    background: #444C32;
    padding: 10px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #FFF;
  }
  .win-brand { font-size: 14px; font-weight: 700; letter-spacing: 0.06em; display: flex; align-items: center; gap: 8px; }
  .win-pills { display: flex; gap: 6px; }
  .pill { width: 10px; height: 10px; border-radius: 50%; background: rgba(255,255,255,0.3); }

  .crm-content {
    flex: 1;
    display: flex;
    background: #F9F7F2;
  }
  .sidebar {
    width: 220px;
    background: #F2EEE4;
    border-right: 1px solid #E2DDD0;
    padding: 16px 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 13px;
  }
  .nav-item {
    padding: 8px 12px;
    border-radius: 8px;
    color: #545148;
    font-weight: 600;
  }
  .nav-item.active { background: #444C32; color: #FFF; }

  .main-panel {
    flex: 1;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    overflow: hidden;
  }
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid #E2DDD0;
    padding-bottom: 12px;
  }
  .doc-title { font-size: 18px; font-weight: 700; color: #181916; }
  .badge-status { background: #EEF2E8; color: #444C32; border: 1px solid #D1D9C5; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 20px; }

  .order-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }
  .card-ocr {
    background: #FFF;
    border: 1px solid #E2DDD0;
    border-radius: 10px;
    padding: 14px;
    font-size: 12.5px;
  }
  .card-ocr-title { font-size: 11.5px; font-weight: 700; color: #C48737; text-transform: uppercase; margin-bottom: 6px; }
  .ocr-preview { background: #FAF8F2; border: 1px dashed #D1D9C5; border-radius: 6px; padding: 8px; font-style: italic; color: #545148; line-height: 1.4; }

  .line-items-table {
    width: 100%;
    border-collapse: collapse;
    background: #FFF;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #E2DDD0;
    font-size: 12px;
  }
  .line-items-table th { background: #F2EEE4; padding: 8px 10px; text-align: left; color: #444C32; font-weight: 700; }
  .line-items-table td { padding: 8px 10px; border-top: 1px solid #F0EBE0; color: #181916; }
  .total-row td { font-weight: 700; background: #EEF2E8; color: #444C32; }

  .footer-action {
    margin-top: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFF;
    padding: 10px 14px;
    border-radius: 8px;
    border: 1px solid #E2DDD0;
    font-size: 12.5px;
  }
  .btn-pdf { background: #C48737; color: #FFF; font-weight: 700; border: none; padding: 6px 14px; border-radius: 6px; }
</style>
</head>
<body>

<div class="window">
  <div class="win-header">
    <div class="win-brand">DOLIBARR CRM &amp; INVOICE GENERATOR // ALANDAS TEA BERLIN</div>
    <div class="win-pills"><div class="pill"></div><div class="pill"></div><div class="pill"></div></div>
  </div>
  <div class="crm-content">
    <div class="sidebar">
      <div class="nav-item">🏢 Third Parties (Cafes)</div>
      <div class="nav-item active">📄 Invoices &amp; Orders</div>
      <div class="nav-item">📦 Inventory &amp; Stock</div>
      <div class="nav-item">🤖 Hermes / Temporal Log</div>
    </div>
    <div class="main-panel">
      <div class="panel-header">
        <div>
          <div class="doc-title">Invoice #INV-2026-0842 (Draft Auto-Created)</div>
          <div style="font-size:12px; color:#848074;">Customer: Café am Neuen See • Source: WhatsApp Photo OCR</div>
        </div>
        <span class="badge-status">VALIDATED BY SIDY</span>
      </div>

      <div class="order-grid">
        <div class="card-ocr">
          <div class="card-ocr-title">Inbound WhatsApp Note (Parsed)</div>
          <div class="ocr-preview">
            "Hi Sidy! We need refills for the weekend:<br>
            • 2x 1kg Earl Grey Classic<br>
            • 1x 1kg Bio Chai Spiced<br>
            • 2x Teapot Sets with Infuser"
          </div>
        </div>
        <div class="card-ocr">
          <div class="card-ocr-title">Automated Dolibarr Extraction</div>
          <div style="line-height:1.45; color:#181916;">
            ✓ Account: Café am Neuen See (#CUST-042)<br>
            ✓ Wholesale Discount: Level 2 Tier Applied (15%)<br>
            ✓ Tax: 7% Food &amp; Beverage / 19% Hardware<br>
            ✓ Due Date: 14 Days Net (SEPA Direct)
          </div>
        </div>
      </div>

      <table class="line-items-table">
        <tr>
          <th>Product / Description</th>
          <th>Qty</th>
          <th>Unit Price</th>
          <th>VAT</th>
          <th>Total</th>
        </tr>
        <tr>
          <td>Alandas Earl Grey Artisan Loose Leaf (1kg Bag)</td>
          <td>2</td>
          <td>€34.00</td>
          <td>7%</td>
          <td>€68.00</td>
        </tr>
        <tr>
          <td>Alandas Bio Chai Spiced Blend (1kg Bag)</td>
          <td>1</td>
          <td>€38.00</td>
          <td>7%</td>
          <td>€38.00</td>
        </tr>
        <tr>
          <td>Heavy Borosilicate Cafe Teapot (500ml)</td>
          <td>2</td>
          <td>€14.00</td>
          <td>19%</td>
          <td>€28.00</td>
        </tr>
        <tr class="total-row">
          <td colspan="4" style="text-align:right;">TOTAL INVOICE (INCL. TAX):</td>
          <td>€140.24</td>
        </tr>
      </table>

      <div class="footer-action">
        <span>Automatic Sync: PDF invoice queued for email &amp; WhatsApp dispatch</span>
        <button class="btn-pdf">Download PDF Invoice</button>
      </div>
    </div>
  </div>
</div>

</body>
</html>"""

    with open(os.path.join(assets_dir, "mockup_dolibarr_crm.html"), "w", encoding="utf-8") as f:
        f.write(dolibarr_html)

    print("[SUCCESS] HTML mockup templates created.")

if __name__ == "__main__":
    create_html_mockups()
