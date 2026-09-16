"""
export_standalone_diagrams.py
Exports standalone, high-definition (2x retina) PNGs of all Alandas system architecture diagrams
and UI mockups into a dedicated folder `standalone_system_diagrams/` ready to send Sidy on WhatsApp.
"""

import os
import shutil
import subprocess

def export_all():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "standalone_system_diagrams")
    os.makedirs(output_dir, exist_ok=True)
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    print(f"Target Output Directory: {output_dir}\n")

    # 1. SVGs to render at 2x Retina Quality
    svg_diagrams = [
        {
            "src": "tier1_essential_automation_flowchart.svg",
            "out": "01_Tier_1_Essential_Revenue_Automation_Flowchart.png",
            "w": 1200,
            "h": 2600,
            "desc": "Tier 1: Essential Revenue Automation State Machine (Full Waterfall Scraper ➔ Sidy WhatsApp ➔ Dolibarr CRM)"
        },
        {
            "src": "tier2_governed_intelligence_flowchart.svg",
            "out": "02_Tier_2_Governed_Decision_Architecture_Flowchart.png",
            "w": 1200,
            "h": 1800,
            "desc": "Tier 2: Governed Decision Flowchart (Policy Engines & Decision Contracts for +30% Ad Budget)"
        },
        {
            "src": "tier3_autonomous_platform_flowchart.svg",
            "out": "03_Tier_3_Autonomous_Platform_Flywheel_Flowchart.png",
            "w": 1200,
            "h": 1500,
            "desc": "Tier 3: Autonomous Revenue Platform Flowchart (Closed-Loop Commercial Flywheel)"
        },
        {
            "src": "waterfall_enrichment.svg",
            "out": "04_Waterfall_Lead_Enrichment_Engine_Flowchart.png",
            "w": 1600,
            "h": 900,
            "desc": "German Impressum § 5 TMG Waterfall Enrichment Engine (87% Data Savings)"
        },
        {
            "src": "tiered_revenue_architecture.svg",
            "out": "05_Three_Tier_Architecture_Overview.png",
            "w": 1600,
            "h": 1000,
            "desc": "Three-Tier Architecture Overview (Essential ➔ Governed ➔ Autonomous Progression)"
        }
    ]

    for item in svg_diagrams:
        src_path = os.path.join(base_dir, item["src"])
        out_path = os.path.join(output_dir, item["out"])
        
        # HTML wrapper to ensure perfect clean background and responsive SVG scaling
        with open(src_path, "r", encoding="utf-8") as sf:
            svg_content = sf.read()

        temp_html = os.path.join(output_dir, f"temp_{item['src']}.html")
        html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #FFFFFF;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 24px;
    width: 100%;
    height: 100%;
  }}
  svg {{
    max-width: 100%;
    height: auto;
    display: block;
    filter: drop-shadow(0 4px 16px rgba(0,0,0,0.06));
  }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
        with open(temp_html, "w", encoding="utf-8") as wf:
            wf.write(html_wrapper)

        url = "file:///" + temp_html.replace(os.sep, "/")
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--device-scale-factor=2",
            f"--window-size={item['w']},{item['h']}",
            f"--screenshot={out_path}",
            url
        ]
        print(f"Rendering [2x Retina] {item['out']}...")
        subprocess.run(cmd, check=True)
        print(f"  --> Created: {out_path} ({os.path.getsize(out_path)} bytes)")
        
        if os.path.exists(temp_html):
            os.remove(temp_html)

    # 2. Standalone UI Mockups & Commercial Product Photo
    ui_assets = [
        {
            "src": os.path.join(base_dir, "assets", "mockup_whatsapp_tier1.png"),
            "out": "06_WhatsApp_Mobile_One_Tap_Approval_Mockup.png",
            "desc": "iPhone Screen: Sidy's 1-Tap Lead Approval & Outbound WhatsApp Dispatch"
        },
        {
            "src": os.path.join(base_dir, "assets", "mockup_dolibarr_crm.png"),
            "out": "07_Dolibarr_CRM_Automated_Invoice_Mockup.png",
            "desc": "Desktop Screen: Dolibarr CRM Handwritten Note OCR & German Tax Invoice Sync"
        },
        {
            "src": os.path.join(base_dir, "assets", "alandas_trial_teapot_kit.jpg"),
            "out": "08_Alandas_19_Euro_Trial_Teapot_Starter_Kit.jpg",
            "desc": "Physical Product: Alandas €19 Borosilicate Teapot & 4 Tea Tins Trial Box"
        }
    ]

    for item in ui_assets:
        out_path = os.path.join(output_dir, item["out"])
        shutil.copy2(item["src"], out_path)
        print(f"Copied {item['out']} ({os.path.getsize(out_path)} bytes)")

    print("\n[SUCCESS] All 8 standalone system diagrams and mockups exported cleanly!")

if __name__ == "__main__":
    export_all()
