"""
Generate Alandas Production Architecture Flowchart in Cyril's exact Excalidraw style:
- True vertical engineering flowchart & state machine
- Start/stop pills (Red/Green)
- Rounded process boxes (Blue/Orange)
- Decision diamonds (Yellow) with branch labels (YES, NO, PASS, FAIL, etc.)
- Side-exit escalation/discard boxes (Red/Orange)
- Agent subgraph containers (Purple, Green, Blue) with nested interconnected activities
- Central trunk line with precise coordinate math and zero overlap
"""

import json
import random
import os

def new_seed():
    return random.randint(100000, 999999)

def make_rect(id_str, x, y, w, h, stroke="#000000", fill="transparent", fill_style="solid", stroke_width=2, roundness=3):
    return {
        "id": id_str,
        "type": "rectangle",
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": fill,
        "fillStyle": fill_style,
        "strokeWidth": stroke_width,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": roundness} if roundness else None,
        "seed": new_seed(),
        "version": 1,
        "versionNonce": new_seed(),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False
    }

def make_ellipse(id_str, x, y, w, h, stroke="#000000", fill="transparent", stroke_width=2):
    return {
        "id": id_str,
        "type": "ellipse",
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": fill,
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
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
        "locked": False
    }

def make_diamond(id_str, x, y, w, h, stroke="#EAB308", fill="#FEF08A", stroke_width=2):
    return {
        "id": id_str,
        "type": "diamond",
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": fill,
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
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
        "locked": False
    }

def make_text(id_str, x, y, text, font_size=16, font_family=1, color="#181916", align="center", w=200):
    lines = text.split("\n")
    h = max(24, int(font_size * 1.3 * len(lines)))
    return {
        "id": id_str,
        "type": "text",
        "x": x,
        "y": y,
        "width": w,
        "height": h,
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
        "textAlign": align,
        "verticalAlign": "middle",
        "baseline": int(font_size * 0.8),
        "containerId": None,
        "originalText": text,
        "lineHeight": 1.25
    }

