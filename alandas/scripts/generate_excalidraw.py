"""
Excalidraw Diagram & Canvas Viewer Generator for Alandas Architecture
Includes:
1. alandas_self_healing_revenue_pipeline.excalidraw (Cyril's exact vertical flowchart & decision tree)
2. waterfall_enrichment_engine.excalidraw
3. tiered_revenue_architecture.excalidraw
4. excalidraw_canvas_viewer.html (Interactive 3-tab canvas with SVG rendering of rect, ellipse, diamond, text, arrows)
"""

import json
import random
import os
from generate_waterfall_flowchart_excalidraw import build_flowchart

def new_seed():
    return random.randint(100000, 999999)

def create_rectangle(id_str, x, y, width, height, stroke_color="#181916", bg_color="#ffffff", fill_style="solid", stroke_width=2, roughness=1, roundness_type=3):
    return {
        "id": id_str,
        "type": "rectangle",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": stroke_color,
        "backgroundColor": bg_color,
        "fillStyle": fill_style,
        "strokeWidth": stroke_width,
        "strokeStyle": "solid",
        "roughness": roughness,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": roundness_type} if roundness_type else None,
        "seed": new_seed(),
        "version": 1,
        "versionNonce": new_seed(),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False
    }

def create_text(id_str, x, y, text, font_size=18, font_family=1, color="#181916", text_align="center", vertical_align="middle", width=200, height=30):
    lines = text.split("\n")
    line_count = len(lines)
    approx_height = max(height, int(font_size * 1.3 * line_count))
    return {
        "id": id_str,
        "type": "text",
        "x": x,
        "y": y,
        "width": width,
        "height": approx_height,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": new_seed(),
        "version": 1,
        "versionNonce": new_seed(),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": font_size,
        "fontFamily": font_family,
        "textAlign": text_align,
        "verticalAlign": vertical_align,
        "baseline": int(font_size * 0.8),
        "containerId": None,
        "originalText": text,
        "lineHeight": 1.25
    }

def create_arrow(id_str, start_x, start_y, end_x, end_y, stroke_color="#444C32", stroke_width=2, stroke_style="solid", roughness=1):
    dx = end_x - start_x
    dy = end_y - start_y
    return {
        "id": id_str,
        "type": "arrow",
        "x": start_x,
        "y": start_y,
        "width": abs(dx),
        "height": abs(dy),
        "angle": 0,
        "strokeColor": stroke_color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
        "strokeStyle": stroke_style,
        "roughness": roughness,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": new_seed(),
        "version": 1,
        "versionNonce": new_seed(),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False,
        "points": [[0, 0], [dx, dy]],
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": "arrow"
    }

