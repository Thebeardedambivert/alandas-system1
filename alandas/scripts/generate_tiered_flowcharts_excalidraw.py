"""
Generate Excalidraw Flowcharts for all 3 Tiers matching Cyril's exact visual language:
1. tier1_essential_automation_flowchart.excalidraw
2. tier2_governed_intelligence_flowchart.excalidraw
3. tier3_autonomous_platform_flowchart.excalidraw
4. master_3tier_architecture_flowcharts.excalidraw (Side-by-side comparison)
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

def make_text(id_str, x, y, text, font_size=15, font_family=1, color="#181916", align="center", w=200):
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
        mid_x = start_x + dx * 0.5
        mid_y = start_y + dy * 0.5
        if abs(dx) > abs(dy):
            lx = mid_x - 35
            ly = mid_y - 18
        else:
            lx = mid_x + 8
            ly = mid_y - 10
        elements.append(make_text(f"{id_str}_lbl", lx, ly, label, font_size=12, font_family=1, color=label_color, align="center", w=70))
    return elements

# =============================================================================
# TIER 1 FLOWCHART
# =============================================================================
def build_tier1_flowchart(cx=480):
    from generate_waterfall_flowchart_excalidraw import build_flowchart
    doc, h = build_flowchart()
    doc["elements"][0] = make_text("h_title", cx - 450, 30, "Tier 1: Essential Revenue Automation — Human-Directed Architecture", font_size=23, font_family=1, color="#181916", align="center", w=900)
    return doc, h

# =============================================================================
# TIER 2 FLOWCHART: GOVERNED DECISION INTELLIGENCE
# =============================================================================
def build_tier2_flowchart(cx=480):
    elements = []
    
    # 0. Header
    elements.append(make_text("t2_title", cx - 450, 30, "Tier 2: Professional Revenue Intelligence — Governed Decision Architecture", font_size=23, font_family=1, color="#181916", align="center", w=900))
    elements.append(make_text("t2_sub", cx - 400, 65, "Policy Engines  •  Decision Contracts  •  Post-Action Verification  •  Blast Radius: Strictly Bounded", font_size=14, font_family=1, color="#C48737", align="center", w=800))

    # 1. Trigger: Meta Ad Performance Signal (Red Oval)
    y = 110
    w_pill = 270
    h_pill = 55
    elements.append(make_ellipse("t2_trig", cx - w_pill//2, y, w_pill, h_pill, stroke="#F87171", fill="#FEE2E2", stroke_width=2.5))
    elements.append(make_text("t2_trig_t", cx - w_pill//2, y + 14, "Ad Spend & Refill Signal Trigger\n(Meta ROAS > 4.0x / Day-20 Refill)", font_size=13, font_family=1, color="#991B1B", align="center", w=w_pill))
    elements.extend(make_arrow("t2_a1", cx, y + h_pill, cx, y + h_pill + 40, stroke="#181916"))

    # 2. Ingest Metrics & Query Active Campaign (Blue box)
    y += h_pill + 40
    w_box = 290
    h_box = 55
    elements.append(make_rect("t2_ingest", cx - w_box//2, y, w_box, h_box, stroke="#38BDF8", fill="#E0F2FE", stroke_width=2))
    elements.append(make_text("t2_ingest_t", cx - w_box//2, y + 14, "Ingest Meta Campaign Telemetry\n(CPA, CTR, Daily Spend, Revenue)", font_size=13, font_family=1, color="#0369A1", align="center", w=w_box))
    elements.extend(make_arrow("t2_a2", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # 3. Selective LangGraph Container: Creative & Budget Reasoning (Purple Container)
    y += h_box + 35
    w_ag = 480
    h_ag = 125
    elements.append(make_rect("t2_ag_cont", cx - w_ag//2, y, w_ag, h_ag, stroke="#C084FC", fill="#F3E8FF", stroke_width=2, roundness=3))
    elements.append(make_text("t2_ag_title", cx - w_ag//2 + 15, y + 12, "Selective LangGraph Agent — Budget & Creative Reasoning", font_size=13, font_family=1, color="#7E22CE", align="left", w=450))
    
    in_w = 200
    in_h = 55
    in_y = y + 45
    elements.append(make_rect("t2_in1", cx - in_w - 15, in_y, in_w, in_h, stroke="#A855F7", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t2_in1_t", cx - in_w - 15, in_y + 14, "Evaluate 7-Day Performance\n(ROAS = 4.2x, CPA = €12)", font_size=12, font_family=1, color="#6B21A8", align="center", w=in_w))
    elements.extend(make_arrow("t2_ain", cx - 15, in_y + in_h//2, cx + 15, in_y + in_h//2, stroke="#A855F7"))

    elements.append(make_rect("t2_in2", cx + 15, in_y, in_w, in_h, stroke="#A855F7", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t2_in2_t", cx + 15, in_y + 14, "Propose Budget Delta:\nIncrease €30 ➔ €39/day (+30%)", font_size=12, font_family=1, color="#6B21A8", align="center", w=in_w))
    elements.extend(make_arrow("t2_a3", cx, y + h_ag, cx, y + h_ag + 40, stroke="#181916"))

    # 4. Construct Typed Decision Contract (Orange Box)
    y += h_ag + 40
    elements.append(make_rect("t2_contract", cx - w_box//2, y, w_box, h_box, stroke="#FDBA74", fill="#FFEDD5", stroke_width=2))
    elements.append(make_text("t2_contract_t", cx - w_box//2, y + 14, "Serialize to Typed Decision Contract\n(Schema: action, delta, bounds, target)", font_size=13, font_family=1, color="#C2410C", align="center", w=w_box))
    elements.extend(make_arrow("t2_a4", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # 5. DECISION DIAMOND: Contract Schema Validation (Yellow)
    y += h_box + 35
    w_dia = 170
    h_dia = 110
    elements.append(make_diamond("t2_d_schema", cx - w_dia//2, y, w_dia, h_dia, stroke="#EAB308", fill="#FEF08A", stroke_width=2.5))
    elements.append(make_text("t2_d_schema_t", cx - w_dia//2, y + 36, "JSON Schema\nValid?\n(Pydantic)", font_size=13, font_family=1, color="#854D0E", align="center", w=w_dia))

    # Branch FAIL (Right) -> Red box
    elements.extend(make_arrow("t2_asch_f", cx + w_dia//2, y + h_dia//2, cx + w_dia//2 + 95, y + h_dia//2, stroke="#EF4444", label="FAIL", label_color="#DC2626"))
    elements.append(make_rect("t2_sch_bad", cx + w_dia//2 + 95, y + 30, 165, 50, stroke="#F87171", fill="#FEE2E2", stroke_width=2))
    elements.append(make_text("t2_sch_bad_t", cx + w_dia//2 + 100, y + 42, "Reject Malformed Contract\nAlert Cyril (Zero Action)", font_size=11.5, font_family=1, color="#991B1B", align="center", w=155))

    # Branch PASS (Down)
    elements.extend(make_arrow("t2_asch_p", cx, y + h_dia, cx, y + h_dia + 45, stroke="#15803D", label="PASS", label_color="#15803D"))

    # 6. Policy Engine Evaluation Container (Blue Box)
    y += h_dia + 45
    w_pol = 500
    h_pol = 115
    elements.append(make_rect("t2_pol_cont", cx - w_pol//2, y, w_pol, h_pol, stroke="#0284C7", fill="#E0F2FE", stroke_width=2, roundness=3))
    elements.append(make_text("t2_pol_t", cx - w_pol//2 + 15, y + 12, "Policy Engine Independent Evaluation (Deterministic Rules)", font_size=13, font_family=1, color="#0369A1", align="left", w=470))
    
    in_w3 = 145
    in_y3 = y + 45
    elements.append(make_rect("t2_p1", cx - in_w3 - 85, in_y3, in_w3, 50, stroke="#38BDF8", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t2_p1_t", cx - in_w3 - 85, in_y3 + 12, "Daily Ceiling Check\n(€39 <= €50 cap)", font_size=11.5, font_family=1, color="#0369A1", align="center", w=in_w3))
    elements.extend(make_arrow("t2_ap1", cx - 85, in_y3 + 25, cx - 60, in_y3 + 25, stroke="#0284C7"))

    elements.append(make_rect("t2_p2", cx - 60, in_y3, in_w3, 50, stroke="#38BDF8", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t2_p2_t", cx - 60, in_y3 + 12, "Min Run Time Check\n(Active > 7 Days)", font_size=11.5, font_family=1, color="#0369A1", align="center", w=in_w3))
    elements.extend(make_arrow("t2_ap2", cx + in_w3 - 60, in_y3 + 25, cx + in_w3 - 35, in_y3 + 25, stroke="#0284C7"))

    elements.append(make_rect("t2_p3", cx + in_w3 - 35, in_y3, in_w3, 50, stroke="#38BDF8", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t2_p3_t", cx + in_w3 - 35, in_y3 + 12, "Max Daily Delta\n(<= +35% Rule)", font_size=11.5, font_family=1, color="#0369A1", align="center", w=in_w3))
    elements.extend(make_arrow("t2_a5", cx, y + h_pol, cx, y + h_pol + 40, stroke="#181916"))

    # 7. DECISION DIAMOND: Policy Engine Compliant? (Yellow)
    y += h_pol + 40
    elements.append(make_diamond("t2_d_pol", cx - w_dia//2, y, w_dia, h_dia, stroke="#EAB308", fill="#FEF08A", stroke_width=2.5))
    elements.append(make_text("t2_d_pol_t", cx - w_dia//2, y + 36, "Policy Engine\nPassed?\n(Zero Risk)", font_size=13, font_family=1, color="#854D0E", align="center", w=w_dia))

    # Branch VIOLATION (Right) -> Red box
    elements.extend(make_arrow("t2_apol_v", cx + w_dia//2, y + h_dia//2, cx + w_dia//2 + 95, y + h_dia//2, stroke="#EF4444", label="VIOLATION", label_color="#DC2626"))
    elements.append(make_rect("t2_pol_bad", cx + w_dia//2 + 95, y + 30, 165, 50, stroke="#F87171", fill="#FEE2E2", stroke_width=2))
    elements.append(make_text("t2_pol_bad_t", cx + w_dia//2 + 100, y + 42, "Halt Execution\nLog Policy Breach", font_size=12, font_family=1, color="#991B1B", align="center", w=155))

    # Branch COMPLIANT (Down)
    elements.extend(make_arrow("t2_apol_c", cx, y + h_dia, cx, y + h_dia + 45, stroke="#15803D", label="COMPLIANT", label_color="#15803D"))

    # 8. DECISION DIAMOND: Material Change Requires Human Gate? (Yellow)
    y += h_dia + 45
    elements.append(make_diamond("t2_d_gate", cx - w_dia//2, y, w_dia, h_dia, stroke="#EAB308", fill="#FEF08A", stroke_width=3))
    elements.append(make_text("t2_d_gate_t", cx - w_dia//2, y + 36, "Delta > €5/day?\n(Human Sign-Off\nRequired)", font_size=13, font_family=1, color="#854D0E", align="center", w=w_dia))

    # Branch NO / MINOR (Left) -> Skip straight to execute
    elements.extend(make_arrow("t2_agate_no", cx - w_dia//2, y + h_dia//2, cx - w_dia//2 - 95, y + h_dia//2, stroke="#15803D", label="NO (<= €5)", label_color="#15803D"))
    elements.append(make_rect("t2_gate_auto", cx - w_dia//2 - 270, y + 30, 175, 50, stroke="#4ADE80", fill="#DCFCE7", stroke_width=2))
    elements.append(make_text("t2_gate_auto_t", cx - w_dia//2 - 265, y + 42, "Auto-Execution Permitted\n(Within Policy Bounds)", font_size=12, font_family=1, color="#166534", align="center", w=165))

    # Branch YES / HUMAN (Down) -> Sidy WhatsApp 1-Tap Approval
    elements.extend(make_arrow("t2_agate_yes", cx, y + h_dia, cx, y + h_dia + 45, stroke="#C48737", label="YES (+€9/day)", label_color="#C48737"))

    # 9. Sidy WhatsApp Approval Box (Ochre / Orange)
    y += h_dia + 45
    elements.append(make_rect("t2_sidy_app", cx - w_box//2, y, w_box, h_box, stroke="#C48737", fill="#FCF4E8", stroke_width=2.5))
    elements.append(make_text("t2_sidy_app_t", cx - w_box//2, y + 14, "Sidy 1-Tap WhatsApp Approval\n[Approve +€9/day] or [Reject]", font_size=13, font_family=1, color="#9A6622", align="center", w=w_box))
    elements.extend(make_arrow("t2_a6", cx, y + h_box, cx, y + h_box + 40, stroke="#15803D", label="APPROVED", label_color="#15803D"))

    # 10. Temporal Activity: Dispatch Meta API Update (Blue Box)
    y += h_box + 40
    elements.append(make_rect("t2_dispatch", cx - w_box//2, y, w_box, h_box, stroke="#38BDF8", fill="#E0F2FE", stroke_width=2))
    elements.append(make_text("t2_dispatch_t", cx - w_box//2, y + 14, "Temporal Activity Dispatch:\nUpdate Meta AdSet Budget to €39.00", font_size=13, font_family=1, color="#0369A1", align="center", w=w_box))
    elements.extend(make_arrow("t2_a7", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # 11. Post-Action Verification Query (Green Box)
    y += h_box + 35
    elements.append(make_rect("t2_verify", cx - w_box//2, y, w_box, h_box, stroke="#4ADE80", fill="#DCFCE7", stroke_width=2))
    elements.append(make_text("t2_verify_t", cx - w_box//2, y + 14, "Post-Action Verification Query\n(Re-query Meta API to confirm state = €39.00)", font_size=13, font_family=1, color="#166534", align="center", w=w_box))
    elements.extend(make_arrow("t2_a8", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # 12. Terminal: Write Immutable Audit Trace to PostgreSQL (Green Pill)
    y += h_box + 35
    w_end = 340
    h_end = 60
    elements.append(make_rect("t2_end", cx - w_end//2, y, w_end, h_end, stroke="#22C55E", fill="#DCFCE7", stroke_width=2.5, roundness=3))
    elements.append(make_text("t2_end_t", cx - w_end//2, y + 12, "Immutable Audit Trail Written\n(PostgreSQL + OpenTelemetry Distributed Trace)", font_size=13.5, font_family=1, color="#15803D", align="center", w=w_end))

    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#FFFFFF"},
        "files": {}
    }
    return doc, y + h_end + 60

# =============================================================================
# TIER 3 FLOWCHART: AUTONOMOUS CLOSED-LOOP FLYWHEEL
# =============================================================================
def build_tier3_flowchart(cx=480):
    elements = []
    
    # 0. Header
    elements.append(make_text("t3_title", cx - 450, 30, "Tier 3: Autonomous Revenue Platform — Closed-Loop Commercial Flywheel", font_size=23, font_family=1, color="#181916", align="center", w=900))
    elements.append(make_text("t3_sub", cx - 400, 65, "Multi-Agent Coordination  •  Model Context Protocol (MCP)  •  Circuit Breakers  •  Autopilot Flywheel", font_size=14, font_family=1, color="#2F5339", align="center", w=800))

    # 1. Trigger: Real-Time Commercial Telemetry Stream (Red Oval)
    y = 110
    w_pill = 290
    h_pill = 55
    elements.append(make_ellipse("t3_trig", cx - w_pill//2, y, w_pill, h_pill, stroke="#F87171", fill="#FEE2E2", stroke_width=2.5))
    elements.append(make_text("t3_trig_t", cx - w_pill//2, y + 14, "Commercial Event Stream (PubSub)\n(Refill Cycles across 100+ Partner Accounts)", font_size=13, font_family=1, color="#991B1B", align="center", w=w_pill))
    elements.extend(make_arrow("t3_a1", cx, y + h_pill, cx, y + h_pill + 40, stroke="#181916"))

    # 2. Shared Revenue State Graph (Blue Box)
    y += h_pill + 40
    w_box = 300
    h_box = 55
    elements.append(make_rect("t3_shared", cx - w_box//2, y, w_box, h_box, stroke="#38BDF8", fill="#E0F2FE", stroke_width=2))
    elements.append(make_text("t3_shared_t", cx - w_box//2, y + 14, "Shared Revenue State Graph\n(LTV, Account Health, Inventory Velocity)", font_size=13, font_family=1, color="#0369A1", align="center", w=w_box))
    elements.extend(make_arrow("t3_a2", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # 3. Domain Specialist Agents Container (Purple Box)
    y += h_box + 35
    w_dom = 540
    h_dom = 125
    elements.append(make_rect("t3_dom_cont", cx - w_dom//2, y, w_dom, h_dom, stroke="#C084FC", fill="#F3E8FF", stroke_width=2, roundness=3))
    elements.append(make_text("t3_dom_t", cx - w_dom//2 + 15, y + 12, "Domain Specialist Agents (Temporal Coordinated)", font_size=13, font_family=1, color="#7E22CE", align="left", w=500))
    
    in_w3 = 150
    in_y3 = y + 45
    elements.append(make_rect("t3_d1", cx - in_w3 - 90, in_y3, in_w3, 55, stroke="#A855F7", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t3_d1_t", cx - in_w3 - 90, in_y3 + 12, "Acquisition Agent\n(Scrape & Qualify)", font_size=12, font_family=1, color="#6B21A8", align="center", w=in_w3))
    elements.extend(make_arrow("t3_ad1", cx - 90, in_y3 + 27, cx - 65, in_y3 + 27, stroke="#A855F7"))

    elements.append(make_rect("t3_d2", cx - 65, in_y3, in_w3, 55, stroke="#A855F7", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t3_d2_t", cx - 65, in_y3 + 12, "Creative Ads Agent\n(Ad Generation & ROAS)", font_size=12, font_family=1, color="#6B21A8", align="center", w=in_w3))
    elements.extend(make_arrow("t3_ad2", cx + in_w3 - 65, in_y3 + 27, cx + in_w3 - 40, in_y3 + 27, stroke="#A855F7"))

    elements.append(make_rect("t3_d3", cx + in_w3 - 40, in_y3, in_w3, 55, stroke="#A855F7", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t3_d3_t", cx + in_w3 - 40, in_y3 + 12, "RevOps Agent\n(Refills & Invoicing)", font_size=12, font_family=1, color="#6B21A8", align="center", w=in_w3))
    elements.extend(make_arrow("t3_a3", cx, y + h_dom, cx, y + h_dom + 40, stroke="#181916"))

    # 4. Continuous Experimentation Engine (Orange Box)
    y += h_dom + 40
    elements.append(make_rect("t3_exp", cx - w_box//2, y, w_box, h_box, stroke="#FDBA74", fill="#FFEDD5", stroke_width=2))
    elements.append(make_text("t3_exp_t", cx - w_box//2, y + 14, "Continuous Experimentation Engine\n(Munich Earl Grey 2x Refill ➔ Formulate Ad)", font_size=13, font_family=1, color="#C2410C", align="center", w=w_box))
    elements.extend(make_arrow("t3_a4", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # 5. DECISION DIAMOND: Automated Circuit Breaker (Yellow)
    y += h_box + 35
    w_dia = 180
    h_dia = 110
    elements.append(make_diamond("t3_d_cb", cx - w_dia//2, y, w_dia, h_dia, stroke="#EAB308", fill="#FEF08A", stroke_width=2.5))
    elements.append(make_text("t3_d_cb_t", cx - w_dia//2, y + 36, "Circuit Breakers\nNormal?\n(Spend & Anomaly)", font_size=13, font_family=1, color="#854D0E", align="center", w=w_dia))

    # Branch ANOMALY (Right) -> Red Halt Box
    elements.extend(make_arrow("t3_acb_a", cx + w_dia//2, y + h_dia//2, cx + w_dia//2 + 95, y + h_dia//2, stroke="#EF4444", label="ANOMALY", label_color="#DC2626"))
    elements.append(make_rect("t3_cb_halt", cx + w_dia//2 + 95, y + 30, 165, 50, stroke="#F87171", fill="#FEE2E2", stroke_width=2))
    elements.append(make_text("t3_cb_halt_t", cx + w_dia//2 + 100, y + 42, "Instant System Pause\nAlert Cyril / Sidy", font_size=12, font_family=1, color="#991B1B", align="center", w=155))

    # Branch NORMAL (Down)
    elements.extend(make_arrow("t3_acb_n", cx, y + h_dia, cx, y + h_dia + 45, stroke="#15803D", label="NORMAL", label_color="#15803D"))

    # 6. Model Context Protocol (MCP) Tool Invocations (Green Box)
    y += h_dia + 45
    w_mcp = 520
    h_mcp = 115
    elements.append(make_rect("t3_mcp_cont", cx - w_mcp//2, y, w_mcp, h_mcp, stroke="#22C55E", fill="#DCFCE7", stroke_width=2, roundness=3))
    elements.append(make_text("t3_mcp_t", cx - w_mcp//2 + 15, y + 12, "Model Context Protocol (MCP) Standardized Tool Invocations", font_size=13, font_family=1, color="#166534", align="left", w=490))
    
    in_w3_mcp = 150
    elements.append(make_rect("t3_m1", cx - in_w3_mcp - 85, in_y3 + 450, in_w3_mcp, 50, stroke="#16A34A", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t3_m1_t", cx - in_w3_mcp - 85, in_y3 + 462, "mcp_meta_ads\n(Auto-Deploy Munich Ad)", font_size=11.5, font_family=1, color="#15803D", align="center", w=in_w3_mcp))

    elements.append(make_rect("t3_m2", cx - 60, in_y3 + 450, in_w3_mcp, 50, stroke="#16A34A", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t3_m2_t", cx - 60, in_y3 + 462, "mcp_dolibarr_crm\n(Reserve 50kg Earl Grey)", font_size=11.5, font_family=1, color="#15803D", align="center", w=in_w3_mcp))

    elements.append(make_rect("t3_m3", cx + in_w3_mcp - 35, in_y3 + 450, in_w3_mcp, 50, stroke="#16A34A", fill="#FFFFFF", stroke_width=1.5))
    elements.append(make_text("t3_m3_t", cx + in_w3_mcp - 35, in_y3 + 462, "mcp_warehouse_log\n(Trigger Berlin ➔ MUC)", font_size=11.5, font_family=1, color="#15803D", align="center", w=in_w3_mcp))
    elements.extend(make_arrow("t3_a5", cx, y + h_mcp, cx, y + h_mcp + 40, stroke="#181916"))

    # 7. DECISION DIAMOND: Enterprise Regulatory & Margin Gate (Yellow)
    y += h_mcp + 40
    elements.append(make_diamond("t3_d_reg", cx - w_dia//2, y, w_dia, h_dia, stroke="#EAB308", fill="#FEF08A", stroke_width=2.5))
    elements.append(make_text("t3_d_reg_t", cx - w_dia//2, y + 36, "German Food Regs\n& Gross Margin\n>= 75%?", font_size=13, font_family=1, color="#854D0E", align="center", w=w_dia))

    # Branch FAIL (Right)
    elements.extend(make_arrow("t3_areg_f", cx + w_dia//2, y + h_dia//2, cx + w_dia//2 + 95, y + h_dia//2, stroke="#EF4444", label="NON-COMPLIANT", label_color="#DC2626"))
    elements.append(make_rect("t3_reg_bad", cx + w_dia//2 + 95, y + 30, 165, 50, stroke="#F87171", fill="#FEE2E2", stroke_width=2))
    elements.append(make_text("t3_reg_bad_t", cx + w_dia//2 + 100, y + 42, "Reject Tool Call\nFlag Botanical Labeling", font_size=11.5, font_family=1, color="#991B1B", align="center", w=155))

    # Branch PASS (Down)
    elements.extend(make_arrow("t3_areg_p", cx, y + h_dia, cx, y + h_dia + 45, stroke="#15803D", label="COMPLIANT", label_color="#15803D"))

    # 8. Closed-Loop Execution & Real-Time Attribution (Green Box)
    y += h_dia + 45
    elements.append(make_rect("t3_exec", cx - w_box//2, y, w_box, h_box, stroke="#4ADE80", fill="#DCFCE7", stroke_width=2))
    elements.append(make_text("t3_exec_t", cx - w_box//2, y + 14, "Execute Autonomous Actions Across Cities\n(Munich Ad Deployed + Warehouses Synced)", font_size=13, font_family=1, color="#166534", align="center", w=w_box))
    elements.extend(make_arrow("t3_a6", cx, y + h_box, cx, y + h_box + 35, stroke="#181916"))

    # 9. Terminal / Flywheel Feedback (Green Pill)
    y += h_box + 35
    w_end = 360
    h_end = 65
    elements.append(make_rect("t3_end", cx - w_end//2, y, w_end, h_end, stroke="#22C55E", fill="#DCFCE7", stroke_width=2.5, roundness=3))
    elements.append(make_text("t3_end_t", cx - w_end//2, y + 12, "Autonomous Flywheel Active (100+ Accounts)\nLTV Reorder Velocity Continuously Trains Ad Agent\nSidy Acts as Executive Supervisor (<2 hrs/wk)", font_size=13, font_family=1, color="#15803D", align="center", w=w_end))

    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#FFFFFF"},
        "files": {}
    }
    return doc, y + h_end + 60

def main():
    base_dir = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas"
    
    # 1. Tier 1
    t1_doc, h1 = build_tier1_flowchart()
    p1 = os.path.join(base_dir, "tier1_essential_automation_flowchart.excalidraw")
    with open(p1, "w", encoding="utf-8") as f:
        json.dump(t1_doc, f, indent=2)
    print(f"[SUCCESS] Tier 1 Flowchart: {p1} ({h1}px)")

    # 2. Tier 2
    t2_doc, h2 = build_tier2_flowchart()
    p2 = os.path.join(base_dir, "tier2_governed_intelligence_flowchart.excalidraw")
    with open(p2, "w", encoding="utf-8") as f:
        json.dump(t2_doc, f, indent=2)
    print(f"[SUCCESS] Tier 2 Flowchart: {p2} ({h2}px)")

    # 3. Tier 3
    t3_doc, h3 = build_tier3_flowchart()
    p3 = os.path.join(base_dir, "tier3_autonomous_platform_flowchart.excalidraw")
    with open(p3, "w", encoding="utf-8") as f:
        json.dump(t3_doc, f, indent=2)
    print(f"[SUCCESS] Tier 3 Flowchart: {p3} ({h3}px)")

if __name__ == "__main__":
    main()