def make_arrow(id_str, start_x, start_y, end_x, end_y, stroke="#181916", stroke_width=2, stroke_style="solid", label=None, label_color="#181916"):
    dx = end_x - start_x
    dy = end_y - start_y
    arrow_elem = {
        "id": id_str,
        "type": "arrow",
        "x": start_x,
        "y": start_y,
        "width": abs(dx),
        "height": abs(dy),
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
        "strokeStyle": stroke_style,
        "roughness": 1,
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
    elements = [arrow_elem]
    if label:
        # Center label on the arrow
        mid_x = start_x + dx * 0.5
        mid_y = start_y + dy * 0.5
        # If horizontal arrow, place label slightly above
        if abs(dx) > abs(dy):
            lx = mid_x - 35
            ly = mid_y - 18
        else:
            lx = mid_x + 8
            ly = mid_y - 10
        elements.append(make_text(f"{id_str}_lbl", lx, ly, label, font_size=12, font_family=1, color=label_color, align="center", w=70))
    return elements

def build_flowchart():
    elements = []
    
    # Canvas Center X
    cx = 480
    
    # -------------------------------------------------------------
    # 0. HEADER
    # -------------------------------------------------------------
    elements.append(make_text("h_title", cx - 450, 30, "Alandas Revenue & Waterfall System — Production Architecture", font_size=24, font_family=1, color="#181916", align="center", w=900))
    elements.append(make_text("h_sub", cx - 400, 65, "Cyril Uzochukwu | AI Automation Engineer | Alandas Tea Berlin", font_size=14, font_family=1, color="#5C5950", align="center", w=800))

    # -------------------------------------------------------------
    # 1. TRIGGER: Raw Lead Ingestion (Red / Coral Pill)
    # -------------------------------------------------------------
    y = 110
    w_pill = 240
    h_pill = 55
    elements.append(make_ellipse("trig_oval", cx - w_pill//2, y, w_pill, h_pill, stroke="#F87171", fill="#FEE2E2", stroke_width=2.5))
    elements.append(make_text("trig_txt", cx - w_pill//2, y + 16, "Raw Lead Trigger\n(Google Maps / Instagram)", font_size=14, font_family=1, color="#991B1B", align="center", w=w_pill))
    
    # Arrow down
    elements.extend(make_arrow("a_trig", cx, y + h_pill, cx, y + h_pill + 40, stroke="#181916"))

    # -------------------------------------------------------------
    # 2. Extract & Normalize Payload (Blue box)
    # -------------------------------------------------------------
    y += h_pill + 40
    w_box = 270
    h_box = 55
    elements.append(make_rect("b_norm", cx - w_box//2, y, w_box, h_box, stroke="#38BDF8", fill="#E0F2FE", stroke_width=2))
    elements.append(make_text("t_norm", cx - w_box//2, y + 16, "Extract & Normalize Venue Data\n(Website, IG handle, Address)", font_size=13, font_family=1, color="#0369A1", align="center", w=w_box))

    # Arrow down
    elements.extend(make_arrow("a_norm", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # -------------------------------------------------------------
    # 3. Idempotency & Dolibarr Deduplication Check (Blue box)
    # -------------------------------------------------------------
    y += h_box + 35
    elements.append(make_rect("b_idemp", cx - w_box//2, y, w_box, h_box, stroke="#38BDF8", fill="#E0F2FE", stroke_width=2))
    elements.append(make_text("t_idemp", cx - w_box//2, y + 16, "Idempotency & Dolibarr Check\n(Existing Customer / Active Lead?)", font_size=13, font_family=1, color="#0369A1", align="center", w=w_box))

    # Arrow down
    elements.extend(make_arrow("a_idemp", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # -------------------------------------------------------------
    # 4. Circuit Breaker / Daily Budget Check (Orange rounded box)
    # -------------------------------------------------------------
    y += h_box + 35
    w_cb = 300
    elements.append(make_rect("b_cb", cx - w_cb//2, y, w_cb, h_box, stroke="#FDBA74", fill="#FFEDD5", stroke_width=2))
    elements.append(make_text("t_cb", cx - w_cb//2, y + 16, "Budget & Rate Limit Check\n(Max €15/day scraping spend)", font_size=13, font_family=1, color="#C2410C", align="center", w=w_cb))

    # Side-Exit Arrow to right: TRIP -> Alert Cyril
    x_side = cx + w_cb//2
    elements.extend(make_arrow("a_cb_trip", x_side, y + h_box//2, x_side + 95, y + h_box//2, stroke="#EF4444", label="TRIP", label_color="#DC2626"))
    elements.append(make_rect("b_cb_stop", x_side + 95, y + 2, 160, 50, stroke="#F87171", fill="#FEE2E2", stroke_width=2))
    elements.append(make_text("t_cb_stop", x_side + 100, y + 16, "Alert Cyril Stop\n(Circuit Open)", font_size=13, font_family=1, color="#991B1B", align="center", w=150))

    # Arrow down (OK)
    elements.extend(make_arrow("a_cb_ok", cx, y + h_box, cx, y + h_box + 40, stroke="#15803D", label="OK", label_color="#15803D"))

    # -------------------------------------------------------------
    # 5. STAGE 0: Free German Legal Impressum Scraper (§ 5 TMG)
    # -------------------------------------------------------------
    y += h_box + 40
    w_imp = 320
    h_imp = 60
    elements.append(make_rect("b_imp", cx - w_imp//2, y, w_imp, h_imp, stroke="#4ADE80", fill="#DCFCE7", stroke_width=2))
    elements.append(make_text("t_imp", cx - w_imp//2, y + 12, "Stage 0: Free § 5 TMG Scraper\n(Scrape /impressum, /kontakt, /legal)", font_size=14, font_family=1, color="#166534", align="center", w=w_imp))

    # Arrow down to diamond
    elements.extend(make_arrow("a_imp_dia", cx, y + h_imp, cx, y + h_imp + 35, stroke="#181916"))

    # -------------------------------------------------------------
    # 6. DECISION DIAMOND: Owner Email in Impressum? (Yellow)
    # -------------------------------------------------------------
    y += h_imp + 35
    w_dia = 160
    h_dia = 110
    elements.append(make_diamond("d_imp", cx - w_dia//2, y, w_dia, h_dia, stroke="#EAB308", fill="#FEF08A", stroke_width=2.5))
    elements.append(make_text("t_dimp", cx - w_dia//2, y + 36, "Owner Email\nFound in\nImpressum?", font_size=13, font_family=1, color="#854D0E", align="center", w=w_dia))

    # Branch YES (Right) -> Fast-path green box (Saved €0.08 / Free)
    elements.extend(make_arrow("a_imp_yes", cx + w_dia//2, y + h_dia//2, cx + w_dia//2 + 95, y + h_dia//2, stroke="#15803D", label="YES (48%)", label_color="#15803D"))
    elements.append(make_rect("b_imp_bypass", cx + w_dia//2 + 95, y + 25, 175, 60, stroke="#4ADE80", fill="#DCFCE7", stroke_width=2))
    elements.append(make_text("t_imp_bypass", cx + w_dia//2 + 100, y + 36, "FREE (§ 5 TMG Success)\nSkip Bulk Paid APIs!", font_size=12, font_family=1, color="#166534", align="center", w=165))

    # Branch NO (Down) -> Stage 1 Bulk DB
    elements.extend(make_arrow("a_imp_no", cx, y + h_dia, cx, y + h_dia + 45, stroke="#181916", label="NO (52%)", label_color="#5C5950"))

    # -------------------------------------------------------------
    # 7. STAGE 1: GitLeads / Apollo Bulk DB (Blue box)
    # -------------------------------------------------------------
    y += h_dia + 45
    elements.append(make_rect("b_stg1", cx - w_box//2, y, w_box, h_box, stroke="#38BDF8", fill="#E0F2FE", stroke_width=2))
    elements.append(make_text("t_stg1", cx - w_box//2, y + 14, "Stage 1: GitLeads / Apollo Bulk DB\n(Low-Cost Query: €0.005 / check)", font_size=13, font_family=1, color="#0369A1", align="center", w=w_box))

    # Arrow down to diamond
    elements.extend(make_arrow("a_stg1_dia", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # -------------------------------------------------------------
    # 8. DECISION DIAMOND: Email Resolved in Apollo? (Yellow)
    # -------------------------------------------------------------
    y += h_box + 35
    elements.append(make_diamond("d_stg1", cx - w_dia//2, y, w_dia, h_dia, stroke="#EAB308", fill="#FEF08A", stroke_width=2.5))
    elements.append(make_text("t_dstg1", cx - w_dia//2, y + 36, "Email\nResolved in\nBulk DB?", font_size=13, font_family=1, color="#854D0E", align="center", w=w_dia))

    # Branch YES (Right) -> Passes down to validation
    elements.extend(make_arrow("a_stg1_yes", cx + w_dia//2, y + h_dia//2, cx + w_dia//2 + 95, y + h_dia//2, stroke="#15803D", label="YES (+24%)", label_color="#15803D"))
    elements.append(make_rect("b_stg1_pass", cx + w_dia//2 + 95, y + 30, 160, 50, stroke="#38BDF8", fill="#E0F2FE", stroke_width=2))
    elements.append(make_text("t_stg1_pass", cx + w_dia//2 + 100, y + 42, "Pass to Validation Gate\n(€0.005 Cost)", font_size=12, font_family=1, color="#0369A1", align="center", w=150))

    # Branch NO (Down) -> Stage 2 Deep Scraper
    elements.extend(make_arrow("a_stg1_no", cx, y + h_dia, cx, y + h_dia + 45, stroke="#181916", label="NO (28%)", label_color="#5C5950"))

    # -------------------------------------------------------------
    # 9. STAGE 2: Origami / Prospeo Deep Scraper (Orange box)
    # -------------------------------------------------------------
    y += h_dia + 45
    elements.append(make_rect("b_stg2", cx - w_box//2, y, w_box, h_box, stroke="#FDBA74", fill="#FFEDD5", stroke_width=2))
    elements.append(make_text("t_stg2", cx - w_box//2, y + 14, "Stage 2: Origami / Prospeo Scraper\n(Name Permutation + MX: €0.02)", font_size=13, font_family=1, color="#C2410C", align="center", w=w_box))

    # Arrow down to diamond
    elements.extend(make_arrow("a_stg2_dia", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # -------------------------------------------------------------
    # 10. DECISION DIAMOND: Deliverability Gate (MillionVerifier) (Yellow)
    # -------------------------------------------------------------
    y += h_box + 35
    w_dia_lg = 180
    h_dia_lg = 120
    elements.append(make_diamond("d_val", cx - w_dia_lg//2, y, w_dia_lg, h_dia_lg, stroke="#EAB308", fill="#FEF08A", stroke_width=2.5))
    elements.append(make_text("t_dval", cx - w_dia_lg//2, y + 36, "MillionVerifier\nDeliverability\nResult?", font_size=14, font_family=1, color="#854D0E", align="center", w=w_dia_lg))

    # Branch INVALID (Right) -> Discard red box
    elements.extend(make_arrow("a_val_inv", cx + w_dia_lg//2, y + h_dia_lg//2, cx + w_dia_lg//2 + 95, y + h_dia_lg//2, stroke="#EF4444", label="INVALID", label_color="#DC2626"))
    elements.append(make_rect("b_val_discard", cx + w_dia_lg//2 + 95, y + 30, 175, 60, stroke="#F87171", fill="#FEE2E2", stroke_width=2))
    elements.append(make_text("t_val_discard", cx + w_dia_lg//2 + 100, y + 42, "Discard Email\n(Protect Bounce Rate <1.5%)", font_size=12, font_family=1, color="#991B1B", align="center", w=165))

    # Branch RISKY / CATCH-ALL (Left) -> Slack low confidence orange box
    elements.extend(make_arrow("a_val_risk", cx - w_dia_lg//2, y + h_dia_lg//2, cx - w_dia_lg//2 - 95, y + h_dia_lg//2, stroke="#F59E0B", label="RISKY", label_color="#D97706"))
    elements.append(make_rect("b_val_risk", cx - w_dia_lg//2 - 270, y + 30, 175, 60, stroke="#FDBA74", fill="#FFEDD5", stroke_width=2))
    elements.append(make_text("t_val_risk", cx - w_dia_lg//2 - 265, y + 42, "Route to WhatsApp / Alt\n(Do not send cold email)", font_size=12, font_family=1, color="#C2410C", align="center", w=165))

    # Branch VALID (Down) -> Stage 3 Mobile Discovery
    elements.extend(make_arrow("a_val_valid", cx, y + h_dia_lg, cx, y + h_dia_lg + 45, stroke="#15803D", label="VALID", label_color="#15803D"))

    # -------------------------------------------------------------
    # 11. STAGE 3: LeadMagic Direct Mobile & WhatsApp (Orange box)
    # -------------------------------------------------------------
    y += h_dia_lg + 45
    elements.append(make_rect("b_mob", cx - w_box//2, y, w_box, h_box, stroke="#FDBA74", fill="#FFEDD5", stroke_width=2))
    elements.append(make_text("t_mob", cx - w_box//2, y + 14, "Stage 3: LeadMagic Mobile Discovery\n(Find Direct WhatsApp Phone)", font_size=13, font_family=1, color="#C2410C", align="center", w=w_box))

    # Arrow down to Agent 1 container
    elements.extend(make_arrow("a_mob_agent", cx, y + h_box, cx, y + h_box + 40, stroke="#181916"))

    # -------------------------------------------------------------
    # 12. AGENT 1 SUBGRAPH: ICP Qualification Agent (Purple Container)
    # -------------------------------------------------------------
    y += h_box + 40
    w_ag1 = 440
    h_ag1 = 125
    elements.append(make_rect("cont_ag1", cx - w_ag1//2, y, w_ag1, h_ag1, stroke="#C084FC", fill="#F3E8FF", stroke_width=2, roundness=3))
    elements.append(make_text("t_ag1_title", cx - w_ag1//2 + 15, y + 12, "Agent 1 — ICP Qualification Agent (Gemini Flash)", font_size=13, font_family=1, color="#7E22CE", align="left", w=400))
    
    # Inner boxes
    in_w = 180
    in_h = 55
    in_y = y + 45
    elements.append(make_rect("ag1_box1", cx - in_w - 15, in_y, in_w, in_h, stroke="#A855F7", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("ag1_t1", cx - in_w - 15, in_y + 14, "Analyze Menu &\nSeating (>30 seats)", font_size=12, font_family=1, color="#6B21A8", align="center", w=in_w))

    elements.extend(make_arrow("a_ag1_in", cx - 15, in_y + in_h//2, cx + 15, in_y + in_h//2, stroke="#A855F7"))

    elements.append(make_rect("ag1_box2", cx + 15, in_y, in_w, in_h, stroke="#A855F7", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("ag1_t2", cx + 15, in_y + 14, "Calculate ICP Score\n& Concept Fit", font_size=12, font_family=1, color="#6B21A8", align="center", w=in_w))

    # Arrow down to Confidence / ICP diamond
    elements.extend(make_arrow("a_ag1_dia", cx, y + h_ag1, cx, y + h_ag1 + 35, stroke="#181916"))

    # -------------------------------------------------------------
    # 13. DECISION DIAMOND: ICP Score >= 70? (Yellow)
    # -------------------------------------------------------------
    y += h_ag1 + 35
    elements.append(make_diamond("d_icp", cx - w_dia//2, y, w_dia, h_dia, stroke="#EAB308", fill="#FEF08A", stroke_width=2.5))
    elements.append(make_text("t_dicp", cx - w_dia//2, y + 36, "ICP Score\n>= 70?\n(High Fit)", font_size=13, font_family=1, color="#854D0E", align="center", w=w_dia))

    # Branch NO (Left) -> Archive orange box
    elements.extend(make_arrow("a_icp_no", cx - w_dia//2, y + h_dia//2, cx - w_dia//2 - 95, y + h_dia//2, stroke="#F59E0B", label="NO", label_color="#D97706"))
    elements.append(make_rect("b_icp_arch", cx - w_dia//2 - 270, y + 30, 175, 50, stroke="#FDBA74", fill="#FFEDD5", stroke_width=2))
    elements.append(make_text("t_icp_arch", cx - w_dia//2 - 265, y + 42, "Archive to Low-Priority\n(Nurture List)", font_size=12, font_family=1, color="#C2410C", align="center", w=165))

    # Branch YES (Down) -> Agent 2 Personalization
    elements.extend(make_arrow("a_icp_yes", cx, y + h_dia, cx, y + h_dia + 45, stroke="#15803D", label="YES", label_color="#15803D"))

    # -------------------------------------------------------------
    # 14. AGENT 2 SUBGRAPH: Pitch Personalization Engine (Green Container)
    # -------------------------------------------------------------
    y += h_dia + 45
    w_ag2 = 540
    h_ag2 = 125
    elements.append(make_rect("cont_ag2", cx - w_ag2//2, y, w_ag2, h_ag2, stroke="#4ADE80", fill="#DCFCE7", stroke_width=2, roundness=3))
    elements.append(make_text("t_ag2_title", cx - w_ag2//2 + 15, y + 12, "Agent 2 — Pitch Personalization Engine (Claude 3.5 Sonnet)", font_size=13, font_family=1, color="#166534", align="left", w=500))

    # 3 Inner boxes
    in_w3 = 150
    in_y3 = y + 45
    # Box 1
    elements.append(make_rect("ag2_b1", cx - in_w3 - 90, in_y3, in_w3, in_h, stroke="#22C55E", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("ag2_t1", cx - in_w3 - 90, in_y3 + 14, "Extract Cafe Aesthetic\n& Signature Blends", font_size=11.5, font_family=1, color="#15803D", align="center", w=in_w3))
    elements.extend(make_arrow("a_ag2_12", cx - 90, in_y3 + in_h//2, cx - 65, in_y3 + in_h//2, stroke="#22C55E"))

    # Box 2
    elements.append(make_rect("ag2_b2", cx - 65, in_y3, in_w3, in_h, stroke="#22C55E", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("ag2_t2", cx - 65, in_y3 + 14, "Draft €19 Discovery Box\nPersonalized Pitch", font_size=11.5, font_family=1, color="#15803D", align="center", w=in_w3))
    elements.extend(make_arrow("a_ag2_23", cx + in_w3 - 65, in_y3 + in_h//2, cx + in_w3 - 40, in_y3 + in_h//2, stroke="#22C55E"))

    # Box 3
    elements.append(make_rect("ag2_b3", cx + in_w3 - 40, in_y3, in_w3, in_h, stroke="#22C55E", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("ag2_t3", cx + in_w3 - 40, in_y3 + 14, "Queue Draft in Sidy's\nWhatsApp Inbox", font_size=11.5, font_family=1, color="#15803D", align="center", w=in_w3))

    # Arrow down to Human Approval Gate
    elements.extend(make_arrow("a_ag2_gate", cx, y + h_ag2, cx, y + h_ag2 + 35, stroke="#181916"))

    # -------------------------------------------------------------
    # 15. DECISION DIAMOND: Sidy Approves on WhatsApp? (Yellow Human Gate)
    # -------------------------------------------------------------
    y += h_ag2 + 35
    w_gate = 180
    h_gate = 110
    elements.append(make_diamond("d_gate", cx - w_gate//2, y, w_gate, h_gate, stroke="#EAB308", fill="#FEF08A", stroke_width=3))
    elements.append(make_text("t_dgate", cx - w_gate//2, y + 36, "Sidy Approves\non WhatsApp?\n(Human Gate)", font_size=13.5, font_family=1, color="#854D0E", align="center", w=w_gate))

    # Branch REJECT / EDIT (Right) -> Red box
    elements.extend(make_arrow("a_gate_no", cx + w_gate//2, y + h_gate//2, cx + w_gate//2 + 95, y + h_gate//2, stroke="#EF4444", label="REJECT", label_color="#DC2626"))
    elements.append(make_rect("b_gate_no", cx + w_gate//2 + 95, y + 30, 160, 50, stroke="#F87171", fill="#FEE2E2", stroke_width=2))
    elements.append(make_text("t_gate_no", cx + w_gate//2 + 100, y + 42, "Discard / Edit Draft\n(Zero Brand Risk)", font_size=12, font_family=1, color="#991B1B", align="center", w=150))

    # Branch PASS / 1-TAP APPROVE (Down) -> Execution
    elements.extend(make_arrow("a_gate_pass", cx, y + h_gate, cx, y + h_gate + 45, stroke="#15803D", label="1-TAP APPROVE", label_color="#15803D"))

    # -------------------------------------------------------------
    # 16. EXECUTE: Temporal Activity Dispatch (Blue box)
    # -------------------------------------------------------------
    y += h_gate + 45
    w_exec = 340
    h_exec = 65
    elements.append(make_rect("b_exec", cx - w_exec//2, y, w_exec, h_exec, stroke="#38BDF8", fill="#E0F2FE", stroke_width=2))
    elements.append(make_text("t_exec", cx - w_exec//2, y + 14, "Temporal Execution Activity\n(Send WhatsApp Outreach + Create Dolibarr Lead)", font_size=13, font_family=1, color="#0369A1", align="center", w=w_exec))

    # Arrow down
    elements.extend(make_arrow("a_exec_log", cx, y + h_exec, cx, y + h_exec + 35, stroke="#181916"))

    # -------------------------------------------------------------
    # 17. LOG: Sync Entity to Dolibarr CRM & PostgreSQL (Green box)
    # -------------------------------------------------------------
    y += h_exec + 35
    elements.append(make_rect("b_log", cx - w_exec//2, y, w_exec, h_exec, stroke="#4ADE80", fill="#DCFCE7", stroke_width=2))
    elements.append(make_text("t_log", cx - w_exec//2, y + 14, "Log Entity to Dolibarr CRM &\nPostgreSQL Audit Ledger", font_size=13.5, font_family=1, color="#166534", align="center", w=w_exec))

    # Arrow down
    elements.extend(make_arrow("a_log_end", cx, y + h_exec, cx, y + h_exec + 35, stroke="#181916"))

    # -------------------------------------------------------------
    # 18. TERMINAL / DURABLE TIMER: Day-4 Follow-Up & Refill (Green Pill)
    # -------------------------------------------------------------
    y += h_exec + 35
    w_end = 320
    h_end = 60
    elements.append(make_rect("b_end", cx - w_end//2, y, w_end, h_end, stroke="#22C55E", fill="#DCFCE7", stroke_width=2.5, roundness=3))
    elements.append(make_text("t_end", cx - w_end//2, y + 12, "Durable Temporal Timer\n(Day-4 Tasting Check-In & Day-25 Refill)", font_size=13.5, font_family=1, color="#15803D", align="center", w=w_end))

    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": "#FFFFFF"
        },
        "files": {}
    }
    return doc, y + h_end + 60

def main():
    doc, total_height = build_flowchart()
    base_dir = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas"
    out_file = os.path.join(base_dir, "alandas_self_healing_revenue_pipeline.excalidraw")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
    print(f"[SUCCESS] Flowchart Excalidraw generated at: {out_file} (Canvas height: {total_height}px)")

if __name__ == "__main__":
    main()