def build_waterfall_excalidraw():
    elements = []
    # Outer title frame
    elements.append(create_rectangle("hdr_bg", 80, 50, 1140, 110, stroke_color="#444C32", bg_color="#F9F7F2", stroke_width=2.5, roughness=1))
    elements.append(create_text("hdr_title", 100, 68, "WATERFALL ENRICHMENT: CHEAPEST TOOL FIRST", font_size=28, font_family=1, color="#181916", text_align="center", width=1100))
    elements.append(create_text("hdr_sub", 100, 112, "Each tool only gets what the last one missed  •  87% Data Acquisition Cost Reduction", font_size=18, font_family=1, color="#C48737", text_align="center", width=1100))

    box_w = 260
    box_h = 160
    
    # Raw Leads
    elements.append(create_rectangle("box_raw", 80, 200, box_w, box_h, stroke_color="#2E3422", bg_color="#EEF2E8", stroke_width=2, roughness=1))
    elements.append(create_text("txt_raw_step", 95, 215, "STEP 0 // INGESTION", font_size=13, font_family=3, color="#444C32", text_align="left", width=230))
    elements.append(create_text("txt_raw_name", 95, 240, "1,000 Raw Leads", font_size=21, font_family=1, color="#181916", text_align="left", width=230))
    elements.append(create_text("txt_raw_desc", 95, 275, "Google Maps Cafes &\nInstagram Engagers\nAcross Germany", font_size=14, font_family=1, color="#5C5950", text_align="left", width=230))

    elements.append(create_arrow("arr_0", 340, 280, 390, 280, stroke_color="#444C32", stroke_width=2))

    # STAGE 0: § 5 TMG Impressum
    elements.append(create_rectangle("box_stg0", 390, 200, box_w, box_h, stroke_color="#2F5339", bg_color="#EDF5EF", stroke_width=2.5, roughness=1))
    elements.append(create_text("txt_stg0_step", 405, 215, "STAGE 0 // €0.00 (FREE)", font_size=13, font_family=3, color="#2F5339", text_align="left", width=230))
    elements.append(create_text("txt_stg0_name", 405, 240, "§ 5 TMG Impressum", font_size=20, font_family=1, color="#181916", text_align="left", width=230))
    elements.append(create_text("txt_stg0_desc", 405, 272, "Scrapes legal notice.\n480 emails found.\n520 pass down ➔", font_size=14, font_family=1, color="#181916", text_align="left", width=230))

    elements.append(create_arrow("arr_1", 650, 280, 700, 280, stroke_color="#444C32", stroke_width=2))

    # STAGE 1: GitLeads / Apollo
    elements.append(create_rectangle("box_stg1", 700, 200, box_w, box_h, stroke_color="#444C32", bg_color="#FFFFFF", stroke_width=2, roughness=1))
    elements.append(create_text("txt_stg1_step", 715, 215, "STAGE 1 // €0.005 / QUERY", font_size=13, font_family=3, color="#444C32", text_align="left", width=230))
    elements.append(create_text("txt_stg1_name", 715, 240, "GitLeads / Apollo", font_size=20, font_family=1, color="#181916", text_align="left", width=230))
    elements.append(create_text("txt_stg1_desc", 715, 272, "Bulk database check.\n240 more found.\n280 pass down ➔", font_size=14, font_family=1, color="#5C5950", text_align="left", width=230))

    elements.append(create_arrow("arr_2", 960, 280, 1010, 280, stroke_color="#444C32", stroke_width=2))

    # STAGE 2: Origami / Prospeo
    elements.append(create_rectangle("box_stg2", 1010, 200, box_w, box_h, stroke_color="#C48737", bg_color="#FCF4E8", stroke_width=2, roughness=1))
    elements.append(create_text("txt_stg2_step", 1025, 215, "STAGE 2 // €0.02 / QUERY", font_size=13, font_family=3, color="#C48737", text_align="left", width=230))
    elements.append(create_text("txt_stg2_name", 1025, 240, "Origami / Prospeo", font_size=20, font_family=1, color="#181916", text_align="left", width=230))
    elements.append(create_text("txt_stg2_desc", 1025, 272, "Deep social & MX scrape.\n180 more found.\n~90% find rate total!", font_size=14, font_family=1, color="#9A6622", text_align="left", width=230))

    # ROW 2
    y_row2 = 420
    elements.append(create_arrow("arr_down_val", 1140, 360, 1140, y_row2, stroke_color="#2F5339", stroke_width=2.5))

    # Deliverability Gate
    elements.append(create_rectangle("box_val", 1010, y_row2, box_w, box_h, stroke_color="#2F5339", bg_color="#EDF5EF", stroke_width=2.5, roughness=1))
    elements.append(create_text("txt_val_step", 1025, y_row2 + 15, "VALIDATE // €0.002 / CHECK", font_size=13, font_family=3, color="#2F5339", text_align="left", width=230))
    elements.append(create_text("txt_val_name", 1025, y_row2 + 40, "MillionVerifier", font_size=20, font_family=1, color="#181916", text_align="left", width=230))
    elements.append(create_text("txt_val_desc", 1025, y_row2 + 72, "Valid, risky, catch-all.\nDiscard bad records.\n<1.5% bounce rate guaranteed!", font_size=14, font_family=1, color="#2F5339", text_align="left", width=230))

    elements.append(create_arrow("arr_val_to_mob", 1010, y_row2 + 80, 960, y_row2 + 80, stroke_color="#C48737", stroke_width=2))

    # STAGE 3: LeadMagic Mobile
    elements.append(create_rectangle("box_mob", 700, y_row2, box_w, box_h, stroke_color="#C48737", bg_color="#FCF4E8", stroke_width=2, roughness=1))
    elements.append(create_text("txt_mob_step", 715, y_row2 + 15, "STAGE 3 // BONUS MOBILE", font_size=13, font_family=3, color="#C48737", text_align="left", width=230))
    elements.append(create_text("txt_mob_name", 715, y_row2 + 40, "LeadMagic Mobile", font_size=20, font_family=1, color="#181916", text_align="left", width=230))
    elements.append(create_text("txt_mob_desc", 715, y_row2 + 72, "Mobile lookup on top.\n650 WhatsApp numbers.\nEnables direct B2B chats!", font_size=14, font_family=1, color="#9A6622", text_align="left", width=230))

    elements.append(create_arrow("arr_mob_to_crm", 700, y_row2 + 80, 650, y_row2 + 80, stroke_color="#444C32", stroke_width=2.5))

    # Dolibarr CRM
    elements.append(create_rectangle("box_crm", 390, y_row2, box_w, box_h, stroke_color="#444C32", bg_color="#EEF2E8", stroke_width=2.5, roughness=1))
    elements.append(create_text("txt_crm_step", 405, y_row2 + 15, "DESTINATION // DOLIBARR", font_size=13, font_family=3, color="#444C32", text_align="left", width=230))
    elements.append(create_text("txt_crm_name", 405, y_row2 + 40, "Dolibarr CRM Lead", font_size=20, font_family=1, color="#181916", text_align="left", width=230))
    elements.append(create_text("txt_crm_desc", 405, y_row2 + 72, "Clean, verified entity.\nWhatsApp draft queued.\nSidy approves with 1 tap.", font_size=14, font_family=1, color="#444C32", text_align="left", width=230))

    # Economics Box
    elements.append(create_rectangle("box_eco", 80, y_row2, box_w, box_h, stroke_color="#181916", bg_color="#FFFFFF", stroke_width=1.5, roughness=1))
    elements.append(create_text("txt_eco_title", 95, y_row2 + 15, "UNIT ECONOMICS", font_size=14, font_family=3, color="#181916", text_align="left", width=230))
    elements.append(create_text("txt_eco_stat", 95, y_row2 + 40, "87% Savings", font_size=22, font_family=1, color="#2F5339", text_align="left", width=230))
    elements.append(create_text("txt_eco_desc", 95, y_row2 + 75, "Flat Scrape: €80 / 1k\nWaterfall: €10 / 1k\nNet Save: €70 per 1k leads!", font_size=14, font_family=1, color="#5C5950", text_align="left", width=230))

    # Bottom Banner
    elements.append(create_rectangle("box_btm", 80, 620, 1190, 85, stroke_color="#444C32", bg_color="#F9F7F2", stroke_width=1.5, roughness=1))
    elements.append(create_text("txt_btm_title", 100, 632, "TEMPORAL DURABILITY GUARANTEE", font_size=13, font_family=3, color="#444C32", text_align="left", width=1150))
    elements.append(create_text("txt_btm_body", 100, 655, "Each waterfall stage is an isolated Temporal Activity with automatic exponential backoff. If Apollo or Prospeo times out,\nthe workflow catches the exception and falls back to the next provider gracefully — zero dropped leads or corrupted records.", font_size=14, font_family=1, color="#181916", text_align="left", width=1150))

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#FBF9F5"},
        "files": {}
    }

def build_tiered_architecture_excalidraw():
    elements = []
    elements.append(create_rectangle("t_hdr_bg", 80, 50, 1140, 110, stroke_color="#444C32", bg_color="#F9F7F2", stroke_width=2.5, roughness=1))
    elements.append(create_text("t_hdr_title", 100, 68, "TIERED REVENUE ARCHITECTURE (ALANDAS CASE STUDY)", font_size=28, font_family=1, color="#181916", text_align="center", width=1100))
    elements.append(create_text("t_hdr_sub", 100, 112, "Complexity must be purchased by a requirement  •  Tiering by operational maturity, not tech count", font_size=18, font_family=1, color="#444C32", text_align="center", width=1100))

    col_w = 360
    col_h = 480
    y_cols = 190
    
    # Tier 1
    elements.append(create_rectangle("t1_bg", 80, y_cols, col_w, col_h, stroke_color="#444C32", bg_color="#EEF2E8", stroke_width=2.5, roughness=1))
    elements.append(create_text("t1_tag", 100, y_cols + 20, "TIER 1 // ESSENTIAL", font_size=13, font_family=3, color="#444C32", text_align="left", width=320))
    elements.append(create_text("t1_title", 100, y_cols + 45, "Durable Automation", font_size=24, font_family=1, color="#181916", text_align="left", width=320))
    elements.append(create_text("t1_sub", 100, y_cols + 80, "Human-Directed Execution (Blast Radius: Zero)", font_size=14, font_family=1, color="#5C5950", text_align="left", width=320))
    t1_body = (
        "• Runtime: Temporal Engine + Python/TS\n"
        "• Storage: Single PostgreSQL Database\n"
        "• Intake: Waterfall Scraper & OpenReply\n"
        "• WhatsApp: Multimodal OCR Order Parser\n"
        "• CRM: Dolibarr Leads & PDF Invoices\n"
        "• Autonomy: Read ➔ Analyze ➔ Propose\n"
        "  ➔ Human Approves in 1 Tap ➔ Execute\n"
        "• Target: 25 to 40 Accounts (€5,000/mo)\n"
        "• Value: Saves Sidy 15+ hours/week"
    )
    elements.append(create_text("t1_bullets", 100, y_cols + 120, t1_body, font_size=15, font_family=1, color="#181916", text_align="left", width=320))
    elements.append(create_arrow("arr_t1_t2", 440, y_cols + 240, 470, y_cols + 240, stroke_color="#C48737", stroke_width=3))

    # Tier 2
    elements.append(create_rectangle("t2_bg", 470, y_cols, col_w, col_h, stroke_color="#C48737", bg_color="#FCF4E8", stroke_width=2.5, roughness=1))
    elements.append(create_text("t2_tag", 490, y_cols + 20, "TIER 2 // PROFESSIONAL", font_size=13, font_family=3, color="#C48737", text_align="left", width=320))
    elements.append(create_text("t2_title", 490, y_cols + 45, "Governed Intelligence", font_size=24, font_family=1, color="#181916", text_align="left", width=320))
    elements.append(create_text("t2_sub", 490, y_cols + 80, "Human-Governed Decisions (Bounded Radius)", font_size=14, font_family=1, color="#9A6622", text_align="left", width=320))
    t2_body = (
        "• All of Tier 1 Foundation Intact\n"
        "• Policy Engine: Strict Ad & Pricing Bounds\n"
        "• Decision Contracts: Typed JSON Schemas\n"
        "• Verification: Post-Action State Query\n"
        "• Churn Defense: Day-25 WhatsApp Refills\n"
        "• Graphs: Bounded LangGraph Creative Eval\n"
        "• Tracing: OpenTelemetry Immutable Audit\n"
        "• Target: 40 to 70 Accounts (€12,000/mo)\n"
        "• Value: Prevents Churn & Zero Bad Ad Spend"
    )
    elements.append(create_text("t2_bullets", 490, y_cols + 120, t2_body, font_size=15, font_family=1, color="#181916", text_align="left", width=320))
    elements.append(create_arrow("arr_t2_t3", 830, y_cols + 240, 860, y_cols + 240, stroke_color="#2F5339", stroke_width=3))

    # Tier 3
    elements.append(create_rectangle("t3_bg", 860, y_cols, col_w, col_h, stroke_color="#2F5339", bg_color="#EDF5EF", stroke_width=2.5, roughness=1))
    elements.append(create_text("t3_tag", 880, y_cols + 20, "TIER 3 // AUTONOMOUS", font_size=13, font_family=3, color="#2F5339", text_align="left", width=320))
    elements.append(create_text("t3_title", 880, y_cols + 45, "Autonomous Platform", font_size=24, font_family=1, color="#181916", text_align="left", width=320))
    elements.append(create_text("t3_sub", 880, y_cols + 80, "Policy-Governed Autonomy (Circuit Breakers)", font_size=14, font_family=1, color="#1E3725", text_align="left", width=320))
    t3_body = (
        "• Multi-Agent Coordination via Temporal\n"
        "• Domain Specialists: Acq, Creative, RevOps\n"
        "• MCP Layer: Standard Tool Interface Protocol\n"
        "• Closed-Loop Flywheel: LTV Reorders Feed Ads\n"
        "• Multi-City Scale: Berlin, Munich, Vienna, Zurich\n"
        "• Circuit Breakers: Automatic Outlier Halt\n"
        "• Executive Role: Sidy as Supervisor\n"
        "• Target: 100+ Accounts (€20k–€30k/mo)\n"
        "• Value: Sidy Quits Swiss Job to be 100% Boss"
    )
    elements.append(create_text("t3_bullets", 880, y_cols + 120, t3_body, font_size=15, font_family=1, color="#181916", text_align="left", width=320))

    elements.append(create_rectangle("t_btm_bg", 80, 690, 1140, 80, stroke_color="#444C32", bg_color="#F9F7F2", stroke_width=1.5, roughness=1))
    elements.append(create_text("t_btm_title", 100, 702, "NON-DESTRUCTIVE EVOLUTION LAW", font_size=13, font_family=3, color="#444C32", text_align="left", width=1100))
    elements.append(create_text("t_btm_desc", 100, 725, "Higher tiers wrap around lower tiers rather than replacing them. Tier 1 code is never discarded; Tier 2 adds Policy Gates,\nand Tier 3 adds Autonomous Loops. Complexity is earned only when concrete business scale demands it.", font_size=14, font_family=1, color="#181916", text_align="left", width=1100))

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#FBF9F5"},
        "files": {}
    }

def build_interactive_viewer(flowchart_data, waterfall_data, tiered_data, output_html_path):
    flowchart_json = json.dumps(flowchart_data)
    waterfall_json = json.dumps(waterfall_data)
    tiered_json = json.dumps(tiered_data)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alandas Architecture Canvas — Excalidraw Flowchart</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=JetBrains+Mono:wght@500;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --bg: #141613;
      --card-bg: #FFFFFF;
      --border: #3A3E35;
      --olive: #444C32;
      --ochre: #C48737;
      --forest: #2F5339;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
      color: #E8E6DF;
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }}
    header {{
      background: #1C1F1A;
      border-bottom: 1px solid var(--border);
      padding: 12px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      z-index: 10;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .logo-badge {{
      background: var(--olive);
      color: #FFF;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
    }}
    .title {{
      font-size: 17px;
      font-weight: 700;
      color: #FFF;
    }}
    .nav-tabs {{
      display: flex;
      gap: 6px;
      background: #121411;
      padding: 4px;
      border-radius: 30px;
      border: 1px solid var(--border);
    }}
    .tab-btn {{
      background: transparent;
      border: none;
      color: #9C9A8E;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-weight: 600;
      font-size: 13.5px;
      padding: 7px 16px;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .tab-btn.active {{
      background: var(--olive);
      color: #FFF;
    }}
    .actions {{
      display: flex;
      gap: 10px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #282C25;
      color: #E8E6DF;
      border: 1px solid var(--border);
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      padding: 7px 15px;
      border-radius: 8px;
      cursor: pointer;
      text-decoration: none;
      transition: background 0.2s;
    }}
    .btn:hover {{
      background: #343A30;
      color: #FFF;
    }}
    .btn-primary {{
      background: var(--ochre);
      color: #FFF;
      border-color: #9A6622;
    }}
    .btn-primary:hover {{
      background: #A66D25;
    }}

    /* CANVAS VIEWPORT - FULL SCROLLING SUPPORT */
    .viewport {{
      flex: 1;
      overflow: auto;
      display: flex;
      align-items: flex-start;
      justify-content: center;
      padding: 30px;
      background: radial-gradient(circle at 50% 50%, #1F231D 0%, #141613 100%);
    }}
    .canvas-container {{
      background: var(--card-bg);
      box-shadow: 0 25px 60px rgba(0,0,0,0.6);
      border-radius: 16px;
      border: 2px solid #33382D;
      position: relative;
      margin-bottom: 40px;
    }}
    svg.excalidraw-svg {{
      display: block;
    }}

    /* NOTICE FOOTER */
    footer {{
      background: #181B16;
      border-top: 1px solid var(--border);
      padding: 10px 24px;
      font-size: 13px;
      color: #9C9A8E;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }}
  </style>
</head>
<body>

<header>
  <div class="brand">
    <div class="logo-badge">EXCALIDRAW</div>
    <div class="title">Alandas Architecture Canvas</div>
  </div>

  <div class="nav-tabs">
    <button class="tab-btn active" id="tabFlow" onclick="switchTab('flowchart')">Production Revenue Flowchart</button>
    <button class="tab-btn" id="tabWaterfall" onclick="switchTab('waterfall')">Waterfall Enrichment Pipeline</button>
    <button class="tab-btn" id="tabTiered" onclick="switchTab('tiered')">3-Tier Maturity Model</button>
  </div>

  <div class="actions">
    <a class="btn" id="btnDownload" href="#" download="alandas_revenue_flowchart.excalidraw">Download .excalidraw</a>
    <a class="btn btn-primary" href="https://excalidraw.com" target="_blank" title="Open Excalidraw.com in a new tab">Open in Excalidraw.com ↗</a>
  </div>
</header>

<div class="viewport" id="viewportArea">
  <div class="canvas-container" id="canvasBox">
    <svg class="excalidraw-svg" id="svgStage" viewBox="0 0 1000 2340" width="1000" height="2340">
      <!-- SVG elements injected here -->
    </svg>
  </div>
</div>

<footer>
  <div><strong>Full Vision State Machine:</strong> True vertical engineering flowchart with decision diamonds, side-exit failure branches & agent containers.</div>
  <div>Alandas Tea Berlin  •  Architecture by Cyril Uzochukwu</div>
</footer>

<script>
  const flowchartData = {flowchart_json};
  const waterfallData = {waterfall_json};
  const tieredData = {tiered_json};
  let currentTab = 'flowchart';

  function renderExcalidrawToSvg(doc, svgElem) {{
    svgElem.innerHTML = '';
    
    // Hand-drawn filter for authentic roughness jitter
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    defs.innerHTML = `
      <filter id="handDrawn" x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise" />
        <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.2" xChannelSelector="R" yChannelSelector="G" />
      </filter>
    `;
    svgElem.appendChild(defs);

    doc.elements.forEach(el => {{
      if (el.type === 'rectangle') {{
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', el.x);
        rect.setAttribute('y', el.y);
        rect.setAttribute('width', el.width);
        rect.setAttribute('height', el.height);
        rect.setAttribute('rx', el.roundness ? '12' : '0');
        rect.setAttribute('fill', el.backgroundColor);
        rect.setAttribute('stroke', el.strokeColor);
        rect.setAttribute('stroke-width', el.strokeWidth);
        rect.setAttribute('filter', 'url(#handDrawn)');
        svgElem.appendChild(rect);
      }} else if (el.type === 'ellipse') {{
        const ellipse = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
        ellipse.setAttribute('cx', el.x + el.width / 2);
        ellipse.setAttribute('cy', el.y + el.height / 2);
        ellipse.setAttribute('rx', el.width / 2);
        ellipse.setAttribute('ry', el.height / 2);
        ellipse.setAttribute('fill', el.backgroundColor);
        ellipse.setAttribute('stroke', el.strokeColor);
        ellipse.setAttribute('stroke-width', el.strokeWidth);
        ellipse.setAttribute('filter', 'url(#handDrawn)');
        svgElem.appendChild(ellipse);
      }} else if (el.type === 'diamond') {{
        const diamond = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        const midX = el.x + el.width / 2;
        const midY = el.y + el.height / 2;
        const topX = midX, topY = el.y;
        const rightX = el.x + el.width, rightY = midY;
        const btmX = midX, btmY = el.y + el.height;
        const leftX = el.x, leftY = midY;
        diamond.setAttribute('points', `${{topX}},${{topY}} ${{rightX}},${{rightY}} ${{btmX}},${{btmY}} ${{leftX}},${{leftY}}`);
        diamond.setAttribute('fill', el.backgroundColor);
        diamond.setAttribute('stroke', el.strokeColor);
        diamond.setAttribute('stroke-width', el.strokeWidth);
        diamond.setAttribute('filter', 'url(#handDrawn)');
        svgElem.appendChild(diamond);
      }} else if (el.type === 'text') {{
        const textNode = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        textNode.setAttribute('x', el.textAlign === 'center' ? el.x + el.width / 2 : el.x);
        textNode.setAttribute('y', el.y + el.fontSize);
        textNode.setAttribute('fill', el.strokeColor);
        textNode.setAttribute('font-size', el.fontSize);
        textNode.setAttribute('font-family', el.fontFamily === 3 ? 'JetBrains Mono, monospace' : (el.fontFamily === 1 ? 'Caveat, cursive, sans-serif' : 'Plus Jakarta Sans, sans-serif'));
        textNode.setAttribute('font-weight', el.fontSize > 18 ? '700' : '600');
        textNode.setAttribute('text-anchor', el.textAlign === 'center' ? 'middle' : 'start');
        
        const lines = el.text.split('\\n');
        lines.forEach((line, idx) => {{
          const tspan = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
          tspan.textContent = line;
          tspan.setAttribute('x', el.textAlign === 'center' ? el.x + el.width / 2 : el.x);
          tspan.setAttribute('dy', idx === 0 ? 0 : el.fontSize * 1.32);
          textNode.appendChild(tspan);
        }});
        svgElem.appendChild(textNode);
      }} else if (el.type === 'arrow') {{
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        const startX = el.x;
        const startY = el.y;
        const endX = el.x + el.points[1][0];
        const endY = el.y + el.points[1][1];
        
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', startX);
        line.setAttribute('y1', startY);
        line.setAttribute('x2', endX);
        line.setAttribute('y2', endY);
        line.setAttribute('stroke', el.strokeColor);
        line.setAttribute('stroke-width', el.strokeWidth);
        line.setAttribute('filter', 'url(#handDrawn)');
        g.appendChild(line);

        const angle = Math.atan2(endY - startY, endX - startX);
        const headLen = 13;
        const p1x = endX - headLen * Math.cos(angle - Math.PI / 6);
        const p1y = endY - headLen * Math.sin(angle - Math.PI / 6);
        const p2x = endX - headLen * Math.cos(angle + Math.PI / 6);
        const p2y = endY - headLen * Math.sin(angle + Math.PI / 6);

        const head = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        head.setAttribute('points', `${{endX}},${{endY}} ${{p1x}},${{p1y}} ${{p2x}},${{p2y}}`);
        head.setAttribute('fill', el.strokeColor);
        g.appendChild(head);
        svgElem.appendChild(g);
      }}
    }});
  }}

  function switchTab(tab) {{
    currentTab = tab;
    const tabF = document.getElementById('tabFlow');
    const tabW = document.getElementById('tabWaterfall');
    const tabT = document.getElementById('tabTiered');
    const btnDown = document.getElementById('btnDownload');
    const svgStage = document.getElementById('svgStage');
    const viewportArea = document.getElementById('viewportArea');

    tabF.classList.remove('active');
    tabW.classList.remove('active');
    tabT.classList.remove('active');

    // Scroll to top when switching
    viewportArea.scrollTop = 0;

    if (tab === 'flowchart') {{
      tabF.classList.add('active');
      svgStage.setAttribute('viewBox', '0 0 1000 2340');
      svgStage.setAttribute('width', '1000');
      svgStage.setAttribute('height', '2340');
      renderExcalidrawToSvg(flowchartData, svgStage);
      btnDown.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(flowchartData, null, 2));
      btnDown.download = 'alandas_self_healing_revenue_pipeline.excalidraw';
    }} else if (tab === 'waterfall') {{
      tabW.classList.add('active');
      svgStage.setAttribute('viewBox', '0 0 1320 740');
      svgStage.setAttribute('width', '1320');
      svgStage.setAttribute('height', '740');
      renderExcalidrawToSvg(waterfallData, svgStage);
      btnDown.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(waterfallData, null, 2));
      btnDown.download = 'waterfall_enrichment_engine.excalidraw';
    }} else {{
      tabT.classList.add('active');
      svgStage.setAttribute('viewBox', '0 0 1300 800');
      svgStage.setAttribute('width', '1300');
      svgStage.setAttribute('height', '800');
      renderExcalidrawToSvg(tieredData, svgStage);
      btnDown.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(tieredData, null, 2));
      btnDown.download = 'tiered_revenue_architecture.excalidraw';
    }}
  }}

  // Initial load
  switchTab('flowchart');
</script>
</body>
</html>
"""
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[SUCCESS] Interactive Excalidraw Viewer updated at: {output_html_path}")

def main():
    base_dir = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas"
    
    # 1. Build Flowchart Excalidraw (Cyril reference style)
    flowchart_doc, total_h = build_flowchart()
    flowchart_path = os.path.join(base_dir, "alandas_self_healing_revenue_pipeline.excalidraw")
    with open(flowchart_path, "w", encoding="utf-8") as f:
        json.dump(flowchart_doc, f, indent=2)
    print(f"[SUCCESS] Generated: {flowchart_path}")

    # 2. Build Waterfall Excalidraw
    waterfall_doc = build_waterfall_excalidraw()
    waterfall_path = os.path.join(base_dir, "waterfall_enrichment_engine.excalidraw")
    with open(waterfall_path, "w", encoding="utf-8") as f:
        json.dump(waterfall_doc, f, indent=2)
    print(f"[SUCCESS] Generated: {waterfall_path}")

    # 3. Build Tiered Architecture Excalidraw
    tiered_doc = build_tiered_architecture_excalidraw()
    tiered_path = os.path.join(base_dir, "tiered_revenue_architecture.excalidraw")
    with open(tiered_path, "w", encoding="utf-8") as f:
        json.dump(tiered_doc, f, indent=2)
    print(f"[SUCCESS] Generated: {tiered_path}")

    # 4. Build Interactive Excalidraw Canvas Viewer
    viewer_path = os.path.join(base_dir, "excalidraw_canvas_viewer.html")
    build_interactive_viewer(flowchart_doc, waterfall_doc, tiered_doc, viewer_path)

if __name__ == "__main__":
    main()
