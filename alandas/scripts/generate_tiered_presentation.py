"""
Generate Tiered Revenue Architecture Presentation & System Design Artifacts
Outputs:
1. Alandas_Tiered_Architecture_Presentation.html (16:9 Interactive Deck with Fixed Stage & Luxury Styling)
2. Alandas_Tiered_Architecture_System.pptx (Native PowerPoint 16:9 Presentation)
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# 1. HTML PRESENTATION BUILDER
# -----------------------------------------------------------------------------
def build_html_presentation(output_html_path):
    print("Generating Interactive 16:9 HTML Presentation...")
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alandas Tea Berlin — Tiered Revenue Architecture & System Design</title>

  <!-- Google Fonts: Luxury Editorial Serif & Precision Technical Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    /* ===========================================
       THEME VARIABLES & DESIGN SYSTEM
       =========================================== */
    :root {
      --stage-bg: #0C0F0C;
      --slide-bg: #F9F7F2;
      --slide-gradient: radial-gradient(1300px 900px at 50% 0%, #FFFFFF 0%, #F9F7F2 65%, #F2EEE4 100%);
      
      --font-display: 'Playfair Display', Georgia, serif;
      --font-body: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      --olive: #444C32;
      --olive-dark: #2E3422;
      --olive-light: #EEF2E8;
      --olive-border: #D1D9C5;

      --ochre: #C48737;
      --ochre-dark: #9A6622;
      --ochre-light: #FCF4E8;
      --ochre-border: #F0DFC2;

      --forest: #2F5339;
      --forest-dark: #1E3725;
      --forest-light: #EDF5EF;

      --text-main: #181916;
      --text-muted: #5C5950;
      --text-subtle: #8C887C;
      
      --card-bg: #FFFFFF;
      --card-alt: #F3EFE6;
      --border: #E4DFD3;
      --border-light: #EFECE4;

      --shadow-sm: 0 4px 16px rgba(24, 25, 22, 0.04);
      --shadow-md: 0 10px 30px rgba(24, 25, 22, 0.07);
      --shadow-lg: 0 20px 48px rgba(24, 25, 22, 0.10);
      
      --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
      --duration-normal: 0.5s;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    /* MANDATORY 16:9 VIEWPORT CONTAINER */
    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: var(--stage-bg);
      font-family: var(--font-body);
      color: var(--text-main);
      -webkit-font-smoothing: antialiased;
    }

    .deck-viewport {
      position: fixed;
      inset: 0;
      overflow: hidden;
      background: var(--stage-bg);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .deck-stage {
      position: absolute;
      width: 1920px;
      height: 1080px;
      left: 50%;
      top: 50%;
      transform-origin: center center;
      background: var(--slide-bg);
      background-image: var(--slide-gradient);
      box-shadow: 0 0 80px rgba(0, 0, 0, 0.85);
      border-radius: 4px;
      overflow: hidden;
    }

    .slide {
      position: absolute;
      inset: 0;
      width: 1920px;
      height: 1080px;
      padding: 70px 90px 60px 90px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
      transition: opacity var(--duration-normal) var(--ease-out-expo), visibility var(--duration-normal);
    }

    .slide.active {
      opacity: 1;
      visibility: visible;
      pointer-events: auto;
      z-index: 2;
    }

    /* TYPOGRAPHY HIERARCHY */
    .slide-header {
      margin-bottom: 24px;
    }
    .kicker {
      font-family: var(--font-mono);
      font-size: 15px;
      font-weight: 700;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--olive);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .kicker::before {
      content: "";
      display: inline-block;
      width: 24px;
      height: 2px;
      background: var(--olive);
    }
    .slide-title {
      font-family: var(--font-display);
      font-size: 46px;
      font-weight: 700;
      line-height: 1.15;
      color: var(--text-main);
      letter-spacing: -0.01em;
      margin-bottom: 10px;
    }
    .slide-subtitle {
      font-size: 20px;
      line-height: 1.45;
      color: var(--text-muted);
      max-width: 1500px;
    }

    /* FOOTER */
    .slide-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 18px;
      border-top: 1px solid var(--border);
      font-family: var(--font-mono);
      font-size: 13px;
      color: var(--text-subtle);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .footer-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 600;
      color: var(--olive-dark);
    }
    .footer-meta {
      display: flex;
      align-items: center;
      gap: 24px;
    }

    /* CONTENT LAYOUTS */
    .slide-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 0;
      margin: 10px 0 20px 0;
    }

    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 28px;
      height: 100%;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 32px;
      height: 100%;
    }
    .grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 24px;
      height: 100%;
    }

    /* CARDS */
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px 30px;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      box-shadow: var(--shadow-sm);
      position: relative;
      overflow: hidden;
    }
    .card.accent-olive {
      border-top: 5px solid var(--olive);
    }
    .card.accent-ochre {
      border-top: 5px solid var(--ochre);
    }
    .card.accent-forest {
      border-top: 5px solid var(--forest);
    }
    .card.highlight {
      background: #FFFFFF;
      border: 2px solid var(--olive);
      box-shadow: var(--shadow-md);
    }

    .card-tag {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin-bottom: 12px;
      display: inline-block;
    }
    .tag-olive { color: var(--olive); }
    .tag-ochre { color: var(--ochre); }
    .tag-forest { color: var(--forest); }

    .card-title {
      font-family: var(--font-display);
      font-size: 26px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 14px;
      line-height: 1.25;
    }
    .card-desc {
      font-size: 17px;
      line-height: 1.5;
      color: var(--text-muted);
      margin-bottom: 18px;
    }

    .bullet-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .bullet-list li {
      position: relative;
      padding-left: 24px;
      font-size: 16.5px;
      line-height: 1.5;
      color: var(--text-main);
    }
    .bullet-list li::before {
      content: "•";
      position: absolute;
      left: 6px;
      top: -1px;
      color: var(--olive);
      font-size: 22px;
    }
    .bullet-list.ochre li::before { color: var(--ochre); }

    /* ARCHITECTURE DIAGRAM BOXES */
    .arch-diagram {
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      height: 100%;
      justify-content: space-between;
    }
    .arch-node {
      background: var(--card-alt);
      border: 1.5px solid var(--border);
      border-radius: 12px;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-weight: 600;
      font-size: 17px;
    }
    .arch-node.primary {
      background: var(--olive-light);
      border-color: var(--olive-border);
      color: var(--olive-dark);
    }
    .arch-node.warning {
      background: var(--ochre-light);
      border-color: var(--ochre-border);
      color: var(--ochre-dark);
    }
    .arch-arrow {
      text-align: center;
      font-size: 20px;
      color: var(--olive);
      line-height: 1;
    }

    /* TABLES */
    .table-container {
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }
    table.data-table th {
      background: var(--olive);
      color: #FFFFFF;
      font-family: var(--font-body);
      font-size: 16px;
      font-weight: 700;
      letter-spacing: 0.04em;
      padding: 16px 22px;
      border-bottom: 2px solid var(--olive-dark);
    }
    table.data-table td {
      padding: 16px 22px;
      font-size: 16px;
      border-bottom: 1px solid var(--border-light);
      color: var(--text-main);
      vertical-align: middle;
    }
    table.data-table tr:nth-child(even) td {
      background: var(--card-alt);
    }
    table.data-table tr:last-child td {
      border-bottom: none;
    }
    .check-yes {
      color: var(--forest);
      font-weight: 700;
      font-size: 18px;
    }
    .check-no {
      color: var(--text-subtle);
      font-size: 16px;
    }
    .badge-pill {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 700;
      font-family: var(--font-mono);
    }
    .badge-olive { background: var(--olive-light); color: var(--olive-dark); }
    .badge-ochre { background: var(--ochre-light); color: var(--ochre-dark); }

    /* CONTROLS OVERLAY */
    .deck-nav {
      position: fixed;
      bottom: 24px;
      right: 32px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(24, 25, 22, 0.85);
      backdrop-filter: blur(12px);
      padding: 8px 16px;
      border-radius: 40px;
      border: 1px solid rgba(255, 255, 255, 0.15);
      z-index: 100;
      color: #FFF;
      font-family: var(--font-mono);
      font-size: 14px;
    }
    .nav-btn {
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
    }
    .nav-btn:hover { background: rgba(255, 255, 255, 0.2); }

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
  </style>
</head>
<body>

<div class="deck-viewport">
  <div class="deck-stage" id="stage">

    <!-- =================================================================== -->
    <!-- SLIDE 1: Title -->
    <!-- =================================================================== -->
    <div class="slide active" data-slide="1">
      <div class="slide-header">
        <div class="kicker">Executive Architecture & Commercial Strategy</div>
        <h1 class="slide-title" style="font-size: 58px; margin-top: 10px;">Tiered Revenue Architecture</h1>
        <p class="slide-subtitle" style="font-size: 23px; max-width: 1400px; margin-top: 10px;">
          Designing for Durability, Governance & Compounding Revenue: Why commercial AI systems must be tiered by operational maturity rather than framework count — A case study for Alandas Tea Berlin.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-3">
          <div class="card accent-olive">
            <span class="card-tag tag-olive">Tier 1 // Essential</span>
            <h3 class="card-title">Durable Automation</h3>
            <p class="card-desc">Human-Directed Workflow Automation</p>
            <ul class="bullet-list">
              <li><strong>Core Goal:</strong> Automate tedious data gathering & outreach with zero fragility.</li>
              <li><strong>Runtime:</strong> Temporal + Python/TS + PostgreSQL + Direct APIs.</li>
              <li><strong>Autonomy:</strong> Read → Analyze → Propose → <em>Human Approves</em> → Execute.</li>
              <li><strong>Best For:</strong> Day-1 operations, lead capture, and safe founder leverage.</li>
            </ul>
          </div>

          <div class="card accent-ochre highlight">
            <span class="card-tag tag-ochre">Tier 2 // Professional</span>
            <h3 class="card-title">Governed Intelligence</h3>
            <p class="card-desc">Human-Governed Decision Intelligence</p>
            <ul class="bullet-list ochre">
              <li><strong>Core Goal:</strong> High-leverage AI reasoning bounded by strict policy rules.</li>
              <li><strong>Runtime:</strong> Temporal + Policy Engine + Decision Contracts + Audit Log.</li>
              <li><strong>Autonomy:</strong> Reason → Decision Contract → Policy Gate → Verify → Audit.</li>
              <li><strong>Best For:</strong> Scaling venues (25–70 accounts) with financial guardrails.</li>
            </ul>
          </div>

          <div class="card accent-forest">
            <span class="card-tag tag-forest">Tier 3 // Autonomous</span>
            <h3 class="card-title">Autonomous Platform</h3>
            <p class="card-desc">Policy-Governed Revenue Operations</p>
            <ul class="bullet-list">
              <li><strong>Core Goal:</strong> Closed-loop commercial machine with multi-agent orchestration.</li>
              <li><strong>Runtime:</strong> Temporal Runtime + Domain Agents + MCP + Closed-Loop Learning.</li>
              <li><strong>Autonomy:</strong> Observe → Reason → Policy Eval → Execute → Measure → Adapt.</li>
              <li><strong>Best For:</strong> Enterprise scale (100+ accounts) with automated feedback.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 01 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 2: The Core Problem -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="2">
      <div class="slide-header">
        <div class="kicker">Architectural Philosophy</div>
        <h2 class="slide-title">The Trap of "Maximum Architecture" on Day 1</h2>
        <p class="slide-subtitle">
          Treating every customer as if they require an autonomous multi-agent platform creates expensive, unmaintainable software that collapses under its own operational complexity.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-3">
          <div class="card" style="border-top: 5px solid #D9534F;">
            <span class="card-tag" style="color: #D9534F;">The Anti-Pattern</span>
            <h3 class="card-title">Technology-First Sprawl</h3>
            <p class="card-desc">Building every shiny framework because we can:</p>
            <ul class="bullet-list">
              <li>"Let's add LangGraph for all tasks!"</li>
              <li>"We need an MCP server for everything!"</li>
              <li>"Let's introduce Redis, Kafka & Vector DBs immediately!"</li>
              <li><strong>Result:</strong> 12 points of failure, massive latency, and impossible debugging when a webhook fails.</li>
            </ul>
          </div>

          <div class="card accent-ochre">
            <span class="card-tag tag-ochre">The Ground Truth</span>
            <h3 class="card-title">What Founders Actually Need</h3>
            <p class="card-desc">Real business requirements are straightforward:</p>
            <ul class="bullet-list ochre">
              <li>Lead inquiries from Instagram & Google Maps never get lost.</li>
              <li>Durable WhatsApp order parsing that never crashes or wipes state.</li>
              <li>Invoices created accurately in Dolibarr without human manual math.</li>
              <li>Timely 25-day refill prompts so cafes don't churn quietly.</li>
            </ul>
          </div>

          <div class="card accent-olive">
            <span class="card-tag tag-olive">The Solution</span>
            <h3 class="card-title">Requirement-First Tiers</h3>
            <p class="card-desc">Earn complexity through validated business scale:</p>
            <ul class="bullet-list">
              <li><strong>Tier 1:</strong> Durable automation solves 80% of manual founder friction.</li>
              <li><strong>Tier 2:</strong> Policy engines protect budget & pricing as volume grows.</li>
              <li><strong>Tier 3:</strong> Autonomous feedback loops scale revenue at maturity.</li>
              <li><strong>Rule:</strong> Never build Tier 3 until Tier 1 unit economics are proven.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 02 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 3: Why Temporal Over n8n? -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="3">
      <div class="slide-header">
        <div class="kicker">Core Runtime Decision</div>
        <h2 class="slide-title">Durability First: Why Temporal Over n8n?</h2>
        <p class="slide-subtitle">
          Visual low-code tools like n8n are great for simple prototypes, but commercial revenue pipelines require deterministic state persistence, crash resilience, and testable code.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-2">
          <div class="card" style="border-top: 5px solid #888;">
            <span class="card-tag" style="color: #666;">Low-Code Tooling // n8n Reality</span>
            <h3 class="card-title">Where n8n Breaks in Production</h3>
            <ul class="bullet-list">
              <li><strong>Transient Memory & State Loss:</strong> If an n8n node fails mid-execution (e.g., during Sidy's server crash), intermediate state is lost. There is no native event history replay.</li>
              <li><strong>No Long-Running Durability:</strong> Pausing a flow for 25 days (predictive refill cycle) relies on fragile cron triggers or polling database records rather than native durable timers.</li>
              <li><strong>Lack of Code Versioning & CI/CD:</strong> Drag-and-drop JSON workflows cannot be unit-tested, mocked, or linted with standard software engineering practices.</li>
              <li><strong>No Deterministic Replay:</strong> Cannot reconstruct the exact history of an order or audit an AI agent's decision tree when something goes wrong.</li>
            </ul>
          </div>

          <div class="card accent-olive">
            <span class="card-tag tag-olive">Engineering Foundation // Temporal Advantage</span>
            <h3 class="card-title">Why Temporal Guarantees Revenue Continuity</h3>
            <ul class="bullet-list">
              <li><strong>True Durable Execution:</strong> Workflows are written as pure Python/TypeScript code. Every state transition is appended to an immutable event log. Workers can crash, reboot, or migrate, and resume at the exact line of code.</li>
              <li><strong>Built-In Idempotency & Retries:</strong> Activities (calling Meta API, sending WhatsApp messages, generating Dolibarr invoices) have automatic exponential backoff with idempotency tokens.</li>
              <li><strong>Native Long-Running Workflows:</strong> `workflow.sleep(25 * days)` is a native, durable construct that consumes zero compute while sleeping.</li>
              <li><strong>Separation of State & Logic:</strong> Temporal manages the execution history, while PostgreSQL stores business entities (clients, invoices, inventory).</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 03 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 4: The Golden Rule -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="4">
      <div class="slide-header">
        <div class="kicker">Governing Engineering Law</div>
        <h2 class="slide-title">"Complexity Must Be Purchased by a Requirement"</h2>
        <p class="slide-subtitle">
          Every framework, agent boundary, and distributed bus introduces new failure modes. We follow a strict decision tree before writing a single line of complex code.
        </p>
      </div>

      <div class="slide-body">
        <div class="card" style="padding: 40px; margin-bottom: 24px;">
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 16px;">
            <div style="flex: 1; background: var(--olive-light); padding: 20px; border-radius: 12px; text-align: center; border: 1.5px solid var(--olive-border);">
              <div style="font-family: var(--font-mono); font-size: 13px; color: var(--olive); font-weight: 700;">STEP 01</div>
              <div style="font-family: var(--font-display); font-size: 20px; font-weight: 700; margin-top: 4px;">Business Need</div>
              <div style="font-size: 14px; color: var(--text-muted); margin-top: 4px;">"Capture cafe leads from Instagram"</div>
            </div>
            <div style="font-size: 24px; color: var(--olive);">➔</div>
            <div style="flex: 1; background: var(--card-alt); padding: 20px; border-radius: 12px; text-align: center; border: 1.5px solid var(--border);">
              <div style="font-family: var(--font-mono); font-size: 13px; color: var(--text-muted); font-weight: 700;">STEP 02</div>
              <div style="font-family: var(--font-display); font-size: 20px; font-weight: 700; margin-top: 4px;">Required Capability</div>
              <div style="font-size: 14px; color: var(--text-muted); margin-top: 4px;">"Comment keyword trigger to DM"</div>
            </div>
            <div style="font-size: 24px; color: var(--olive);">➔</div>
            <div style="flex: 1; background: var(--card-alt); padding: 20px; border-radius: 12px; text-align: center; border: 1.5px solid var(--border);">
              <div style="font-family: var(--font-mono); font-size: 13px; color: var(--text-muted); font-weight: 700;">STEP 03</div>
              <div style="font-family: var(--font-display); font-size: 20px; font-weight: 700; margin-top: 4px;">Required Robustness</div>
              <div style="font-size: 14px; color: var(--text-muted); margin-top: 4px;">"100% webhook receipt & CRM sync"</div>
            </div>
            <div style="font-size: 24px; color: var(--olive);">➔</div>
            <div style="flex: 1; background: var(--ochre-light); padding: 20px; border-radius: 12px; text-align: center; border: 1.5px solid var(--ochre-border);">
              <div style="font-family: var(--font-mono); font-size: 13px; color: var(--ochre); font-weight: 700;">STEP 04</div>
              <div style="font-family: var(--font-display); font-size: 20px; font-weight: 700; margin-top: 4px;">Architecture Tier</div>
              <div style="font-size: 14px; color: var(--ochre-dark); font-weight: 700; margin-top: 4px;">Tier 1: Essential Automation</div>
            </div>
            <div style="font-size: 24px; color: var(--olive);">➔</div>
            <div style="flex: 1; background: #FFFFFF; padding: 20px; border-radius: 12px; text-align: center; border: 2px solid var(--olive);">
              <div style="font-family: var(--font-mono); font-size: 13px; color: var(--olive); font-weight: 700;">STEP 05</div>
              <div style="font-family: var(--font-display); font-size: 20px; font-weight: 700; margin-top: 4px;">Clean Code</div>
              <div style="font-size: 14px; color: var(--text-muted); margin-top: 4px;">Temporal Workflow + OpenReply</div>
            </div>
          </div>
        </div>

        <div class="grid-3">
          <div class="card">
            <span class="card-tag tag-olive">Principle A</span>
            <h4 class="card-title" style="font-size: 20px;">Zero Framework Tourism</h4>
            <p class="card-desc" style="font-size: 15px;">Do not add LangGraph, MCP, or Redis simply because they exist in AI news. Only add them when a concrete bottleneck demands them.</p>
          </div>
          <div class="card">
            <span class="card-tag tag-ochre">Principle B</span>
            <h4 class="card-title" style="font-size: 20px;">Protect the Domain Core</h4>
            <p class="card-desc" style="font-size: 15px;">Dolibarr CRM, PostgreSQL, and business accounting remain the immutable source of truth. AI operates outside as an assistant, never as unconstrained master.</p>
          </div>
          <div class="card">
            <span class="card-tag tag-forest">Principle C</span>
            <h4 class="card-title" style="font-size: 20px;">Non-Destructive Upgrades</h4>
            <p class="card-desc" style="font-size: 15px;">Tier 1 code is never discarded when upgrading to Tier 2. Each tier sits cleanly on top of the prior layer's data contracts and workflows.</p>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 04 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 5: Commercial Packaging -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="5">
      <div class="slide-header">
        <div class="kicker">Commercial Strategy & Positioning</div>
        <h2 class="slide-title">Selling Business Capability, Never Tech Stacks</h2>
        <p class="slide-subtitle">
          Clients do not care if a system uses LangGraph or Temporal. They pay for capability, reliability, autonomy, scale, and risk controls. We package the architecture accordingly.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-3">
          <div class="card accent-olive">
            <div style="font-family: var(--font-mono); font-size: 13px; color: var(--text-subtle);">DO NOT SELL: "Temporal + Postgres + Python"</div>
            <div style="font-size: 16px; font-weight: 700; color: var(--olive); margin: 6px 0 12px 0;">SELL INSTEAD:</div>
            <h3 class="card-title" style="font-size: 28px;">Lead Generation & Follow-Up System</h3>
            <p class="card-desc"><strong>Human-Directed Automation.</strong> The system does the repetitive heavy lifting; the founder retains complete conversational and financial control.</p>
            <div style="background: var(--card-alt); padding: 14px; border-radius: 8px; font-size: 14px; line-height: 1.45;">
              <strong>Customer Value:</strong> Saves 15+ hours/week. Scrapes cafes, enriches profiles, drafts outreach, and syncs orders into Dolibarr CRM without hallucination risk.
            </div>
          </div>

          <div class="card accent-ochre highlight">
            <div style="font-family: var(--font-mono); font-size: 13px; color: var(--text-subtle);">DO NOT SELL: "Policy Engines + Observability"</div>
            <div style="font-size: 16px; font-weight: 700; color: var(--ochre); margin: 6px 0 12px 0;">SELL INSTEAD:</div>
            <h3 class="card-title" style="font-size: 28px;">AI Revenue Intelligence System</h3>
            <p class="card-desc"><strong>Human-Governed Intelligence.</strong> The system actively reasons, monitors ad performance, calculates refill schedules, and requests 1-tap approvals.</p>
            <div style="background: var(--card-alt); padding: 14px; border-radius: 8px; font-size: 14px; line-height: 1.45;">
              <strong>Customer Value:</strong> Prevents cafe churn with automated Day-25 reorder prompts. Automatically optimizes ad budgets within strict policy limits.
            </div>
          </div>

          <div class="card accent-forest">
            <div style="font-family: var(--font-mono); font-size: 13px; color: var(--text-subtle);">DO NOT SELL: "Multi-Agent MCP Event Architecture"</div>
            <div style="font-size: 16px; font-weight: 700; color: var(--forest); margin: 6px 0 12px 0;">SELL INSTEAD:</div>
            <h3 class="card-title" style="font-size: 28px;">AI Revenue Operations Platform</h3>
            <p class="card-desc"><strong>Policy-Governed Autonomy.</strong> Closed-loop commercial machine where live customer reorder data automatically trains marketing experiments.</p>
            <div style="background: var(--card-alt); padding: 14px; border-radius: 8px; font-size: 14px; line-height: 1.45;">
              <strong>Customer Value:</strong> Full autopilot commercial machine. Scales Alandas to 100+ hospitality accounts across Germany with zero linear headcount growth.
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 05 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 6: Tier 1 Architecture -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="6">
      <div class="slide-header">
        <div class="kicker">Tier 1 // Technical Architecture</div>
        <h2 class="slide-title">Essential Revenue Automation Blueprint</h2>
        <p class="slide-subtitle">
          A clean, durable, production-grade foundation. Zero LangGraph, zero MCP, zero Redis, zero multi-agent debate. Pure engineering reliability.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-2">
          <!-- Left: Visual Blueprint -->
          <div class="arch-diagram">
            <div class="arch-node primary">
              <span>TEMPORAL WORKFLOW ENGINE</span>
              <span class="badge-pill badge-olive">Durable Runtime</span>
            </div>
            <div class="arch-arrow">▼</div>
            <div class="arch-node">
              <span>APPLICATION LOGIC (Python / TypeScript)</span>
              <span class="badge-pill">Deterministic Core</span>
            </div>
            <div class="arch-arrow">▼</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
              <div class="arch-node" style="justify-content: center; text-align: center;">
                <span>Deterministic Rules<br><small style="color:var(--text-muted);">Pricing, VAT, Scoring</small></span>
              </div>
              <div class="arch-node" style="justify-content: center; text-align: center;">
                <span>LLM Reasoning API<br><small style="color:var(--text-muted);">Research, Drafting</small></span>
              </div>
            </div>
            <div class="arch-arrow">▼</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
              <div class="arch-node warning" style="font-size: 14px; justify-content: center;">Meta & Instagram</div>
              <div class="arch-node warning" style="font-size: 14px; justify-content: center;">Dolibarr CRM</div>
              <div class="arch-node warning" style="font-size: 14px; justify-content: center;">Shopify Store</div>
            </div>
            <div class="arch-arrow">▼</div>
            <div class="arch-node primary">
              <span>POSTGRESQL DATABASE</span>
              <span class="badge-pill badge-olive">Single System of Record</span>
            </div>
          </div>

          <!-- Right: Capabilities & Boundary -->
          <div class="card accent-olive">
            <span class="card-tag tag-olive">System Boundaries & Deliverables</span>
            <h3 class="card-title">What Tier 1 Actually Delivers</h3>
            <ul class="bullet-list">
              <li><strong>Prospect Discovery & Waterfall:</strong> Scrapes cafes from Google Maps & Instagram, enriches contact details, verifies business email/WhatsApp.</li>
              <li><strong>ICP Lead Scoring:</strong> Evaluates seating capacity (>30 seats), culinary aesthetic, and tea presence mathematically.</li>
              <li><strong>Dolibarr CRM Sync:</strong> Automatically creates third-party accounts and prospect cards in Sidy's open-source Dolibarr instance.</li>
              <li><strong>WhatsApp Order Parsing:</strong> OCR parses paper order photos and voice notes into line items, queuing draft PDF invoices for Sidy's confirmation.</li>
              <li><strong>Human Safety Gate:</strong> The AI proposes outreach drafts; Sidy taps "Approve" before any external message is dispatched.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 06 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 7: Tier 1 Deep Dive -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="7">
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 2340" width="1000" height="2340">

  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&amp;family=JetBrains+Mono:wght@500;700&amp;family=Plus+Jakarta+Sans:wght@500;600;700&amp;display=swap');
      text { font-family: 'Caveat', cursive, sans-serif; }
    </style>
    <filter id="handDrawn" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.2" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF" />

  <text x="480.0" y="53" fill="#181916" font-size="23" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="middle">
    <tspan x="480.0" dy="0">Tier 1: Essential Revenue Automation — Human-Directed Architecture</tspan>
  </text>
  <text x="480.0" y="79" fill="#5C5950" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Cyril Uzochukwu | AI Automation Engineer | Alandas Tea Berlin</tspan>
  </text>
  <ellipse cx="480.0" cy="137.5" rx="120.0" ry="27.5" fill="#FEE2E2" stroke="#F87171" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="140" fill="#991B1B" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Raw Lead Trigger</tspan>
    <tspan x="480.0" dy="18">(Google Maps / Instagram)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="165" x2="480" y2="205" stroke="#181916" stroke-width="2" />
    <polygon points="480,205 473.5,193.7416697508023 486.5,193.7416697508023" fill="#181916" />
  </g>
  <rect x="345" y="205" width="270" height="55" rx="12" fill="#E0F2FE" stroke="#38BDF8" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="234" fill="#0369A1" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Extract &amp; Normalize Venue Data</tspan>
    <tspan x="480.0" dy="17">(Website, IG handle, Address)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="260" x2="480" y2="295" stroke="#181916" stroke-width="2" />
    <polygon points="480,295 473.5,283.7416697508023 486.5,283.7416697508023" fill="#181916" />
  </g>
  <rect x="345" y="295" width="270" height="55" rx="12" fill="#E0F2FE" stroke="#38BDF8" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="324" fill="#0369A1" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Idempotency &amp; Dolibarr Check</tspan>
    <tspan x="480.0" dy="17">(Existing Customer / Active Lead?)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="350" x2="480" y2="385" stroke="#181916" stroke-width="2" />
    <polygon points="480,385 473.5,373.7416697508023 486.5,373.7416697508023" fill="#181916" />
  </g>
  <rect x="330" y="385" width="300" height="55" rx="12" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="414" fill="#C2410C" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Budget &amp; Rate Limit Check</tspan>
    <tspan x="480.0" dy="17">(Max €15/day scraping spend)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="630" y1="412" x2="725" y2="412" stroke="#EF4444" stroke-width="2" />
    <polygon points="725,412 713.7416697508023,418.5 713.7416697508023,405.5" fill="#EF4444" />
  </g>
  <text x="677.5" y="406.0" fill="#DC2626" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="677.5" dy="0">TRIP</tspan>
  </text>
  <rect x="725" y="387" width="160" height="50" rx="12" fill="#FEE2E2" stroke="#F87171" stroke-width="2" filter="url(#handDrawn)" />
  <text x="805.0" y="414" fill="#991B1B" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="805.0" dy="0">Alert Cyril Stop</tspan>
    <tspan x="805.0" dy="17">(Circuit Open)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="440" x2="480" y2="480" stroke="#15803D" stroke-width="2" />
    <polygon points="480,480 473.5,468.7416697508023 486.5,468.7416697508023" fill="#15803D" />
  </g>
  <text x="523.0" y="462.0" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">OK</tspan>
  </text>
  <rect x="320" y="480" width="320" height="60" rx="12" fill="#DCFCE7" stroke="#4ADE80" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="506" fill="#166534" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Stage 0: Free § 5 TMG Scraper</tspan>
    <tspan x="480.0" dy="18">(Scrape /impressum, /kontakt, /legal)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="540" x2="480" y2="575" stroke="#181916" stroke-width="2" />
    <polygon points="480,575 473.5,563.7416697508023 486.5,563.7416697508023" fill="#181916" />
  </g>
  <polygon points="480.0,575 560,630.0 480.0,685 400,630.0" fill="#FEF08A" stroke="#EAB308" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="624" fill="#854D0E" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Owner Email</tspan>
    <tspan x="480.0" dy="17">Found in</tspan>
    <tspan x="480.0" dy="17">Impressum?</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="560" y1="630" x2="655" y2="630" stroke="#15803D" stroke-width="2" />
    <polygon points="655,630 643.7416697508023,636.5 643.7416697508023,623.5" fill="#15803D" />
  </g>
  <text x="607.5" y="624.0" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="607.5" dy="0">YES (48%)</tspan>
  </text>
  <rect x="655" y="600" width="175" height="60" rx="12" fill="#DCFCE7" stroke="#4ADE80" stroke-width="2" filter="url(#handDrawn)" />
  <text x="742.5" y="623" fill="#166534" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="742.5" dy="0">FREE (§ 5 TMG Success)</tspan>
    <tspan x="742.5" dy="15">Skip Bulk Paid APIs!</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="685" x2="480" y2="730" stroke="#181916" stroke-width="2" />
    <polygon points="480,730 473.5,718.7416697508023 486.5,718.7416697508023" fill="#181916" />
  </g>
  <text x="523.0" y="709.5" fill="#5C5950" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">NO (52%)</tspan>
  </text>
  <rect x="345" y="730" width="270" height="55" rx="12" fill="#E0F2FE" stroke="#38BDF8" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="757" fill="#0369A1" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Stage 1: GitLeads / Apollo Bulk DB</tspan>
    <tspan x="480.0" dy="17">(Low-Cost Query: €0.005 / check)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="785" x2="480" y2="820" stroke="#181916" stroke-width="2" />
    <polygon points="480,820 473.5,808.7416697508023 486.5,808.7416697508023" fill="#181916" />
  </g>
  <polygon points="480.0,820 560,875.0 480.0,930 400,875.0" fill="#FEF08A" stroke="#EAB308" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="869" fill="#854D0E" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Email</tspan>
    <tspan x="480.0" dy="17">Resolved in</tspan>
    <tspan x="480.0" dy="17">Bulk DB?</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="560" y1="875" x2="655" y2="875" stroke="#15803D" stroke-width="2" />
    <polygon points="655,875 643.7416697508023,881.5 643.7416697508023,868.5" fill="#15803D" />
  </g>
  <text x="607.5" y="869.0" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="607.5" dy="0">YES (+24%)</tspan>
  </text>
  <rect x="655" y="850" width="160" height="50" rx="12" fill="#E0F2FE" stroke="#38BDF8" stroke-width="2" filter="url(#handDrawn)" />
  <text x="735.0" y="874" fill="#0369A1" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="735.0" dy="0">Pass to Validation Gate</tspan>
    <tspan x="735.0" dy="15">(€0.005 Cost)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="930" x2="480" y2="975" stroke="#181916" stroke-width="2" />
    <polygon points="480,975 473.5,963.7416697508023 486.5,963.7416697508023" fill="#181916" />
  </g>
  <text x="523.0" y="954.5" fill="#5C5950" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">NO (28%)</tspan>
  </text>
  <rect x="345" y="975" width="270" height="55" rx="12" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="1002" fill="#C2410C" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Stage 2: Origami / Prospeo Scraper</tspan>
    <tspan x="480.0" dy="17">(Name Permutation + MX: €0.02)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1030" x2="480" y2="1065" stroke="#181916" stroke-width="2" />
    <polygon points="480,1065 473.5,1053.7416697508022 486.5,1053.7416697508022" fill="#181916" />
  </g>
  <polygon points="480.0,1065 570,1125.0 480.0,1185 390,1125.0" fill="#FEF08A" stroke="#EAB308" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="1115" fill="#854D0E" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">MillionVerifier</tspan>
    <tspan x="480.0" dy="18">Deliverability</tspan>
    <tspan x="480.0" dy="18">Result?</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="570" y1="1125" x2="665" y2="1125" stroke="#EF4444" stroke-width="2" />
    <polygon points="665,1125 653.7416697508023,1131.5 653.7416697508023,1118.5" fill="#EF4444" />
  </g>
  <text x="617.5" y="1119.0" fill="#DC2626" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="617.5" dy="0">INVALID</tspan>
  </text>
  <rect x="665" y="1095" width="175" height="60" rx="12" fill="#FEE2E2" stroke="#F87171" stroke-width="2" filter="url(#handDrawn)" />
  <text x="752.5" y="1119" fill="#991B1B" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="752.5" dy="0">Discard Email</tspan>
    <tspan x="752.5" dy="15">(Protect Bounce Rate &lt;1.5%)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="390" y1="1125" x2="295" y2="1125" stroke="#F59E0B" stroke-width="2" />
    <polygon points="295,1125 306.2583302491977,1118.5 306.2583302491977,1131.5" fill="#F59E0B" />
  </g>
  <text x="342.5" y="1119.0" fill="#D97706" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="342.5" dy="0">RISKY</tspan>
  </text>
  <rect x="120" y="1095" width="175" height="60" rx="12" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2" filter="url(#handDrawn)" />
  <text x="207.5" y="1119" fill="#C2410C" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="207.5" dy="0">Route to WhatsApp / Alt</tspan>
    <tspan x="207.5" dy="15">(Do not send cold email)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1185" x2="480" y2="1230" stroke="#15803D" stroke-width="2" />
    <polygon points="480,1230 473.5,1218.7416697508022 486.5,1218.7416697508022" fill="#15803D" />
  </g>
  <text x="523.0" y="1209.5" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">VALID</tspan>
  </text>
  <rect x="345" y="1230" width="270" height="55" rx="12" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="1257" fill="#C2410C" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Stage 3: LeadMagic Mobile Discovery</tspan>
    <tspan x="480.0" dy="17">(Find Direct WhatsApp Phone)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1285" x2="480" y2="1325" stroke="#181916" stroke-width="2" />
    <polygon points="480,1325 473.5,1313.7416697508022 486.5,1313.7416697508022" fill="#181916" />
  </g>
  <rect x="260" y="1325" width="440" height="125" rx="12" fill="#F3E8FF" stroke="#C084FC" stroke-width="2" filter="url(#handDrawn)" />
  <text x="275" y="1350" fill="#7E22CE" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="275" dy="0">Agent 1 — ICP Qualification Agent (Gemini Flash)</tspan>
  </text>
  <rect x="285" y="1370" width="180" height="55" rx="12" fill="#FFFFFF" stroke="#A855F7" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="375.0" y="1396" fill="#6B21A8" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="375.0" dy="0">Analyze Menu &amp;</tspan>
    <tspan x="375.0" dy="15">Seating (&gt;30 seats)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="465" y1="1397" x2="495" y2="1397" stroke="#A855F7" stroke-width="2" />
    <polygon points="495,1397 483.7416697508023,1403.5 483.7416697508023,1390.5" fill="#A855F7" />
  </g>
  <rect x="495" y="1370" width="180" height="55" rx="12" fill="#FFFFFF" stroke="#A855F7" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="585.0" y="1396" fill="#6B21A8" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="585.0" dy="0">Calculate ICP Score</tspan>
    <tspan x="585.0" dy="15">&amp; Concept Fit</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1450" x2="480" y2="1485" stroke="#181916" stroke-width="2" />
    <polygon points="480,1485 473.5,1473.7416697508022 486.5,1473.7416697508022" fill="#181916" />
  </g>
  <polygon points="480.0,1485 560,1540.0 480.0,1595 400,1540.0" fill="#FEF08A" stroke="#EAB308" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="1534" fill="#854D0E" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">ICP Score</tspan>
    <tspan x="480.0" dy="17">&gt;= 70?</tspan>
    <tspan x="480.0" dy="17">(High Fit)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="400" y1="1540" x2="305" y2="1540" stroke="#F59E0B" stroke-width="2" />
    <polygon points="305,1540 316.2583302491977,1533.5 316.2583302491977,1546.5" fill="#F59E0B" />
  </g>
  <text x="352.5" y="1534.0" fill="#D97706" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="352.5" dy="0">NO</tspan>
  </text>
  <rect x="130" y="1515" width="175" height="50" rx="12" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2" filter="url(#handDrawn)" />
  <text x="217.5" y="1539" fill="#C2410C" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="217.5" dy="0">Archive to Low-Priority</tspan>
    <tspan x="217.5" dy="15">(Nurture List)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1595" x2="480" y2="1640" stroke="#15803D" stroke-width="2" />
    <polygon points="480,1640 473.5,1628.7416697508022 486.5,1628.7416697508022" fill="#15803D" />
  </g>
  <text x="523.0" y="1619.5" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">YES</tspan>
  </text>
  <rect x="210" y="1640" width="540" height="125" rx="12" fill="#DCFCE7" stroke="#4ADE80" stroke-width="2" filter="url(#handDrawn)" />
  <text x="225" y="1665" fill="#166534" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="225" dy="0">Agent 2 — Pitch Personalization Engine (Claude 3.5 Sonnet)</tspan>
  </text>
  <rect x="240" y="1685" width="150" height="55" rx="12" fill="#FFFFFF" stroke="#22C55E" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="315.0" y="1710.5" fill="#15803D" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="315.0" dy="0">Extract Cafe Aesthetic</tspan>
    <tspan x="315.0" dy="15">&amp; Signature Blends</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="390" y1="1712" x2="415" y2="1712" stroke="#22C55E" stroke-width="2" />
    <polygon points="415,1712 403.7416697508023,1718.5 403.7416697508023,1705.5" fill="#22C55E" />
  </g>
  <rect x="415" y="1685" width="150" height="55" rx="12" fill="#FFFFFF" stroke="#22C55E" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="490.0" y="1710.5" fill="#15803D" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="490.0" dy="0">Draft €19 Discovery Box</tspan>
    <tspan x="490.0" dy="15">Personalized Pitch</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="565" y1="1712" x2="590" y2="1712" stroke="#22C55E" stroke-width="2" />
    <polygon points="590,1712 578.7416697508023,1718.5 578.7416697508023,1705.5" fill="#22C55E" />
  </g>
  <rect x="590" y="1685" width="150" height="55" rx="12" fill="#FFFFFF" stroke="#22C55E" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="665.0" y="1710.5" fill="#15803D" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="665.0" dy="0">Queue Draft in Sidy's</tspan>
    <tspan x="665.0" dy="15">WhatsApp Inbox</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1765" x2="480" y2="1800" stroke="#181916" stroke-width="2" />
    <polygon points="480,1800 473.5,1788.7416697508022 486.5,1788.7416697508022" fill="#181916" />
  </g>
  <polygon points="480.0,1800 570,1855.0 480.0,1910 390,1855.0" fill="#FEF08A" stroke="#EAB308" stroke-width="3" filter="url(#handDrawn)" />
  <text x="480.0" y="1849.5" fill="#854D0E" font-size="13.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Sidy Approves</tspan>
    <tspan x="480.0" dy="17">on WhatsApp?</tspan>
    <tspan x="480.0" dy="17">(Human Gate)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="570" y1="1855" x2="665" y2="1855" stroke="#EF4444" stroke-width="2" />
    <polygon points="665,1855 653.7416697508023,1861.5 653.7416697508023,1848.5" fill="#EF4444" />
  </g>
  <text x="617.5" y="1849.0" fill="#DC2626" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="617.5" dy="0">REJECT</tspan>
  </text>
  <rect x="665" y="1830" width="160" height="50" rx="12" fill="#FEE2E2" stroke="#F87171" stroke-width="2" filter="url(#handDrawn)" />
  <text x="745.0" y="1854" fill="#991B1B" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="745.0" dy="0">Discard / Edit Draft</tspan>
    <tspan x="745.0" dy="15">(Zero Brand Risk)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1910" x2="480" y2="1955" stroke="#15803D" stroke-width="2" />
    <polygon points="480,1955 473.5,1943.7416697508022 486.5,1943.7416697508022" fill="#15803D" />
  </g>
  <text x="523.0" y="1934.5" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">1-TAP APPROVE</tspan>
  </text>
  <rect x="310" y="1955" width="340" height="65" rx="12" fill="#E0F2FE" stroke="#38BDF8" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="1982" fill="#0369A1" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Temporal Execution Activity</tspan>
    <tspan x="480.0" dy="17">(Send WhatsApp Outreach + Create Dolibarr Lead)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="2020" x2="480" y2="2055" stroke="#181916" stroke-width="2" />
    <polygon points="480,2055 473.5,2043.7416697508022 486.5,2043.7416697508022" fill="#181916" />
  </g>
  <rect x="310" y="2055" width="340" height="65" rx="12" fill="#DCFCE7" stroke="#4ADE80" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="2082.5" fill="#166534" font-size="13.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Log Entity to Dolibarr CRM &amp;</tspan>
    <tspan x="480.0" dy="17">PostgreSQL Audit Ledger</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="2120" x2="480" y2="2155" stroke="#181916" stroke-width="2" />
    <polygon points="480,2155 473.5,2143.7416697508024 486.5,2143.7416697508024" fill="#181916" />
  </g>
  <rect x="320" y="2155" width="320" height="60" rx="12" fill="#DCFCE7" stroke="#22C55E" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="2180.5" fill="#15803D" font-size="13.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Durable Temporal Timer</tspan>
    <tspan x="480.0" dy="17">(Day-4 Tasting Check-In &amp; Day-25 Refill)</tspan>
  </text>
</svg>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 07 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 8: Waterfall Enrichment Engine -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="8">
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1320 740" width="1320" height="740">

  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&amp;family=JetBrains+Mono:wght@500;700&amp;family=Plus+Jakarta+Sans:wght@500;600;700&amp;display=swap');
      text { font-family: 'Caveat', cursive, sans-serif; }
    </style>
    <filter id="handDrawn" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.2" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF" />

  <rect x="80" y="50" width="1140" height="110" rx="12" fill="#F9F7F2" stroke="#444C32" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="650.0" y="96" fill="#181916" font-size="28" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="middle">
    <tspan x="650.0" dy="0">WATERFALL ENRICHMENT: CHEAPEST TOOL FIRST</tspan>
  </text>
  <text x="650.0" y="130" fill="#C48737" font-size="18" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="middle">
    <tspan x="650.0" dy="0">Each tool only gets what the last one missed  •  87% Data Acquisition Cost Reduction</tspan>
  </text>
  <rect x="80" y="200" width="260" height="160" rx="12" fill="#EEF2E8" stroke="#2E3422" stroke-width="2" filter="url(#handDrawn)" />
  <text x="95" y="228" fill="#444C32" font-size="13" font-family="JetBrains Mono, monospace" font-weight="600" text-anchor="start">
    <tspan x="95" dy="0">STEP 0 // INGESTION</tspan>
  </text>
  <text x="95" y="261" fill="#181916" font-size="21" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="start">
    <tspan x="95" dy="0">1,000 Raw Leads</tspan>
  </text>
  <text x="95" y="289" fill="#5C5950" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="95" dy="0">Google Maps Cafes &amp;</tspan>
    <tspan x="95" dy="18">Instagram Engagers</tspan>
    <tspan x="95" dy="18">Across Germany</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="340" y1="280" x2="390" y2="280" stroke="#444C32" stroke-width="2" />
    <polygon points="390,280 378.7416697508023,286.5 378.7416697508023,273.5" fill="#444C32" />
  </g>
  <rect x="390" y="200" width="260" height="160" rx="12" fill="#EDF5EF" stroke="#2F5339" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="405" y="228" fill="#2F5339" font-size="13" font-family="JetBrains Mono, monospace" font-weight="600" text-anchor="start">
    <tspan x="405" dy="0">STAGE 0 // €0.00 (FREE)</tspan>
  </text>
  <text x="405" y="260" fill="#181916" font-size="20" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="start">
    <tspan x="405" dy="0">§ 5 TMG Impressum</tspan>
  </text>
  <text x="405" y="286" fill="#181916" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="405" dy="0">Scrapes legal notice.</tspan>
    <tspan x="405" dy="18">480 emails found.</tspan>
    <tspan x="405" dy="18">520 pass down ➔</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="650" y1="280" x2="700" y2="280" stroke="#444C32" stroke-width="2" />
    <polygon points="700,280 688.7416697508023,286.5 688.7416697508023,273.5" fill="#444C32" />
  </g>
  <rect x="700" y="200" width="260" height="160" rx="12" fill="#FFFFFF" stroke="#444C32" stroke-width="2" filter="url(#handDrawn)" />
  <text x="715" y="228" fill="#444C32" font-size="13" font-family="JetBrains Mono, monospace" font-weight="600" text-anchor="start">
    <tspan x="715" dy="0">STAGE 1 // €0.005 / QUERY</tspan>
  </text>
  <text x="715" y="260" fill="#181916" font-size="20" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="start">
    <tspan x="715" dy="0">GitLeads / Apollo</tspan>
  </text>
  <text x="715" y="286" fill="#5C5950" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="715" dy="0">Bulk database check.</tspan>
    <tspan x="715" dy="18">240 more found.</tspan>
    <tspan x="715" dy="18">280 pass down ➔</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="960" y1="280" x2="1010" y2="280" stroke="#444C32" stroke-width="2" />
    <polygon points="1010,280 998.7416697508023,286.5 998.7416697508023,273.5" fill="#444C32" />
  </g>
  <rect x="1010" y="200" width="260" height="160" rx="12" fill="#FCF4E8" stroke="#C48737" stroke-width="2" filter="url(#handDrawn)" />
  <text x="1025" y="228" fill="#C48737" font-size="13" font-family="JetBrains Mono, monospace" font-weight="600" text-anchor="start">
    <tspan x="1025" dy="0">STAGE 2 // €0.02 / QUERY</tspan>
  </text>
  <text x="1025" y="260" fill="#181916" font-size="20" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="start">
    <tspan x="1025" dy="0">Origami / Prospeo</tspan>
  </text>
  <text x="1025" y="286" fill="#9A6622" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="1025" dy="0">Deep social &amp; MX scrape.</tspan>
    <tspan x="1025" dy="18">180 more found.</tspan>
    <tspan x="1025" dy="18">~90% find rate total!</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="1140" y1="360" x2="1140" y2="420" stroke="#2F5339" stroke-width="2.5" />
    <polygon points="1140,420 1133.5,408.7416697508023 1146.5,408.7416697508023" fill="#2F5339" />
  </g>
  <rect x="1010" y="420" width="260" height="160" rx="12" fill="#EDF5EF" stroke="#2F5339" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="1025" y="448" fill="#2F5339" font-size="13" font-family="JetBrains Mono, monospace" font-weight="600" text-anchor="start">
    <tspan x="1025" dy="0">VALIDATE // €0.002 / CHECK</tspan>
  </text>
  <text x="1025" y="480" fill="#181916" font-size="20" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="start">
    <tspan x="1025" dy="0">MillionVerifier</tspan>
  </text>
  <text x="1025" y="506" fill="#2F5339" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="1025" dy="0">Valid, risky, catch-all.</tspan>
    <tspan x="1025" dy="18">Discard bad records.</tspan>
    <tspan x="1025" dy="18">&lt;1.5% bounce rate guaranteed!</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="1010" y1="500" x2="960" y2="500" stroke="#C48737" stroke-width="2" />
    <polygon points="960,500 971.2583302491977,493.5 971.2583302491977,506.5" fill="#C48737" />
  </g>
  <rect x="700" y="420" width="260" height="160" rx="12" fill="#FCF4E8" stroke="#C48737" stroke-width="2" filter="url(#handDrawn)" />
  <text x="715" y="448" fill="#C48737" font-size="13" font-family="JetBrains Mono, monospace" font-weight="600" text-anchor="start">
    <tspan x="715" dy="0">STAGE 3 // BONUS MOBILE</tspan>
  </text>
  <text x="715" y="480" fill="#181916" font-size="20" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="start">
    <tspan x="715" dy="0">LeadMagic Mobile</tspan>
  </text>
  <text x="715" y="506" fill="#9A6622" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="715" dy="0">Mobile lookup on top.</tspan>
    <tspan x="715" dy="18">650 WhatsApp numbers.</tspan>
    <tspan x="715" dy="18">Enables direct B2B chats!</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="700" y1="500" x2="650" y2="500" stroke="#444C32" stroke-width="2.5" />
    <polygon points="650,500 661.2583302491977,493.5 661.2583302491977,506.5" fill="#444C32" />
  </g>
  <rect x="390" y="420" width="260" height="160" rx="12" fill="#EEF2E8" stroke="#444C32" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="405" y="448" fill="#444C32" font-size="13" font-family="JetBrains Mono, monospace" font-weight="600" text-anchor="start">
    <tspan x="405" dy="0">DESTINATION // DOLIBARR</tspan>
  </text>
  <text x="405" y="480" fill="#181916" font-size="20" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="start">
    <tspan x="405" dy="0">Dolibarr CRM Lead</tspan>
  </text>
  <text x="405" y="506" fill="#444C32" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="405" dy="0">Clean, verified entity.</tspan>
    <tspan x="405" dy="18">WhatsApp draft queued.</tspan>
    <tspan x="405" dy="18">Sidy approves with 1 tap.</tspan>
  </text>
  <rect x="80" y="420" width="260" height="160" rx="12" fill="#FFFFFF" stroke="#181916" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="95" y="449" fill="#181916" font-size="14" font-family="JetBrains Mono, monospace" font-weight="600" text-anchor="start">
    <tspan x="95" dy="0">UNIT ECONOMICS</tspan>
  </text>
  <text x="95" y="482" fill="#2F5339" font-size="22" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="start">
    <tspan x="95" dy="0">87% Savings</tspan>
  </text>
  <text x="95" y="509" fill="#5C5950" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="95" dy="0">Flat Scrape: €80 / 1k</tspan>
    <tspan x="95" dy="18">Waterfall: €10 / 1k</tspan>
    <tspan x="95" dy="18">Net Save: €70 per 1k leads!</tspan>
  </text>
  <rect x="80" y="620" width="1190" height="85" rx="12" fill="#F9F7F2" stroke="#444C32" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="100" y="645" fill="#444C32" font-size="13" font-family="JetBrains Mono, monospace" font-weight="600" text-anchor="start">
    <tspan x="100" dy="0">TEMPORAL DURABILITY GUARANTEE</tspan>
  </text>
  <text x="100" y="669" fill="#181916" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="100" dy="0">Each waterfall stage is an isolated Temporal Activity with automatic exponential backoff. If Apollo or Prospeo times out,</tspan>
    <tspan x="100" dy="18">the workflow catches the exception and falls back to the next provider gracefully — zero dropped leads or corrupted records.</tspan>
  </text>
</svg>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 08 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 9: Tier 2 Architecture -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="9">
      <div class="slide-header">
        <div class="kicker">Tier 2 // Technical Architecture</div>
        <h2 class="slide-title">Professional Revenue Intelligence Blueprint</h2>
        <p class="slide-subtitle">
          Introducing durable domain workflows, structured Policy Engines, Decision Contracts, post-action verification, and comprehensive audit logs.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-2">
          <!-- Left: Blueprint -->
          <div class="arch-diagram">
            <div class="arch-node primary">
              <span>TEMPORAL RUNTIME WORKFLOWS</span>
              <span class="badge-pill badge-olive">Orchestrator</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
              <div class="arch-node" style="font-size: 13px; justify-content: center;">Acquisition Domain</div>
              <div class="arch-node" style="font-size: 13px; justify-content: center;">Marketing Domain</div>
              <div class="arch-node" style="font-size: 13px; justify-content: center;">RevOps Domain</div>
            </div>
            <div class="arch-arrow">▼</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
              <div class="arch-node"><span>Deterministic Rules</span></div>
              <div class="arch-node"><span>Selective LangGraph Loops</span></div>
            </div>
            <div class="arch-arrow">▼</div>
            <div class="arch-node warning" style="border: 2px solid var(--ochre);">
              <span>POLICY ENGINE & DECISION CONTRACT</span>
              <span class="badge-pill badge-ochre">The Enforcement Gate</span>
            </div>
            <div class="arch-arrow">▼</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
              <div class="arch-node" style="justify-content: center;">Dolibarr CRM API</div>
              <div class="arch-node" style="justify-content: center;">Shopify & Meta API</div>
            </div>
            <div class="arch-arrow">▼</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
              <div class="arch-node primary" style="justify-content: center;">PostgreSQL Storage</div>
              <div class="arch-node primary" style="justify-content: center;">Audit Trail & Tracing</div>
            </div>
          </div>

          <!-- Right: What Changes -->
          <div class="card accent-ochre">
            <span class="card-tag tag-ochre">The Architectural Leap</span>
            <h3 class="card-title">From Automation to Governed Intelligence</h3>
            <p class="card-desc">In Tier 1, Temporal executes commands. In Tier 2, the system must justify decisions before execution.</p>
            <ul class="bullet-list ochre">
              <li><strong>Policy Engine:</strong> Independent rules governing budget, pricing, discounts, and communication cadence.</li>
              <li><strong>Decision Contracts:</strong> Every AI recommendation is parsed into a typed, validated JSON contract before evaluation.</li>
              <li><strong>Post-Action Verification:</strong> After invoking an external API, the system queries the external service to mathematically verify state change.</li>
              <li><strong>Selective LangGraph:</strong> Bounded reasoning graphs used strictly for complex evaluations (e.g. ad creative analysis), never for the whole app.</li>
              <li><strong>Full Tracing & Auditability:</strong> OpenTelemetry traces every model call, latency, cost, and decision path.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 09 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 10: Tier 2 Decision Contract in Action -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="10">
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1600" width="1000" height="1600">

  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&amp;family=JetBrains+Mono:wght@500;700&amp;family=Plus+Jakarta+Sans:wght@500;600;700&amp;display=swap');
      text { font-family: 'Caveat', cursive, sans-serif; }
    </style>
    <filter id="handDrawn" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.2" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF" />

  <text x="480.0" y="53" fill="#181916" font-size="23" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="middle">
    <tspan x="480.0" dy="0">Tier 2: Professional Revenue Intelligence — Governed Decision Architecture</tspan>
  </text>
  <text x="480.0" y="79" fill="#C48737" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Policy Engines  •  Decision Contracts  •  Post-Action Verification  •  Blast Radius: Strictly Bounded</tspan>
  </text>
  <ellipse cx="480.0" cy="137.5" rx="135.0" ry="27.5" fill="#FEE2E2" stroke="#F87171" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="137" fill="#991B1B" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Ad Spend &amp; Refill Signal Trigger</tspan>
    <tspan x="480.0" dy="17">(Meta ROAS &gt; 4.0x / Day-20 Refill)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="165" x2="480" y2="205" stroke="#181916" stroke-width="2" />
    <polygon points="480,205 473.5,193.7416697508023 486.5,193.7416697508023" fill="#181916" />
  </g>
  <rect x="335" y="205" width="290" height="55" rx="12" fill="#E0F2FE" stroke="#38BDF8" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="232" fill="#0369A1" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Ingest Meta Campaign Telemetry</tspan>
    <tspan x="480.0" dy="17">(CPA, CTR, Daily Spend, Revenue)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="260" x2="480" y2="295" stroke="#181916" stroke-width="2" />
    <polygon points="480,295 473.5,283.7416697508023 486.5,283.7416697508023" fill="#181916" />
  </g>
  <rect x="240" y="295" width="480" height="125" rx="12" fill="#F3E8FF" stroke="#C084FC" stroke-width="2" filter="url(#handDrawn)" />
  <text x="255" y="320" fill="#7E22CE" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="255" dy="0">Selective LangGraph Agent — Budget &amp; Creative Reasoning</tspan>
  </text>
  <rect x="265" y="340" width="200" height="55" rx="12" fill="#FFFFFF" stroke="#A855F7" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="365.0" y="366" fill="#6B21A8" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="365.0" dy="0">Evaluate 7-Day Performance</tspan>
    <tspan x="365.0" dy="15">(ROAS = 4.2x, CPA = €12)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="465" y1="367" x2="495" y2="367" stroke="#A855F7" stroke-width="2" />
    <polygon points="495,367 483.7416697508023,373.5 483.7416697508023,360.5" fill="#A855F7" />
  </g>
  <rect x="495" y="340" width="200" height="55" rx="12" fill="#FFFFFF" stroke="#A855F7" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="595.0" y="366" fill="#6B21A8" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="595.0" dy="0">Propose Budget Delta:</tspan>
    <tspan x="595.0" dy="15">Increase €30 ➔ €39/day (+30%)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="420" x2="480" y2="460" stroke="#181916" stroke-width="2" />
    <polygon points="480,460 473.5,448.7416697508023 486.5,448.7416697508023" fill="#181916" />
  </g>
  <rect x="335" y="460" width="290" height="55" rx="12" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="487" fill="#C2410C" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Serialize to Typed Decision Contract</tspan>
    <tspan x="480.0" dy="17">(Schema: action, delta, bounds, target)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="515" x2="480" y2="550" stroke="#181916" stroke-width="2" />
    <polygon points="480,550 473.5,538.7416697508023 486.5,538.7416697508023" fill="#181916" />
  </g>
  <polygon points="480.0,550 565,605.0 480.0,660 395,605.0" fill="#FEF08A" stroke="#EAB308" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="599" fill="#854D0E" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">JSON Schema</tspan>
    <tspan x="480.0" dy="17">Valid?</tspan>
    <tspan x="480.0" dy="17">(Pydantic)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="565" y1="605" x2="660" y2="605" stroke="#EF4444" stroke-width="2" />
    <polygon points="660,605 648.7416697508023,611.5 648.7416697508023,598.5" fill="#EF4444" />
  </g>
  <text x="612.5" y="599.0" fill="#DC2626" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="612.5" dy="0">FAIL</tspan>
  </text>
  <rect x="660" y="580" width="165" height="50" rx="12" fill="#FEE2E2" stroke="#F87171" stroke-width="2" filter="url(#handDrawn)" />
  <text x="742.5" y="603.5" fill="#991B1B" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="742.5" dy="0">Reject Malformed Contract</tspan>
    <tspan x="742.5" dy="15">Alert Cyril (Zero Action)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="660" x2="480" y2="705" stroke="#15803D" stroke-width="2" />
    <polygon points="480,705 473.5,693.7416697508023 486.5,693.7416697508023" fill="#15803D" />
  </g>
  <text x="523.0" y="684.5" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">PASS</tspan>
  </text>
  <rect x="230" y="705" width="500" height="115" rx="12" fill="#E0F2FE" stroke="#0284C7" stroke-width="2" filter="url(#handDrawn)" />
  <text x="245" y="730" fill="#0369A1" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="245" dy="0">Policy Engine Independent Evaluation (Deterministic Rules)</tspan>
  </text>
  <rect x="250" y="750" width="145" height="50" rx="12" fill="#FFFFFF" stroke="#38BDF8" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="322.5" y="773.5" fill="#0369A1" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="322.5" dy="0">Daily Ceiling Check</tspan>
    <tspan x="322.5" dy="15">(€39 &lt;= €50 cap)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="395" y1="775" x2="420" y2="775" stroke="#0284C7" stroke-width="2" />
    <polygon points="420,775 408.7416697508023,781.5 408.7416697508023,768.5" fill="#0284C7" />
  </g>
  <rect x="420" y="750" width="145" height="50" rx="12" fill="#FFFFFF" stroke="#38BDF8" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="492.5" y="773.5" fill="#0369A1" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="492.5" dy="0">Min Run Time Check</tspan>
    <tspan x="492.5" dy="15">(Active &gt; 7 Days)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="565" y1="775" x2="590" y2="775" stroke="#0284C7" stroke-width="2" />
    <polygon points="590,775 578.7416697508023,781.5 578.7416697508023,768.5" fill="#0284C7" />
  </g>
  <rect x="590" y="750" width="145" height="50" rx="12" fill="#FFFFFF" stroke="#38BDF8" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="662.5" y="773.5" fill="#0369A1" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="662.5" dy="0">Max Daily Delta</tspan>
    <tspan x="662.5" dy="15">(&lt;= +35% Rule)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="820" x2="480" y2="860" stroke="#181916" stroke-width="2" />
    <polygon points="480,860 473.5,848.7416697508023 486.5,848.7416697508023" fill="#181916" />
  </g>
  <polygon points="480.0,860 565,915.0 480.0,970 395,915.0" fill="#FEF08A" stroke="#EAB308" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="909" fill="#854D0E" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Policy Engine</tspan>
    <tspan x="480.0" dy="17">Passed?</tspan>
    <tspan x="480.0" dy="17">(Zero Risk)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="565" y1="915" x2="660" y2="915" stroke="#EF4444" stroke-width="2" />
    <polygon points="660,915 648.7416697508023,921.5 648.7416697508023,908.5" fill="#EF4444" />
  </g>
  <text x="612.5" y="909.0" fill="#DC2626" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="612.5" dy="0">VIOLATION</tspan>
  </text>
  <rect x="660" y="890" width="165" height="50" rx="12" fill="#FEE2E2" stroke="#F87171" stroke-width="2" filter="url(#handDrawn)" />
  <text x="742.5" y="914" fill="#991B1B" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="742.5" dy="0">Halt Execution</tspan>
    <tspan x="742.5" dy="15">Log Policy Breach</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="970" x2="480" y2="1015" stroke="#15803D" stroke-width="2" />
    <polygon points="480,1015 473.5,1003.7416697508023 486.5,1003.7416697508023" fill="#15803D" />
  </g>
  <text x="523.0" y="994.5" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">COMPLIANT</tspan>
  </text>
  <polygon points="480.0,1015 565,1070.0 480.0,1125 395,1070.0" fill="#FEF08A" stroke="#EAB308" stroke-width="3" filter="url(#handDrawn)" />
  <text x="480.0" y="1064" fill="#854D0E" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Delta &gt; €5/day?</tspan>
    <tspan x="480.0" dy="17">(Human Sign-Off</tspan>
    <tspan x="480.0" dy="17">Required)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="395" y1="1070" x2="300" y2="1070" stroke="#15803D" stroke-width="2" />
    <polygon points="300,1070 311.2583302491977,1063.5 311.2583302491977,1076.5" fill="#15803D" />
  </g>
  <text x="347.5" y="1064.0" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="347.5" dy="0">NO (&lt;= €5)</tspan>
  </text>
  <rect x="125" y="1045" width="175" height="50" rx="12" fill="#DCFCE7" stroke="#4ADE80" stroke-width="2" filter="url(#handDrawn)" />
  <text x="212.5" y="1069" fill="#166534" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="212.5" dy="0">Auto-Execution Permitted</tspan>
    <tspan x="212.5" dy="15">(Within Policy Bounds)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1125" x2="480" y2="1170" stroke="#C48737" stroke-width="2" />
    <polygon points="480,1170 473.5,1158.7416697508022 486.5,1158.7416697508022" fill="#C48737" />
  </g>
  <text x="523.0" y="1149.5" fill="#C48737" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">YES (+€9/day)</tspan>
  </text>
  <rect x="335" y="1170" width="290" height="55" rx="12" fill="#FCF4E8" stroke="#C48737" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="1197" fill="#9A6622" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Sidy 1-Tap WhatsApp Approval</tspan>
    <tspan x="480.0" dy="17">[Approve +€9/day] or [Reject]</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1225" x2="480" y2="1265" stroke="#15803D" stroke-width="2" />
    <polygon points="480,1265 473.5,1253.7416697508022 486.5,1253.7416697508022" fill="#15803D" />
  </g>
  <text x="523.0" y="1247.0" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">APPROVED</tspan>
  </text>
  <rect x="335" y="1265" width="290" height="55" rx="12" fill="#E0F2FE" stroke="#38BDF8" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="1292" fill="#0369A1" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Temporal Activity Dispatch:</tspan>
    <tspan x="480.0" dy="17">Update Meta AdSet Budget to €39.00</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1320" x2="480" y2="1355" stroke="#181916" stroke-width="2" />
    <polygon points="480,1355 473.5,1343.7416697508022 486.5,1343.7416697508022" fill="#181916" />
  </g>
  <rect x="335" y="1355" width="290" height="55" rx="12" fill="#DCFCE7" stroke="#4ADE80" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="1382" fill="#166534" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Post-Action Verification Query</tspan>
    <tspan x="480.0" dy="17">(Re-query Meta API to confirm state = €39.00)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1410" x2="480" y2="1445" stroke="#181916" stroke-width="2" />
    <polygon points="480,1445 473.5,1433.7416697508022 486.5,1433.7416697508022" fill="#181916" />
  </g>
  <rect x="310" y="1445" width="340" height="60" rx="12" fill="#DCFCE7" stroke="#22C55E" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="1470.5" fill="#15803D" font-size="13.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Immutable Audit Trail Written</tspan>
    <tspan x="480.0" dy="17">(PostgreSQL + OpenTelemetry Distributed Trace)</tspan>
  </text>
</svg>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 10 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 11: Tier 3 Architecture -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="11">
      <div class="slide-header">
        <div class="kicker">Tier 3 // Technical Architecture</div>
        <h2 class="slide-title">Autonomous Revenue Platform Blueprint</h2>
        <p class="slide-subtitle">
          When commercial scale reaches 100+ accounts, the system transitions into an autonomous, closed-loop revenue engine powered by MCP capability boundaries and shared revenue state.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-2">
          <!-- Architecture Flow -->
          <div class="arch-diagram">
            <div class="arch-node primary">
              <span>TEMPORAL RUNTIME & EVENT BUS</span>
              <span class="badge-pill badge-olive">Event Backbone</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
              <div class="arch-node warning" style="font-size: 13px; justify-content: center;">Acquisition Agent</div>
              <div class="arch-node warning" style="font-size: 13px; justify-content: center;">Ads & Creative Agent</div>
              <div class="arch-node warning" style="font-size: 13px; justify-content: center;">RevOps Agent</div>
            </div>
            <div class="arch-arrow">▼</div>
            <div class="arch-node" style="background: var(--card-alt); border-color: var(--border);">
              <span>SHARED REVENUE STATE & REAL-TIME REVENUE GRAPH</span>
            </div>
            <div class="arch-arrow">▼</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
              <div class="arch-node" style="font-size: 13px; justify-content: center;">Policy Engine</div>
              <div class="arch-node" style="font-size: 13px; justify-content: center;">Enterprise RAG/KB</div>
              <div class="arch-node" style="font-size: 13px; justify-content: center;">Revenue Analytics</div>
            </div>
            <div class="arch-arrow">▼</div>
            <div class="arch-node" style="border: 2px solid var(--forest); background: var(--forest-light);">
              <span>MCP CAPABILITY LAYER (Model Context Protocol)</span>
              <span class="badge-pill" style="background: var(--forest); color: #FFF;">Dynamic Tools</span>
            </div>
            <div class="arch-arrow">▼</div>
            <div class="arch-node primary">
              <span>CLOSED-LOOP LEARNING: Customer LTV Feedback ➔ Ad Hypotheses</span>
            </div>
          </div>

          <!-- Why Complexity is Earned -->
          <div class="card accent-forest">
            <span class="card-tag tag-forest">Earned Complexity</span>
            <h3 class="card-title">When Is Tier 3 Justified?</h3>
            <p class="card-desc">Tier 3 is built ONLY when customer transaction volume warrants it:</p>
            <ul class="bullet-list">
              <li><strong>Cross-Domain Signals:</strong> Cafe reorder frequency directly triggers creative testing on Meta Ads without human intervention.</li>
              <li><strong>MCP Dynamic Capabilities:</strong> Agents dynamically discover tools and query inventory, CRM, and logistics via standardized protocol boundaries.</li>
              <li><strong>Continuous Experimentation:</strong> The system formulates hypotheses (e.g. "Highlighting iced tea cold-brew increases terrace cafe conversions by 40%"), executes test campaigns, and measures LTV impact.</li>
              <li><strong>True Scale:</strong> Operates 200+ partner accounts across multiple countries with zero additional administrative personnel.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 11 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 12: Tier 3 Closed-Loop Flywheel -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="12">
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1300" width="1000" height="1300">

  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&amp;family=JetBrains+Mono:wght@500;700&amp;family=Plus+Jakarta+Sans:wght@500;600;700&amp;display=swap');
      text { font-family: 'Caveat', cursive, sans-serif; }
    </style>
    <filter id="handDrawn" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="2.2" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="#FFFFFF" />

  <text x="480.0" y="53" fill="#181916" font-size="23" font-family="Caveat, cursive, sans-serif" font-weight="700" text-anchor="middle">
    <tspan x="480.0" dy="0">Tier 3: Autonomous Revenue Platform — Closed-Loop Commercial Flywheel</tspan>
  </text>
  <text x="480.0" y="79" fill="#2F5339" font-size="14" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Multi-Agent Coordination  •  Model Context Protocol (MCP)  •  Circuit Breakers  •  Autopilot Flywheel</tspan>
  </text>
  <ellipse cx="480.0" cy="137.5" rx="145.0" ry="27.5" fill="#FEE2E2" stroke="#F87171" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="137" fill="#991B1B" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Commercial Event Stream (PubSub)</tspan>
    <tspan x="480.0" dy="17">(Refill Cycles across 100+ Partner Accounts)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="165" x2="480" y2="205" stroke="#181916" stroke-width="2" />
    <polygon points="480,205 473.5,193.7416697508023 486.5,193.7416697508023" fill="#181916" />
  </g>
  <rect x="330" y="205" width="300" height="55" rx="12" fill="#E0F2FE" stroke="#38BDF8" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="232" fill="#0369A1" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Shared Revenue State Graph</tspan>
    <tspan x="480.0" dy="17">(LTV, Account Health, Inventory Velocity)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="260" x2="480" y2="295" stroke="#181916" stroke-width="2" />
    <polygon points="480,295 473.5,283.7416697508023 486.5,283.7416697508023" fill="#181916" />
  </g>
  <rect x="210" y="295" width="540" height="125" rx="12" fill="#F3E8FF" stroke="#C084FC" stroke-width="2" filter="url(#handDrawn)" />
  <text x="225" y="320" fill="#7E22CE" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="225" dy="0">Domain Specialist Agents (Temporal Coordinated)</tspan>
  </text>
  <rect x="240" y="340" width="150" height="55" rx="12" fill="#FFFFFF" stroke="#A855F7" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="315.0" y="364" fill="#6B21A8" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="315.0" dy="0">Acquisition Agent</tspan>
    <tspan x="315.0" dy="15">(Scrape &amp; Qualify)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="390" y1="367" x2="415" y2="367" stroke="#A855F7" stroke-width="2" />
    <polygon points="415,367 403.7416697508023,373.5 403.7416697508023,360.5" fill="#A855F7" />
  </g>
  <rect x="415" y="340" width="150" height="55" rx="12" fill="#FFFFFF" stroke="#A855F7" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="490.0" y="364" fill="#6B21A8" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="490.0" dy="0">Creative Ads Agent</tspan>
    <tspan x="490.0" dy="15">(Ad Generation &amp; ROAS)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="565" y1="367" x2="590" y2="367" stroke="#A855F7" stroke-width="2" />
    <polygon points="590,367 578.7416697508023,373.5 578.7416697508023,360.5" fill="#A855F7" />
  </g>
  <rect x="590" y="340" width="150" height="55" rx="12" fill="#FFFFFF" stroke="#A855F7" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="665.0" y="364" fill="#6B21A8" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="665.0" dy="0">RevOps Agent</tspan>
    <tspan x="665.0" dy="15">(Refills &amp; Invoicing)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="420" x2="480" y2="460" stroke="#181916" stroke-width="2" />
    <polygon points="480,460 473.5,448.7416697508023 486.5,448.7416697508023" fill="#181916" />
  </g>
  <rect x="330" y="460" width="300" height="55" rx="12" fill="#FFEDD5" stroke="#FDBA74" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="487" fill="#C2410C" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Continuous Experimentation Engine</tspan>
    <tspan x="480.0" dy="17">(Munich Earl Grey 2x Refill ➔ Formulate Ad)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="515" x2="480" y2="550" stroke="#181916" stroke-width="2" />
    <polygon points="480,550 473.5,538.7416697508023 486.5,538.7416697508023" fill="#181916" />
  </g>
  <polygon points="480.0,550 570,605.0 480.0,660 390,605.0" fill="#FEF08A" stroke="#EAB308" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="599" fill="#854D0E" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Circuit Breakers</tspan>
    <tspan x="480.0" dy="17">Normal?</tspan>
    <tspan x="480.0" dy="17">(Spend &amp; Anomaly)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="570" y1="605" x2="665" y2="605" stroke="#EF4444" stroke-width="2" />
    <polygon points="665,605 653.7416697508023,611.5 653.7416697508023,598.5" fill="#EF4444" />
  </g>
  <text x="617.5" y="599.0" fill="#DC2626" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="617.5" dy="0">ANOMALY</tspan>
  </text>
  <rect x="665" y="580" width="165" height="50" rx="12" fill="#FEE2E2" stroke="#F87171" stroke-width="2" filter="url(#handDrawn)" />
  <text x="747.5" y="604" fill="#991B1B" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="747.5" dy="0">Instant System Pause</tspan>
    <tspan x="747.5" dy="15">Alert Cyril / Sidy</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="660" x2="480" y2="705" stroke="#15803D" stroke-width="2" />
    <polygon points="480,705 473.5,693.7416697508023 486.5,693.7416697508023" fill="#15803D" />
  </g>
  <text x="523.0" y="684.5" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">NORMAL</tspan>
  </text>
  <rect x="220" y="705" width="520" height="115" rx="12" fill="#DCFCE7" stroke="#22C55E" stroke-width="2" filter="url(#handDrawn)" />
  <text x="235" y="730" fill="#166534" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="start">
    <tspan x="235" dy="0">Model Context Protocol (MCP) Standardized Tool Invocations</tspan>
  </text>
  <rect x="245" y="790" width="150" height="50" rx="12" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="320.0" y="813.5" fill="#15803D" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="320.0" dy="0">mcp_meta_ads</tspan>
    <tspan x="320.0" dy="15">(Auto-Deploy Munich Ad)</tspan>
  </text>
  <rect x="420" y="790" width="150" height="50" rx="12" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="495.0" y="813.5" fill="#15803D" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="495.0" dy="0">mcp_dolibarr_crm</tspan>
    <tspan x="495.0" dy="15">(Reserve 50kg Earl Grey)</tspan>
  </text>
  <rect x="595" y="790" width="150" height="50" rx="12" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5" filter="url(#handDrawn)" />
  <text x="670.0" y="813.5" fill="#15803D" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="670.0" dy="0">mcp_warehouse_log</tspan>
    <tspan x="670.0" dy="15">(Trigger Berlin ➔ MUC)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="820" x2="480" y2="860" stroke="#181916" stroke-width="2" />
    <polygon points="480,860 473.5,848.7416697508023 486.5,848.7416697508023" fill="#181916" />
  </g>
  <polygon points="480.0,860 570,915.0 480.0,970 390,915.0" fill="#FEF08A" stroke="#EAB308" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="909" fill="#854D0E" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">German Food Regs</tspan>
    <tspan x="480.0" dy="17">&amp; Gross Margin</tspan>
    <tspan x="480.0" dy="17">&gt;= 75%?</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="570" y1="915" x2="665" y2="915" stroke="#EF4444" stroke-width="2" />
    <polygon points="665,915 653.7416697508023,921.5 653.7416697508023,908.5" fill="#EF4444" />
  </g>
  <text x="617.5" y="909.0" fill="#DC2626" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="617.5" dy="0">NON-COMPLIANT</tspan>
  </text>
  <rect x="665" y="890" width="165" height="50" rx="12" fill="#FEE2E2" stroke="#F87171" stroke-width="2" filter="url(#handDrawn)" />
  <text x="747.5" y="913.5" fill="#991B1B" font-size="11.5" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="747.5" dy="0">Reject Tool Call</tspan>
    <tspan x="747.5" dy="15">Flag Botanical Labeling</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="970" x2="480" y2="1015" stroke="#15803D" stroke-width="2" />
    <polygon points="480,1015 473.5,1003.7416697508023 486.5,1003.7416697508023" fill="#15803D" />
  </g>
  <text x="523.0" y="994.5" fill="#15803D" font-size="12" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="523.0" dy="0">COMPLIANT</tspan>
  </text>
  <rect x="330" y="1015" width="300" height="55" rx="12" fill="#DCFCE7" stroke="#4ADE80" stroke-width="2" filter="url(#handDrawn)" />
  <text x="480.0" y="1042" fill="#166534" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Execute Autonomous Actions Across Cities</tspan>
    <tspan x="480.0" dy="17">(Munich Ad Deployed + Warehouses Synced)</tspan>
  </text>
  <g filter="url(#handDrawn)">
    <line x1="480" y1="1070" x2="480" y2="1105" stroke="#181916" stroke-width="2" />
    <polygon points="480,1105 473.5,1093.7416697508022 486.5,1093.7416697508022" fill="#181916" />
  </g>
  <rect x="300" y="1105" width="360" height="65" rx="12" fill="#DCFCE7" stroke="#22C55E" stroke-width="2.5" filter="url(#handDrawn)" />
  <text x="480.0" y="1130" fill="#15803D" font-size="13" font-family="Caveat, cursive, sans-serif" font-weight="600" text-anchor="middle">
    <tspan x="480.0" dy="0">Autonomous Flywheel Active (100+ Accounts)</tspan>
    <tspan x="480.0" dy="17">LTV Reorder Velocity Continuously Trains Ad Agent</tspan>
    <tspan x="480.0" dy="17">Sidy Acts as Executive Supervisor (&lt;2 hrs/wk)</tspan>
  </text>
</svg>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 12 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 13: Master Tier Comparison Matrix -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="13">
      <div class="slide-header">
        <div class="kicker">System Design Benchmark</div>
        <h2 class="slide-title">Master Architectural Comparison Matrix</h2>
        <p class="slide-subtitle">
          How capabilities, governance, and technology stacks evolve systematically across the three tiers.
        </p>
      </div>

      <div class="slide-body">
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th style="width: 28%;">Capability / Dimension</th>
                <th style="width: 24%;">Tier 1 // Essential</th>
                <th style="width: 24%;">Tier 2 // Professional</th>
                <th style="width: 24%;">Tier 3 // Autonomous</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Commercial Positioning</strong></td>
                <td>Lead Gen & Follow-Up System</td>
                <td>AI Revenue Intelligence System</td>
                <td>AI Revenue Operations Platform</td>
              </tr>
              <tr>
                <td><strong>Autonomy Philosophy</strong></td>
                <td>Human-Directed Automation</td>
                <td>Human-Governed Intelligence</td>
                <td>Policy-Governed Autonomy</td>
              </tr>
              <tr>
                <td><strong>State & Workflow Engine</strong></td>
                <td>Temporal Durable Execution</td>
                <td>Temporal + Domain Services</td>
                <td>Temporal Runtime + Event Bus</td>
              </tr>
              <tr>
                <td><strong>Policy & Governance Gate</strong></td>
                <td>Basic Static Checks</td>
                <td><span class="check-yes">✓</span> Formal Policy Engine</td>
                <td><span class="check-yes">✓</span> Autonomous Policy Engine</td>
              </tr>
              <tr>
                <td><strong>Post-Action State Verification</strong></td>
                <td>Basic API status code</td>
                <td><span class="check-yes">✓</span> Query & Verify External State</td>
                <td><span class="check-yes">✓</span> Continuous State Reconciliation</td>
              </tr>
              <tr>
                <td><strong>Audit & Telemetry Trail</strong></td>
                <td>Application Logs</td>
                <td><span class="check-yes">✓</span> Structured Audit Trail</td>
                <td><span class="check-yes">✓</span> OpenTelemetry + GenAI Tracing</td>
              </tr>
              <tr>
                <td><strong>LangGraph & Agent Roles</strong></td>
                <td><span class="check-no">None (Pure Temporal)</span></td>
                <td><span class="badge-pill badge-ochre">Selective Sub-Loops</span></td>
                <td><span class="check-yes">✓</span> Multi-Agent Domain Teams</td>
              </tr>
              <tr>
                <td><strong>MCP (Model Context Protocol)</strong></td>
                <td><span class="check-no">Optional / Direct APIs</span></td>
                <td><span class="badge-pill badge-ochre">Selective Tool Layer</span></td>
                <td><span class="check-yes">✓</span> Full MCP Infrastructure</td>
              </tr>
              <tr>
                <td><strong>Closed-Loop Feedback</strong></td>
                <td><span class="check-no">Manual Analysis</span></td>
                <td>Deterministic Reporting</td>
                <td><span class="check-yes">✓</span> Automated Campaign Optimization</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 13 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 14: Autonomy Maturity -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="14">
      <div class="slide-header">
        <div class="kicker">Operational Risk & Blast Radius</div>
        <h2 class="slide-title">The Autonomy Spectrum & Blast Radius Containment</h2>
        <p class="slide-subtitle">
          The difference between tiers is not merely "more code." It is the structured management of risk and blast radius across the business.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-3">
          <div class="card accent-olive">
            <span class="card-tag tag-olive">Tier 1 Autonomy</span>
            <h3 class="card-title">Human-Directed</h3>
            <div style="font-size: 15px; font-weight: 700; color: var(--olive); margin-bottom: 12px;">BLAST RADIUS: ZERO</div>
            <ul class="bullet-list">
              <li>Machine only reads public web data and gathers facts.</li>
              <li>Every prospect message, proposal, and sample box dispatch requires human click.</li>
              <li>No external financial or legal commitment can be initiated by AI.</li>
              <li><strong>Verdict:</strong> 100% safe for early-stage founders and fragile brand trust.</li>
            </ul>
          </div>

          <div class="card accent-ochre highlight">
            <span class="card-tag tag-ochre">Tier 2 Autonomy</span>
            <h3 class="card-title">Human-Governed</h3>
            <div style="font-size: 15px; font-weight: 700; color: var(--ochre-dark); margin-bottom: 12px;">BLAST RADIUS: STRICTLY BOUNDED</div>
            <ul class="bullet-list ochre">
              <li>Machine autonomously executes low-risk standard tasks (e.g. Day-20 check-in text).</li>
              <li>High-risk actions (ad budget changes, price changes, custom terms) trigger Decision Contracts.</li>
              <li>Human approval required for any action outside policy bounds.</li>
              <li><strong>Verdict:</strong> High leverage with guaranteed safety nets.</li>
            </ul>
          </div>

          <div class="card accent-forest">
            <span class="card-tag tag-forest">Tier 3 Autonomy</span>
            <h3 class="card-title">Policy-Governed</h3>
            <div style="font-size: 15px; font-weight: 700; color: var(--forest); margin-bottom: 12px;">BLAST RADIUS: MATHEMATICALLY CONTROLLED</div>
            <ul class="bullet-list">
              <li>Machine autonomously shifts ad spend, rotates blends, and optimizes schedules.</li>
              <li>Protected by automated circuit breakers: any sudden anomaly halts the system instantly.</li>
              <li>Human executive acts as supervisor reviewing weekly performance digests.</li>
              <li><strong>Verdict:</strong> Massive operational scale with automated anomaly defense.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 14 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 15: Instagram Architecture -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="15">
      <div class="slide-header">
        <div class="kicker">Omnichannel Acquisition</div>
        <h2 class="slide-title">Instagram as a First-Class Architecture Channel</h2>
        <p class="slide-subtitle">
          Instagram is an essential acquisition channel and signal source across all three tiers — not a disconnected fourth agent or an afterthought.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-4">
          <div class="card">
            <span class="card-tag tag-olive">Role 01</span>
            <h4 class="card-title" style="font-size: 21px;">Outbound Prospecting</h4>
            <p class="card-desc" style="font-size: 15px;">System identifies specialty brunch cafes, analyses interior aesthetic from feed, and pre-qualifies tea menu fit.</p>
          </div>

          <div class="card highlight">
            <span class="card-tag tag-ochre">Role 02</span>
            <h4 class="card-title" style="font-size: 21px;">OpenReply Inbound</h4>
            <p class="card-desc" style="font-size: 15px;">A barista comments "TEABAR" on a reel. OpenReply triggers an instant DM sending a 60-second qualification link for the €19 trial box.</p>
          </div>

          <div class="card">
            <span class="card-tag tag-forest">Role 03</span>
            <h4 class="card-title" style="font-size: 21px;">Marketing Signals</h4>
            <p class="card-desc" style="font-size: 15px;">Cafe owners liking or commenting on whole-leaf brewing reels generate intent signals, triggering automated enrichment in Dolibarr.</p>
          </div>

          <div class="card">
            <span class="card-tag tag-olive">Role 04</span>
            <h4 class="card-title" style="font-size: 21px;">Paid Acquisition</h4>
            <p class="card-desc" style="font-size: 15px;">Meta Ads funnels targeted German cafe owners into direct WhatsApp conversations and credited sample landing pages.</p>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 15 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 16: Instagram Sophistication Evolution -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="16">
      <div class="slide-header">
        <div class="kicker">Channel Evolution Across Tiers</div>
        <h2 class="slide-title">How Instagram Matures Across Tiers</h2>
        <p class="slide-subtitle">
          Tier 1 does not mean a compromised Instagram experience. It has a complete, working comment-to-DM loop. Higher tiers add intelligence, governance, and cross-channel optimization.
        </p>
      </div>

      <div class="slide-body">
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th style="width: 28%;">Instagram Workflow Dimension</th>
                <th style="width: 24%;">Tier 1 // Essential</th>
                <th style="width: 24%;">Tier 2 // Professional</th>
                <th style="width: 24%;">Tier 3 // Autonomous</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Comment ➔ DM Automation</strong></td>
                <td><span class="check-yes">✓</span> OpenReply Keyword Triggers</td>
                <td><span class="check-yes">✓</span> OpenReply + Context Routing</td>
                <td><span class="check-yes">✓</span> Dynamic Intent Extraction</td>
              </tr>
              <tr>
                <td><strong>Lead Qualification Link</strong></td>
                <td><span class="check-yes">✓</span> Standard 60-Sec Intake</td>
                <td><span class="check-yes">✓</span> Dynamic Gated Qualification</td>
                <td><span class="check-yes">✓</span> Real-Time Venue Scoring</td>
              </tr>
              <tr>
                <td><strong>Dolibarr CRM Lead Sync</strong></td>
                <td><span class="check-yes">✓</span> Immediate Lead Creation</td>
                <td><span class="check-yes">✓</span> Lead Card + Social Scores</td>
                <td><span class="check-yes">✓</span> Full Omnichannel Identity</td>
              </tr>
              <tr>
                <td><strong>Outreach Messaging</strong></td>
                <td>AI-Drafted ➔ Human Approves</td>
                <td>Governed Template Engine</td>
                <td>Autonomous Personalized DM</td>
              </tr>
              <tr>
                <td><strong>Engagement Signal Mining</strong></td>
                <td><span class="check-no">Manual Observation</span></td>
                <td><span class="check-yes">✓</span> Profile Engagement Scoring</td>
                <td><span class="check-yes">✓</span> Predictive Prospect Triggers</td>
              </tr>
              <tr>
                <td><strong>Meta Ads Optimization</strong></td>
                <td><span class="check-no">Manual Ad Manager</span></td>
                <td>AI Recommendations (+30% Rule)</td>
                <td><span class="check-yes">✓</span> Autonomous Budget Allocation</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 16 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 17: Non-Destructive Upgrade Path -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="17">
      <div class="slide-header">
        <div class="kicker">Lifecycle Engineering</div>
        <h2 class="slide-title">Evolving Without Rewriting</h2>
        <p class="slide-subtitle">
          Customers never have to throw away code or migrate databases when upgrading. The architecture expands outward like onion layers around the core.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-3">
          <div class="card accent-olive">
            <span class="card-tag tag-olive">Foundation // Tier 1</span>
            <h3 class="card-title">The Durable Substrate</h3>
            <ul class="bullet-list">
              <li>Temporal Orchestration Engine</li>
              <li>PostgreSQL Core Schemas</li>
              <li>Direct Dolibarr REST API Client</li>
              <li>Direct Meta / OpenReply Webhooks</li>
              <li>LLM Prompt Templates & OCR Parser</li>
            </ul>
            <div style="margin-top: 18px; padding: 12px; background: var(--olive-light); border-radius: 8px; font-size: 14px; font-weight: 600; color: var(--olive-dark);">
              Remains 100% active in all future tiers.
            </div>
          </div>

          <div class="card accent-ochre highlight">
            <span class="card-tag tag-ochre">Layer 2 // Tier 2 Additions</span>
            <h3 class="card-title">The Governance Shell</h3>
            <ul class="bullet-list ochre">
              <li>Domain Service Abstractions</li>
              <li>Policy Evaluation Engine</li>
              <li>Decision Contract Validation Layer</li>
              <li>Post-Action State Verification</li>
              <li>OpenTelemetry Traces & Audit Logs</li>
            </ul>
            <div style="margin-top: 18px; padding: 12px; background: var(--ochre-light); border-radius: 8px; font-size: 14px; font-weight: 600; color: var(--ochre-dark);">
              Wraps around Tier 1 without altering database models.
            </div>
          </div>

          <div class="card accent-forest">
            <span class="card-tag tag-forest">Layer 3 // Tier 3 Additions</span>
            <h3 class="card-title">The Autonomous Flywheel</h3>
            <ul class="bullet-list">
              <li>Domain Specialist Agents</li>
              <li>Model Context Protocol (MCP) Tools</li>
              <li>Shared Revenue State & Event PubSub</li>
              <li>Cross-Domain Feedback Engine</li>
              <li>Continuous Experimentation Harness</li>
            </ul>
            <div style="margin-top: 18px; padding: 12px; background: var(--forest-light); border-radius: 8px; font-size: 14px; font-weight: 600; color: var(--forest);;">
              Adds autonomous loops over Tier 2 governance.
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 17 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 18: Deep-Dive Tradeoffs -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="18">
      <div class="slide-header">
        <div class="kicker">Engineering Defense</div>
        <h2 class="slide-title">System Design Tradeoff Analysis: The "Why"</h2>
        <p class="slide-subtitle">
          Every decision has a cost. A senior engineer is defined not by the tools they choose, but by the tradeoffs they can explicitly defend.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-2">
          <div class="card">
            <span class="card-tag tag-olive">Decision 01</span>
            <h4 class="card-title" style="font-size: 22px;">Temporal vs. n8n</h4>
            <p style="font-size: 15px; line-height: 1.5; color: var(--text-muted);">
              <strong>Tradeoff:</strong> Temporal requires writing real code and operating a cluster, whereas n8n has a visual UI.<br>
              <strong>Defense:</strong> Revenue operations require true durability. An unhandled exception or server restart in n8n drops state. Temporal’s append-only event history ensures zero lost invoices and deterministic replay.
            </p>
          </div>

          <div class="card">
            <span class="card-tag tag-ochre">Decision 02</span>
            <h4 class="card-title" style="font-size: 22px;">Direct APIs vs. MCP in Tiers 1–2</h4>
            <p style="font-size: 15px; line-height: 1.5; color: var(--text-muted);">
              <strong>Tradeoff:</strong> Direct Python API clients are tightly coupled; MCP standardizes tool protocols.<br>
              <strong>Defense:</strong> Direct APIs have zero protocol serialization overhead, simpler debugging, and strict type safety. MCP adds immense value in Tier 3 where agents dynamically discover tools, but is unnecessary overhead in Tier 1.
            </p>
          </div>

          <div class="card">
            <span class="card-tag tag-forest">Decision 03</span>
            <h4 class="card-title" style="font-size: 22px;">PostgreSQL vs. Event Streaming (Kafka)</h4>
            <p style="font-size: 15px; line-height: 1.5; color: var(--text-muted);">
              <strong>Tradeoff:</strong> Postgres is relational; Kafka handles massive distributed event streaming.<br>
              <strong>Defense:</strong> Alandas’ target is 100 active accounts ordering monthly. That is ~500 transactions/month. PostgreSQL ACID transactions and JSONB state easily scale to 50,000 accounts without distributed complexity.
            </p>
          </div>

          <div class="card">
            <span class="card-tag tag-olive">Decision 04</span>
            <h4 class="card-title" style="font-size: 22px;">Selective LangGraph vs. Whole-App Graphs</h4>
            <p style="font-size: 15px; line-height: 1.5; color: var(--text-muted);">
              <strong>Tradeoff:</strong> LangGraph gives cyclic graph control; Temporal gives durable execution.<br>
              <strong>Defense:</strong> LangGraph is brilliant for bounded multi-turn reflection (e.g., evaluating an ad draft). It is poor as an enterprise runtime. Temporal acts as the parent orchestrator; LangGraph runs inside an Activity.
            </p>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 18 / 19</div>
      </div>
    </div>

    <!-- =================================================================== -->
    <!-- SLIDE 19: Strategic Roadmap for Alandas -->
    <!-- =================================================================== -->
    <div class="slide" data-slide="19">
      <div class="slide-header">
        <div class="kicker">Execution Roadmap</div>
        <h2 class="slide-title">The Alandas Roadmap: Starting Tier 1 Today</h2>
        <p class="slide-subtitle">
          How Cyril and Sidy execute this strategy: stabilize operations at Tier 1 immediately, scale to 50 accounts with Tier 2, and unlock 100 accounts full-time freedom with Tier 3.
        </p>
      </div>

      <div class="slide-body">
        <div class="grid-3">
          <div class="card accent-olive highlight">
            <span class="card-tag tag-olive">Months 1–3 // Immediate Start</span>
            <h3 class="card-title">Sprint 1: Tier 1 Launch</h3>
            <p class="card-desc"><strong>Target: 25 ➔ 40 Active Accounts (€5k/mo)</strong></p>
            <ul class="bullet-list">
              <li>Stabilize Dolibarr CRM with automated daily cloud backups.</li>
              <li>Restore Hermes AI WhatsApp order parsing with deterministic rules.</li>
              <li>Deploy OpenReply Instagram comment-to-DM loop on B2B page.</li>
              <li>Standardize €19 discovery kit featuring shatter-resistant teapot.</li>
              <li>Sidy handles 10–20 WhatsApp chats daily with AI-assisted drafting.</li>
            </ul>
          </div>

          <div class="card accent-ochre">
            <span class="card-tag tag-ochre">Months 4–6 // Scaling Up</span>
            <h3 class="card-title">Sprint 2: Tier 2 Governance</h3>
            <p class="card-desc"><strong>Target: 40 ➔ 70 Active Accounts (€12k/mo)</strong></p>
            <ul class="bullet-list ochre">
              <li>Deploy Policy Engine & Decision Contracts for Meta ad spend.</li>
              <li>Automate Day-25 predictive refills via Dolibarr WhatsApp alerts.</li>
              <li>Add OpenTelemetry tracing & audit log for all AI decisions.</li>
              <li>Deploy barista table talkers and QR counter refill portals.</li>
              <li>Sidy reduces administrative hours to < 4 hours/week.</li>
            </ul>
          </div>

          <div class="card accent-forest">
            <span class="card-tag tag-forest">Months 7–12 // Full Freedom</span>
            <h3 class="card-title">Sprint 3: Tier 3 Platform</h3>
            <p class="card-desc"><strong>Target: 100 Active Accounts (€20k–€30k/mo)</strong></p>
            <ul class="bullet-list">
              <li>Closed-loop revenue flywheel: LTV data drives Meta ad creative.</li>
              <li>MCP capability layer connects multi-city logistics and warehouse.</li>
              <li>Multi-agent coordination across Germany, Austria & Switzerland.</li>
              <li>Predictable recurring gross margin of €15,000–€30,000/month.</li>
              <li><strong>Sidy quits Swiss job to be his own boss 100% full-time.</strong></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <div class="footer-brand">ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE</div>
        <div class="footer-meta">SLIDE 19 / 19</div>
      </div>
    </div>

  </div> <!-- /deck-stage -->
</div> <!-- /deck-viewport -->

<!-- CONTROLS OVERLAY -->
<div class="deck-nav">
  <button class="nav-btn" id="prevBtn" title="Previous Slide (←)">◀</button>
  <span id="slideCounter" style="margin: 0 4px; font-weight: 700;">1 / 19</span>
  <a href="excalidraw_canvas_viewer.html" target="_blank" class="nav-btn canvas-link" title="Open Multi-Tab Excalidraw Canvas Viewer" style="text-decoration:none; font-size:12px; margin-left:6px; color:#E8E6DF;">📐 Canvas</a>
  <button class="nav-btn" id="nextBtn" title="Next Slide (→)">▶</button>
</div>

<!-- =================================================================== -->
<!-- JAVASCRIPT: STAGE SCALING & SLIDE CONTROLLER -->
<!-- =================================================================== -->
<script>
  (function() {
    const stage = document.getElementById('stage');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const slideCounter = document.getElementById('slideCounter');
    
    let currentSlide = 0;
    const totalSlides = slides.length;

    // Uniform 16:9 Scale to Fit Viewport
    function scaleStage() {
      const designWidth = 1920;
      const designHeight = 1080;
      const windowWidth = window.innerWidth;
      const windowHeight = window.innerHeight;

      const scaleX = windowWidth / designWidth;
      const scaleY = windowHeight / designHeight;
      const scale = Math.min(scaleX, scaleY);

      stage.style.transform = `translate(-50%, -50%) scale(${scale})`;
    }

    window.addEventListener('resize', scaleStage);
    scaleStage();

    // Slide Navigation
    function showSlide(index) {
      if (index < 0) index = 0;
      if (index >= totalSlides) index = totalSlides - 1;
      
      slides[currentSlide].classList.remove('active');
      currentSlide = index;
      slides[currentSlide].classList.add('active');

      slideCounter.textContent = `${currentSlide + 1} / ${totalSlides}`;
    }

    prevBtn.addEventListener('click', () => showSlide(currentSlide - 1));
    nextBtn.addEventListener('click', () => showSlide(currentSlide + 1));

    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        showSlide(currentSlide + 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        showSlide(currentSlide - 1);
      } else if (e.key === 'Home') {
        e.preventDefault();
        showSlide(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        showSlide(totalSlides - 1);
      }
    });

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
      const modal = document.getElementById('flowchartModal');
      const title = document.getElementById('modalTitle');
      const dlBtn = document.getElementById('modalDownloadBtn');
      const container = document.getElementById('modalSvgContainer');

      if (title) title.textContent = data.title;
      if (dlBtn) dlBtn.href = data.download;
      const sourceSvg = document.getElementById(data.svgId);
      if (sourceSvg && container) {
        container.innerHTML = sourceSvg.innerHTML;
      }
      modalZoom = 1;
      if (container) container.style.transform = "scale(1)";
      if (modal) modal.classList.add('open');
    };

    window.closeFlowchartModal = function() {
      const modal = document.getElementById('flowchartModal');
      if (modal) modal.classList.remove('open');
    };

    window.zoomModal = function(factor) {
      modalZoom = Math.min(3.0, Math.max(0.3, modalZoom * factor));
      const container = document.getElementById('modalSvgContainer');
      if (container) container.style.transform = `scale(${modalZoom})`;
    };

    window.resetModalZoom = function() {
      modalZoom = 1;
      const container = document.getElementById('modalSvgContainer');
      if (container) container.style.transform = "scale(1)";
    };

    window.addEventListener('keydown', (e) => {
      const modal = document.getElementById('flowchartModal');
      if (e.key === 'Escape' && modal && modal.classList.contains('open')) {
        closeFlowchartModal();
      }
    });

  })();
</script>


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

</body>
</html>
"""
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[SUCCESS] Interactive HTML Presentation generated at: {output_html_path}")


# -----------------------------------------------------------------------------
# 2. NATIVE POWERPOINT PRESENTATION BUILDER
# -----------------------------------------------------------------------------
COLOR_BG = RGBColor(0xF8, 0xF6, 0xF0)          # Warm Linen
COLOR_TEXT_MAIN = RGBColor(0x18, 0x19, 0x16)   # Deep Charcoal
COLOR_TEXT_MUTED = RGBColor(0x5C, 0x59, 0x50)  # Muted Earth
COLOR_OLIVE = RGBColor(0x44, 0x4C, 0x32)       # Botanical Olive
COLOR_OCHRE = RGBColor(0xC4, 0x87, 0x37)       # Rich Ochre
COLOR_FOREST = RGBColor(0x2F, 0x53, 0x39)      # Forest Green
COLOR_CARD_BG = RGBColor(0xFF, 0xFF, 0xFF)     # Pure White
COLOR_CARD_BORDER = RGBColor(0xE4, 0xDF, 0xD3) # Sandstone Border
COLOR_LIGHT_BG = RGBColor(0xF3, 0xEF, 0xE6)    # Accent Linen Fill
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT_HEAD = "Georgia"
FONT_BODY = "Calibri"

def set_slide_bg(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

def add_header(slide, kicker_text, title_text, lead_text=None):
    set_slide_bg(slide)
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = kicker_text.upper()
    p0.font.name = FONT_BODY
    p0.font.size = Pt(11.5)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_OLIVE
    p0.space_after = Pt(4)
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p1.space_after = Pt(4)
    
    if lead_text:
        p2 = tf.add_paragraph()
        p2.text = lead_text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(13.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

def add_footer(slide, current_slide, total_slides=19):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"ALANDAS TEA BERLIN  •  TIERED REVENUE ARCHITECTURE  |  SLIDE {current_slide:02d} OF {total_slides:02d}"
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
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_formatted_card(slide, left, top, width, height, tag, title, body_bullets, tag_color=COLOR_OLIVE, bg_color=COLOR_CARD_BG, title_size=16, bullet_size=12):
    create_card(slide, left, top, width, height, bg_color=bg_color)
    tb = slide.shapes.add_textbox(left + Inches(0.24), top + Inches(0.22), width - Inches(0.48), height - Inches(0.44))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = tag.upper()
    p0.font.name = FONT_BODY
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = tag_color
    p0.space_after = Pt(4)
    
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(title_size)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p1.space_after = Pt(8)
    
    for bullet in body_bullets:
        pb = tf.add_paragraph()
        pb.text = f"•  {bullet}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(bullet_size)
        pb.font.color.rgb = COLOR_TEXT_MUTED
        pb.space_after = Pt(5)

def build_pptx_presentation(output_pptx_path):
    print("Generating Native PowerPoint Presentation...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Slide 1: Title
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)
    create_card(s1, Inches(0.8), Inches(0.75), Inches(11.733), Inches(6.0))
    tb = s1.shapes.add_textbox(Inches(1.4), Inches(1.15), Inches(10.5), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "EXECUTIVE ARCHITECTURE & COMMERCIAL STRATEGY"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_OLIVE
    p0.space_after = Pt(10)
    p1 = tf.add_paragraph()
    p1.text = "Tiered Revenue Architecture"
    p1.font.name = FONT_HEAD
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    p1.space_after = Pt(10)
    p2 = tf.add_paragraph()
    p2.text = "Designing for Durability, Governance & Scalable Revenue: Why commercial AI systems must be tiered by operational maturity rather than framework count — A case study for Alandas Tea Berlin."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(14)
    p2.font.color.rgb = COLOR_TEXT_MUTED

    tiers = [
        ("TIER 1 // ESSENTIAL", "Durable Automation", ["Human-directed workflow automation", "Temporal + Python + Postgres + APIs", "Read ➔ Analyze ➔ Propose ➔ Human Approves ➔ Execute", "Day-1 safe founder leverage without fragility"]),
        ("TIER 2 // PROFESSIONAL", "Governed Intelligence", ["Human-governed decision intelligence", "Temporal + Policy Engine + Decision Contracts", "Reason ➔ Decision Contract ➔ Policy Gate ➔ Verify", "Scaling venues (25–70 accounts) with financial guardrails"]),
        ("TIER 3 // AUTONOMOUS", "Autonomous Platform", ["Policy-governed revenue operations", "Temporal Runtime + Domain Agents + MCP Tools", "Observe ➔ Reason ➔ Policy Eval ➔ Measure ➔ Learn", "Enterprise scale (100+ accounts) with automated feedback"])
    ]
    w = Inches(3.68)
    gap = Inches(0.34)
    for i, (tag, title, bullets) in enumerate(tiers):
        add_formatted_card(s1, Inches(1.4) + i * (w + gap), Inches(4.3), w, Inches(2.1), tag, title, bullets, tag_color=COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST), title_size=15, bullet_size=10.5)

    # Slide 2: The Core Problem
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "01 // Architectural Philosophy", "The Trap of 'Maximum Architecture' on Day 1",
               "Treating every customer as if they require an autonomous multi-agent platform creates expensive, unmaintainable software.")
    add_footer(s2, 2, total_slides=19)
    cards_s2 = [
        ("THE ANTI-PATTERN", "Technology-First Sprawl", ["'Let's add LangGraph for all tasks!'", "'We need an MCP server for everything!'", "'Let's introduce Redis, Kafka & Vector DBs immediately!'", "Result: 12 points of failure, massive latency, and fragile debugging."]),
        ("THE GROUND TRUTH", "What Founders Actually Need", ["Lead inquiries from Instagram & Google Maps never get lost", "Durable WhatsApp order parsing that never crashes or wipes state", "Invoices created accurately in Dolibarr without manual math", "Timely 25-day refill prompts so cafes don't churn quietly"]),
        ("THE SOLUTION", "Requirement-First Tiers", ["Tier 1: Durable automation solves 80% of founder friction", "Tier 2: Policy engines protect budget & pricing as volume grows", "Tier 3: Autonomous feedback loops scale revenue at maturity", "Rule: Never build Tier 3 until Tier 1 unit economics are proven"])
    ]
    w = Inches(3.72)
    gap = Inches(0.28)
    for i, (tag, title, bullets) in enumerate(cards_s2):
        add_formatted_card(s2, Inches(0.8) + i * (w + gap), Inches(2.0), w, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE if i!=0 else COLOR_OCHRE, title_size=18, bullet_size=12)

    # Slide 3: Temporal Over n8n
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "02 // Runtime Decision", "Durability First: Why Temporal Over n8n?",
               "Why visual low-code tools fail for mission-critical revenue operations, and why Temporal provides the necessary foundation.")
    add_footer(s3, 3, total_slides=19)
    add_formatted_card(s3, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "LOW-CODE TOOLING // n8n REALITY", "Where n8n Breaks in Production", [
        "Transient Memory & State Loss: If a node fails mid-execution, intermediate state is lost. There is no native event replay.",
        "No Long-Running Durability: Pausing for 25 days (refill cycle) relies on fragile cron triggers instead of native durable timers.",
        "Lack of Code Versioning & CI/CD: Drag-and-drop workflows cannot be unit-tested or linted with standard software engineering practices.",
        "No Deterministic Replay: Cannot reconstruct the exact history of an order or audit an AI agent's decision tree."
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)
    add_formatted_card(s3, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "ENGINEERING FOUNDATION // TEMPORAL ADVANTAGE", "Why Temporal Guarantees Continuity", [
        "True Durable Execution: Workflows are written in Python/TS. State transitions are appended to an immutable event log.",
        "Crash Resilience: Workers can die, reboot, or migrate, and resume at the exact millisecond of execution.",
        "Built-In Idempotency & Retries: Activities have automatic exponential backoff with idempotency tokens.",
        "Native Long-Running Timers: workflow.sleep(25 * days) is a native, durable construct consuming zero compute while sleeping.",
        "Separation of Concerns: Temporal manages execution history; PostgreSQL stores business entities (clients, invoices, stock)."
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)

    # Slide 4: The Golden Rule
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "03 // Governing Principle", "'Complexity Must Be Purchased by a Requirement'",
               "Every framework, agent boundary, and distributed bus introduces new failure modes. Follow a strict decision tree.")
    add_footer(s4, 4, total_slides=19)
    # 5-step flow box
    create_card(s4, Inches(0.8), Inches(2.0), Inches(11.733), Inches(1.8))
    steps_s4 = [("01", "Business Need", "Capture cafe leads"), ("02", "Required Capability", "Comment to DM"), ("03", "Required Robustness", "100% webhook receipt"), ("04", "Architecture Tier", "Tier 1: Essential"), ("05", "Clean Code", "Temporal + OpenReply")]
    w_st = Inches(2.14)
    gap_st = Inches(0.20)
    for i, (num, name, desc) in enumerate(steps_s4):
        create_card(s4, Inches(1.0) + i*(w_st+gap_st), Inches(2.2), w_st, Inches(1.4), bg_color=COLOR_LIGHT_BG)
        tb = s4.shapes.add_textbox(Inches(1.1) + i*(w_st+gap_st), Inches(2.3), w_st - Inches(0.2), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = f"STEP {num}"
        p0.font.name = FONT_BODY
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE
        p1 = tf.add_paragraph()
        p1.text = name
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_formatted_card(s4, Inches(0.8), Inches(4.1), Inches(3.72), Inches(2.7), "PRINCIPLE A", "Zero Framework Tourism", ["Do not add LangGraph, MCP, or Redis simply because they exist in AI news.", "Only add them when a concrete bottleneck demands them."], title_size=16, bullet_size=11.5)
    add_formatted_card(s4, Inches(4.8), Inches(4.1), Inches(3.72), Inches(2.7), "PRINCIPLE B", "Protect the Domain Core", ["Dolibarr CRM, PostgreSQL, and accounting remain the immutable source of truth.", "AI operates outside as an assistant, never as unconstrained master."], title_size=16, bullet_size=11.5)
    add_formatted_card(s4, Inches(8.8), Inches(4.1), Inches(3.72), Inches(2.7), "PRINCIPLE C", "Non-Destructive Upgrades", ["Tier 1 code is never discarded when upgrading to Tier 2.", "Each tier sits cleanly on top of the prior layer's data contracts."], title_size=16, bullet_size=11.5)

    # Slide 5: Commercial Packaging
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "04 // Commercial Strategy", "Selling Business Capability, Never Tech Stacks",
               "Clients pay for capability, reliability, autonomy, scale, and risk controls — never for underlying framework names.")
    add_footer(s5, 5, total_slides=19)
    pkg = [
        ("TIER 1 POSITIONING", "Lead Gen & Follow-Up System", [
            "Human-Directed Automation",
            "System does the tedious heavy lifting; human retains control.",
            "Saves 15+ hours/week for Sidy.",
            "Scrapes cafes, enriches profiles, drafts outreach, syncs Dolibarr CRM.",
            "100% brand-safe; zero hallucination risk."
        ]),
        ("TIER 2 POSITIONING", "AI Revenue Intelligence System", [
            "Human-Governed Intelligence",
            "System reasons, monitors ad performance, calculates refill schedules.",
            "All consequential actions evaluated against strict Policy Engines.",
            "Prevents cafe churn with automated Day-25 reorder prompts.",
            "Automates ad budget optimization within verified limits."
        ]),
        ("TIER 3 POSITIONING", "AI Revenue Operations Platform", [
            "Policy-Governed Autonomy",
            "Closed-loop commercial machine with multi-agent orchestration.",
            "Live customer reorder data directly trains marketing ad experiments.",
            "Scales Alandas to 100+ accounts across Germany with zero linear headcount growth.",
            "Complete operational independence for the founder."
        ])
    ]
    for i, (tag, title, bullets) in enumerate(pkg):
        add_formatted_card(s5, Inches(0.8) + i * (w + gap), Inches(2.0), w, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST), title_size=18, bullet_size=12)

    # Slide 6: Tier 1 Architecture
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "05 // Tier 1 Architecture", "Essential Revenue Automation Blueprint",
               "A clean, durable, production-grade foundation. Zero LangGraph, zero MCP, zero Redis. Pure engineering reliability.")
    add_footer(s6, 6, total_slides=19)
    add_formatted_card(s6, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "SYSTEM BLUEPRINT", "The Durable Pipeline", [
        "Temporal Workflow Engine: Manages execution durability and state recovery.",
        "Application Logic: Pure Python/TypeScript domain code.",
        "Deterministic Logic: Exact pricing, volume discount math, and ICP scoring.",
        "LLM Reasoning: Bounded web research and personalized message drafting.",
        "Direct APIs: Clean clients for Meta/OpenReply, Dolibarr CRM, and Shopify.",
        "PostgreSQL: Single system of record for leads, venues, and interaction logs."
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)
    add_formatted_card(s6, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "CAPABILITIES DELIVERED", "What Tier 1 Solves Today", [
        "Prospect Discovery: Scrapes German cafe hubs (Berlin, Munich, Hamburg, Frankfurt, NRW).",
        "Enrichment Waterfall: Pulls phone, email, seating count, and food/tea concept.",
        "Dolibarr CRM Creation: Pushes new qualified accounts into Dolibarr automatically.",
        "WhatsApp Order Parser: OCR extracts line items from paper note photos into draft invoices.",
        "Human Safety Gate: Sidy approves outreach drafts in 1 tap on WhatsApp before dispatch.",
        "Follow-Up Cadence: Automatic Day-4 tasting check-in after €19 sample box delivery."
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # Slide 7: Tier 1 Flow
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "06 // Tier 1 Execution Flow", "The Human-Directed Autonomy Model",
               "The safest entry model: Read ➔ Analyze ➔ Propose ➔ Human Approves ➔ Execute. 100% brand control.")
    s7.notes_slide.notes_text_frame.text = '''EXCALIDRAW STATE-MACHINE SPECIFICATION: tier1_essential_automation_flowchart.excalidraw\nArchitecture: Terminal Start (Raw Lead) -> Deduplication -> Circuit Breaker (Rate Limit) -> Section 5 TMG Legal Impressum -> 3-Stage Waterfall -> ICP Qualification Agent -> Personalization Agent -> Sidy WhatsApp 1-Tap Gate -> Dolibarr CRM Sync -> Temporal Day-4 & Day-25 Timers.\nInspect in browser: excalidraw_canvas_viewer.html#t1'''
    add_footer(s7, 7, total_slides=19)
    flow_steps = [
        ("01", "READ", "System detects inbound Instagram comment or scrapes target cafe on Google Maps."),
        ("02", "ANALYZE", "LLM extracts menu items, beverage prices, and seating capacity; calculates ICP score."),
        ("03", "PROPOSE", "Generates personalized outreach emphasizing €19 trial kit and 96% gross profit."),
        ("04", "APPROVE", "Sidy reviews on WhatsApp in 1 tap. Zero risk of bot hallucinating botanical claims."),
        ("05", "EXECUTE", "Temporal dispatches message, creates Dolibarr card, and schedules Day-4 follow-up.")
    ]
    w_fl = Inches(2.18)
    gap_fl = Inches(0.20)
    for i, (num, name, desc) in enumerate(flow_steps):
        create_card(s7, Inches(0.8) + i * (w_fl + gap_fl), Inches(2.0), w_fl, Inches(4.8), bg_color=COLOR_CARD_BG if i!=3 else COLOR_LIGHT_BG)
        tb = s7.shapes.add_textbox(Inches(1.0) + i * (w_fl + gap_fl), Inches(2.2), w_fl - Inches(0.4), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = f"STAGE {num}"
        p0.font.name = FONT_BODY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_OLIVE if i!=3 else COLOR_OCHRE
        p1 = tf.add_paragraph()
        p1.text = name
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(10)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(13)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    # Slide 8: Waterfall Enrichment Engine
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "07 // Tier 1 Lead Intelligence", "Waterfall Enrichment: Cheapest Tool First",
               "Each tool only gets what the last one missed: How Alandas achieves ~92% contact find rates with verified WhatsApp numbers at an 87% data cost reduction.")
    s8.notes_slide.notes_text_frame.text = '''EXCALIDRAW STATE-MACHINE SPECIFICATION: waterfall_enrichment_engine.excalidraw\nStage 0 (Section 5 TMG Impressum, 0 EUR, 48% find) -> Stage 1 (GitLeads bulk, 0.005 EUR, 24%) -> Stage 2 (Prospeo, 0.02 EUR, 18%) -> Stage 3 (LeadMagic Mobile, 0.05 EUR) -> Deliverability Gate (<1.5% bounce).\nInspect in browser: excalidraw_canvas_viewer.html#wf'''
    add_footer(s8, 8, total_slides=19)

    # 5 Waterfall Stage Cards across the top
    wf_stages = [
        ("STAGE 0 // €0.00", "§ 5 TMG Impressum", "Scrapes German legal notice (/impressum) for managing director & email.", "Finds 48% (480/1k)\n520 Passed Down ➔", COLOR_FOREST),
        ("STAGE 1 // €0.005", "GitLeads / Apollo", "Bulk database query applied only to the 520 missed cafe records.", "Finds 24% (+240)\n280 Passed Down ➔", COLOR_OLIVE),
        ("STAGE 2 // €0.02", "Prospeo / Origami", "Deep email scraper & social MX permutation for stubborn misses.", "Finds 18% (+180)\n~90% Total Email Find", COLOR_OCHRE),
        ("STAGE 3 // €0.05", "LeadMagic Mobile", "Direct mobile & WhatsApp lookup for found cafe owners and baristas.", "Finds 650 Mobiles\nEnables WhatsApp B2B", COLOR_OCHRE),
        ("VALIDATE // €0.002", "MillionVerifier", "Strict deliverability gate. Risky / Catch-All filtered out before outreach.", "< 1.5% Bounce Rate\nInbound Domain Safe", COLOR_FOREST)
    ]
    w_wf = Inches(2.20)
    gap_wf = Inches(0.18)
    for i, (tag, name, desc, stat, col) in enumerate(wf_stages):
        left_c = Inches(0.8) + i * (w_wf + gap_wf)
        create_card(s8, left_c, Inches(2.0), w_wf, Inches(2.6), bg_color=COLOR_CARD_BG)
        tb = s8.shapes.add_textbox(left_c + Inches(0.15), Inches(2.15), w_wf - Inches(0.30), Inches(2.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p0 = tf.paragraphs[0]
        p0.text = tag.upper()
        p0.font.name = FONT_BODY
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(3)
        p1 = tf.add_paragraph()
        p1.text = name
        p1.font.name = FONT_HEAD
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MAIN
        p1.space_after = Pt(5)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        p2.space_after = Pt(6)
        p3 = tf.add_paragraph()
        p3.text = stat
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10)
        p3.font.bold = True
        p3.font.color.rgb = col

    # Bottom 2 Cards: Unit Economics & German Legal Advantage
    add_formatted_card(s8, Inches(0.8), Inches(4.85), Inches(5.68), Inches(1.95), "UNIT ECONOMICS", "87% Data Acquisition Cost Reduction", [
        "Naive Flat Approach: $0.08 × 1,000 = $80.00 (High bounce risk & wasted spend).",
        "Waterfall Pipeline: €0 + €2.60 + €5.60 + €1.80 = €10.00 per 1,000 enriched leads.",
        "Net Result: 87% lower customer data cost while achieving ~92% verified contact rate."
    ], tag_color=COLOR_OLIVE, title_size=17, bullet_size=11)

    add_formatted_card(s8, Inches(6.85), Inches(4.85), Inches(5.68), Inches(1.95), "ARCHITECTURAL ADVANTAGE", "German § 5 TMG & Temporal Activity Isolation", [
        "§ 5 TMG Legal Impressum: German law requires commercial sites to publish owner name & email. Stage 0 resolves 48% of leads for €0.",
        "Temporal Durability: Each stage runs as an isolated activity with exponential backoff. If Apollo times out, workflow cascades to Prospeo.",
        "Reputation Defense: MillionVerifier keeps sender bounce rate < 1.5%, protecting sending domains from Google Workspace blacklisting."
    ], tag_color=COLOR_OCHRE, title_size=17, bullet_size=11)

    # Slide 9: Tier 2 Architecture
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "08 // Tier 2 Architecture", "Professional Revenue Intelligence Blueprint",
               "Introducing durable domain workflows, structured Policy Engines, Decision Contracts, and audit trails.")
    add_footer(s9, 9, total_slides=19)
    add_formatted_card(s9, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "SYSTEM BLUEPRINT", "The Governed Architecture", [
        "Temporal Domain Workflows: Explicit services for Acquisition, Marketing & RevOps.",
        "Domain Logic Layer: Decouples business rules from external transport APIs.",
        "Policy Engine: Mathematical verification of budgets, pricing, and messaging limits.",
        "Decision Contracts: Typed JSON contracts required for all AI recommendations.",
        "Post-Action Verification: System re-queries external APIs to verify state change.",
        "PostgreSQL + Audit Traces: Full OpenTelemetry tracing across all operations."
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)
    add_formatted_card(s9, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "THE ARCHITECTURAL LEAP", "From Automation to Governed Intelligence", [
        "In Tier 1, Temporal executes commands. In Tier 2, the system must justify decisions before execution.",
        "Policy Engine: Independent rules governing budget, pricing, discounts, and cadence.",
        "Decision Contracts: Every AI recommendation is validated against schemas before execution.",
        "Selective LangGraph: Bounded reasoning graphs used strictly for complex evaluations (e.g. ad creative analysis), never for the whole app.",
        "Auditability: In any dispute, the customer has an exact chronological record of every AI decision."
    ], tag_color=COLOR_OCHRE, title_size=20, bullet_size=12.5)

    # Slide 10: Tier 2 in Action
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "09 // Tier 2 Governance in Action", "The Decision Contract Walkthrough",
               "Example: AI recommends a 30% Meta Ad budget increase. How the system governs this safely.")
    s10.notes_slide.notes_text_frame.text = '''EXCALIDRAW STATE-MACHINE SPECIFICATION: tier2_governed_intelligence_flowchart.excalidraw\nSignal Ingest -> LangGraph Creative Loop -> Typed Decision Contract -> Schema Gate -> Policy Engine Check -> Budget Delta Gate (>5 EUR requires Sidy 1-tap sign-off) -> Meta API Dispatch -> Post-Action Query Verification -> Immutable PostgreSQL Audit Ledger.\nInspect in browser: excalidraw_canvas_viewer.html#t2'''
    add_footer(s10, 10, total_slides=19)
    add_formatted_card(s10, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "8-STAGE GOVERNANCE GATE", "Executing +30% Ad Budget Increase", [
        "1. AI Recommendation: 'Increase Berlin Brunch Ad budget from €30 to €39/day (+30%).'",
        "2. Validity Check: Is campaign ID active? Does the ad set exist?",
        "3. Eligibility Check: Has campaign run > 7 days? Is ROAS > 3.0x? (Yes: 4.2x).",
        "4. Policy Evaluation: Does €39 exceed the daily ceiling (€50)? (Compliant).",
        "5. Approval Threshold: Does budget delta > €5 require human sign-off? (Policy: YES).",
        "6. Human Approval: Sidy receives 1-tap notification: [Approve +€9/day].",
        "7. Execute & Verify: Meta API called; system re-queries Meta to confirm new budget = €39.00.",
        "8. Audit Logging: Immutable record written with reasoning, timestamp, and Sidy's ID."
    ], tag_color=COLOR_OCHRE, title_size=18, bullet_size=11.5)
    add_formatted_card(s10, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "COMMERCIAL VALUE", "What the Customer Is Actually Paying For", [
        "Zero Runaway Spend: An AI bug or hallucination can never drain the customer's bank account or ad budget.",
        "Zero Pricing Leaks: B2B wholesale volume discounts follow strict mathematical tables, not model whims.",
        "Regulatory Compliance: Strict policy checks guarantee botanical and organic labeling compliance under German food regulations.",
        "Complete Auditability: Exact chronological record of every AI decision for investors and accountants."
    ], tag_color=COLOR_OLIVE, title_size=18, bullet_size=12)

    # Slide 11: Tier 3 Architecture
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10 // Tier 3 Architecture", "Autonomous Revenue Platform Blueprint",
               "When commercial scale reaches 100+ accounts, the system transitions into an autonomous closed-loop revenue engine.")
    add_footer(s11, 11, total_slides=19)
    add_formatted_card(s11, Inches(0.8), Inches(2.0), Inches(5.68), Inches(4.8), "SYSTEM BLUEPRINT", "The Autonomous Platform", [
        "Temporal Runtime & Event Bus: Durable event backbone coordinating all domain agents.",
        "Domain Specialist Agents: Dedicated agents for Acquisition, Creative/Ads, and RevOps.",
        "Shared Revenue State: Central real-time graph of customer accounts, consumption & LTV.",
        "Policy Engine & Enterprise RAG: Ingestion of blend sensory sheets, cafe notes & market trends.",
        "MCP Capability Layer: Standardized protocol boundaries for tool invocation across services.",
        "Closed-Loop Learning: Automated feedback connecting customer refills back into ad bidding."
    ], tag_color=COLOR_OLIVE, title_size=20, bullet_size=12.5)
    add_formatted_card(s11, Inches(6.85), Inches(2.0), Inches(5.68), Inches(4.8), "EARNED COMPLEXITY", "When Is Tier 3 Justified?", [
        "Cross-Domain Signals: Cafe reorder frequency directly triggers creative testing on Meta Ads without human intervention.",
        "MCP Dynamic Capabilities: Agents dynamically discover tools and query inventory, CRM, and logistics via standardized protocol boundaries.",
        "Continuous Experimentation: System formulates hypotheses, executes test campaigns, and measures LTV impact.",
        "True Scale: Operates 200+ partner accounts across multiple countries with zero additional administrative personnel."
    ], tag_color=COLOR_FOREST, title_size=20, bullet_size=12.5)

    # Slide 12: Tier 3 Flywheel
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "11 // Tier 3 Operational Flywheel", "The Closed-Loop Commercial Flywheel",
               "Connecting top-of-funnel acquisition directly to post-purchase retention and lifetime value in a continuous feedback loop.")
    s12.notes_slide.notes_text_frame.text = '''EXCALIDRAW STATE-MACHINE SPECIFICATION: tier3_autonomous_platform_flowchart.excalidraw\nCommercial Event Bus -> Shared Revenue State Graph -> Multi-Agent Domain Team (Acquisition, Creative, RevOps) -> Continuous Experimentation -> Automated Circuit Breakers -> MCP Dynamic Tool Layer -> Closed-Loop Flywheel.\nInspect in browser: excalidraw_canvas_viewer.html#t3'''
    add_footer(s12, 12, total_slides=19)
    flywheel = [
        ("STAGE 01", "Market Signals", ["Scrapes German dining clusters", "Tracks Instagram engagement", "Identifies active beverage buyers"]),
        ("STAGE 02", "€19 Trial Box", ["Automated qualification routes heavy borosilicate teapot", "Verified cafe baristas receive kit", "100% credited against Starter Crate"]),
        ("STAGE 03", "Starter Crate", ["€249 Starter Crate deployed", "Turnkey counter Teebar installed", "Barista brewing cheat sheets automated"]),
        ("STAGE 04", "Predictive Refills", ["Day-25 consumption alerts", "1-click WhatsApp reorders", "Automated Dolibarr PDF invoicing"])
    ]
    w_fw = Inches(2.72)
    gap_fw = Inches(0.28)
    for i, (tag, title, bullets) in enumerate(flywheel):
        add_formatted_card(s12, Inches(0.8) + i * (w_fw + gap_fw), Inches(2.0), w_fw, Inches(3.2), tag, title, bullets, title_size=16, bullet_size=11)

    create_card(s12, Inches(0.8), Inches(5.4), Inches(11.733), Inches(1.4), bg_color=COLOR_LIGHT_BG)
    tb = s12.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.333), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "THE AUTONOMOUS FEEDBACK LOOP // WHAT MAKES IT FLYWHEEL"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_OLIVE
    p1 = tf.add_paragraph()
    p1.text = "Actual cafe replenishment rates feed back into the Ads Agent. If brunch cafes in Munich reorder Earl Grey 2x faster than average, the system automatically writes new ad copy, allocates budget to Munich brunch clusters, and tests new creative hypotheses without human intervention."
    p1.font.name = FONT_BODY
    p1.font.size = Pt(12)
    p1.font.color.rgb = COLOR_TEXT_MAIN

    # Slide 13: Framework Comparison Matrix
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "12 // System Design Benchmark", "Master Architectural Comparison Matrix",
               "Clear component separation across tiers: Customer capability scales without unnecessary infrastructure bloat.")
    add_footer(s13, 13, total_slides=19)
    add_formatted_card(s13, Inches(0.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 1 // ESSENTIAL", "Durable Automation", [
        "Runtime: Temporal + Python/TS",
        "Orchestration: Temporal Workflows",
        "Intelligence: Direct LLM API",
        "Safety: Human Approval Gate",
        "Integrations: Direct REST APIs",
        "Database: PostgreSQL Core",
        "Caching / Bus: None (Zero Bloat)",
        "Audit: PostgreSQL Ledgers",
        "Commercial Value: Saves 15h/week"
    ], tag_color=COLOR_OLIVE, title_size=17, bullet_size=11.5)
    add_formatted_card(s13, Inches(4.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 2 // PROFESSIONAL", "Governed Intelligence", [
        "Runtime: Temporal Runtime",
        "Orchestration: Temporal + Selective LangGraph",
        "Intelligence: Policy Engines + Schemas",
        "Safety: Decision Contracts + Human Gate",
        "Integrations: Direct APIs + Verifiers",
        "Database: PostgreSQL + Audit Store",
        "Caching / Bus: None needed at this scale",
        "Audit: OpenTelemetry Traces",
        "Commercial Value: Churn prevention"
    ], tag_color=COLOR_OCHRE, title_size=17, bullet_size=11.5)
    add_formatted_card(s13, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 3 // AUTONOMOUS", "Autonomous Platform", [
        "Runtime: Temporal Platform",
        "Orchestration: Domain Agents + Temporal",
        "Intelligence: Enterprise RAG + Learning",
        "Safety: Automated Circuit Breakers",
        "Integrations: Model Context Protocol (MCP)",
        "Database: PostgreSQL + Shared State Graph",
        "Caching / Bus: Event PubSub Layer",
        "Audit: Comprehensive System Telemetry",
        "Commercial Value: Enterprise autonomy"
    ], tag_color=COLOR_FOREST, title_size=17, bullet_size=11.5)

    # Slide 14: Autonomy Spectrum
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "13 // Operational Governance", "The Autonomy Spectrum & Blast Radius Containment",
               "The difference between tiers is not merely more code. It is the structured management of risk and blast radius across the business.")
    add_footer(s14, 14, total_slides=19)
    add_formatted_card(s14, Inches(0.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 1 // ZERO BLAST RADIUS", "Human-Directed", [
        "Machine only reads public data & gathers facts.",
        "Every prospect message, sample box dispatch, and proposal requires human click.",
        "Zero risk of bot hallucinating botanical claims or unauthorized pricing.",
        "Safe for early-stage founders and fragile brand trust."
    ], tag_color=COLOR_OLIVE, title_size=17, bullet_size=12)
    add_formatted_card(s14, Inches(4.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 2 // STRICT BOUNDS", "Human-Governed", [
        "Standard repetitive tasks execute autonomously (e.g. Day-20 refill check-in).",
        "High-risk actions (pricing, discounts, budget delta > €5) trigger Decision Contracts.",
        "Human approval required for any action outside policy bounds.",
        "High leverage with guaranteed safety nets."
    ], tag_color=COLOR_OCHRE, title_size=17, bullet_size=12)
    add_formatted_card(s14, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.8), "TIER 3 // MATHEMATICALLY BOUND", "Policy-Governed", [
        "Machine autonomously shifts ad spend, rotates blends, and optimizes schedules.",
        "Protected by automated circuit breakers: any sudden metric spike halts system.",
        "Human executive acts as supervisor reviewing weekly performance digests.",
        "Massive operational scale with automated anomaly defense."
    ], tag_color=COLOR_FOREST, title_size=17, bullet_size=12)

    # Slide 15: Instagram Architecture
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "14 // Omnichannel Acquisition", "Instagram as a First-Class Architecture Channel",
               "Instagram is an essential acquisition channel and signal source across all three tiers — not an afterthought.")
    add_footer(s15, 15, total_slides=19)
    ig_roles = [
        ("ROLE 01", "Outbound Prospecting", ["Identifies specialty brunch cafes", "Analyzes feed interior aesthetic", "Pre-qualifies tea menu fit"]),
        ("ROLE 02", "OpenReply Inbound", ["Barista comments 'TEABAR' on reel", "Triggers instant qualification DM", "Sends €19 trial kit link in 60s"]),
        ("ROLE 03", "Marketing Signals", ["Tracks likes & comments on tea reels", "Identifies active beverage directors", "Enriches intent in Dolibarr CRM"]),
        ("ROLE 04", "Paid Acquisition", ["Meta Ads target cafe owners directly", "Drives to 1-tap WhatsApp chat", "Captures pre-paid sample orders"])
    ]
    w_ig = Inches(2.72)
    gap_ig = Inches(0.28)
    for i, (tag, title, bullets) in enumerate(ig_roles):
        add_formatted_card(s15, Inches(0.8) + i * (w_ig + gap_ig), Inches(2.0), w_ig, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE if i%2==0 else COLOR_OCHRE, title_size=17, bullet_size=12)

    # Slide 16: Instagram Across Tiers
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "15 // Channel Evolution", "How Instagram Matures Across Tiers",
               "Tier 1 has a complete, working comment-to-DM loop. Higher tiers add intelligence, governance, and cross-channel optimization.")
    add_footer(s16, 16, total_slides=19)
    table_shape = s16.shapes.add_table(6, 4, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(2.844)
    table.columns[2].width = Inches(2.844)
    table.columns[3].width = Inches(2.844)

    ig_matrix = [
        ["Dimension", "Tier 1 // Essential", "Tier 2 // Professional", "Tier 3 // Autonomous"],
        ["Comment ➔ DM", "OpenReply Keyword Triggers", "OpenReply + Context Routing", "Dynamic Intent Extraction"],
        ["Lead Qualification", "Standard 60-Sec Form", "Dynamic Gated Qualification", "Real-Time Venue Scoring"],
        ["Dolibarr CRM Sync", "Immediate Lead Card", "Lead Card + Social Score", "Full Omnichannel Identity"],
        ["Outreach Messaging", "AI-Drafted ➔ Human Approves", "Pre-Approved Policy Templates", "Autonomous Dynamic Copy"],
        ["Ad Spend Feedback", "Manual Ad Optimization", "Policy Engine Budgets (±20%)", "Closed-Loop Attribution"]
    ]
    for row_idx, row_data in enumerate(ig_matrix):
        for col_idx, cell_value in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.text = cell_value
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(11.5 if row_idx > 0 else 12)
            p.font.bold = (row_idx == 0 or col_idx == 0)
            if row_idx == 0:
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_OLIVE
            else:
                p.font.color.rgb = COLOR_TEXT_MAIN
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_CARD_BG if row_idx % 2 == 1 else COLOR_LIGHT_BG

    # Slide 17: Tech Stack Evolution
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "16 // Lifecycle Engineering", "Evolving the Architecture Without Rewriting",
               "Every tier is additive: Higher tiers wrap around lower tiers rather than replacing them.")
    add_footer(s17, 17, total_slides=19)
    w_up = Inches(3.7)
    gap_up = Inches(0.316)
    upgrade_layers = [
        ("LAYER 1 // TIER 1 FOUNDATION", "Essential Automation Core", [
            "Temporal Workflow Engine",
            "Application Logic (Python / TS)",
            "PostgreSQL Database",
            "Dolibarr CRM API Client",
            "Shopify Store REST Client",
            "Meta / Instagram API Client",
            "Direct LLM API Wrapper",
            "Status: Remains untouched in Tier 2."
        ]),
        ("LAYER 2 // TIER 2 ADDITIONS", "Governed Intelligence Layer", [
            "Policy Engine Framework",
            "Decision Contract Validator",
            "OpenTelemetry Tracing Exporter",
            "Selective LangGraph Engine",
            "Post-Action Verification Engine",
            "Audit Trail Storage & Ledger",
            "Status: Wraps around Tier 1 without altering database models."
        ]),
        ("LAYER 3 // TIER 3 ADDITIONS", "The Autonomous Flywheel", [
            "Domain Specialist Agents",
            "Model Context Protocol (MCP) Tools",
            "Shared Revenue State & Event PubSub",
            "Cross-Domain Feedback Engine",
            "Continuous Experimentation Harness",
            "Status: Adds autonomous loops over Tier 2 governance."
        ])
    ]
    for i, (tag, title, bullets) in enumerate(upgrade_layers):
        add_formatted_card(s17, Inches(0.8) + i * (w_up + gap_up), Inches(2.0), w_up, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST), title_size=18, bullet_size=12)

    # Slide 18: Deep-Dive Tradeoffs
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "17 // Engineering Defense", "System Design Tradeoff Analysis: The 'Why'",
               "Every decision has a cost. A senior engineer is defined by the tradeoffs they can explicitly defend.")
    add_footer(s18, 18, total_slides=19)
    add_formatted_card(s18, Inches(0.8), Inches(2.0), Inches(5.68), Inches(2.3), "DECISION 01", "Temporal vs. n8n", [
        "Tradeoff: Temporal requires writing code; n8n has a visual UI.",
        "Defense: Revenue operations require true durability. An unhandled error in n8n drops state. Temporal's append-only event log guarantees zero lost invoices and deterministic replay."
    ], tag_color=COLOR_OLIVE, title_size=16, bullet_size=11)
    add_formatted_card(s18, Inches(6.85), Inches(2.0), Inches(5.68), Inches(2.3), "DECISION 02", "Direct APIs vs. MCP in Tiers 1–2", [
        "Tradeoff: Direct API clients are tightly coupled; MCP standardizes tool protocols.",
        "Defense: Direct APIs have zero protocol overhead, simpler debugging, and strict type safety. MCP adds value in Tier 3 dynamic discovery, but is unnecessary overhead in Tier 1."
    ], tag_color=COLOR_OCHRE, title_size=16, bullet_size=11)
    add_formatted_card(s18, Inches(0.8), Inches(4.5), Inches(5.68), Inches(2.3), "DECISION 03", "PostgreSQL vs. Event Streaming (Kafka)", [
        "Tradeoff: Postgres is relational; Kafka handles massive distributed streaming.",
        "Defense: Alandas' target is 100 accounts (~500 transactions/mo). PostgreSQL ACID transactions and JSONB state easily scale to 50,000 accounts without distributed Kafka complexity."
    ], tag_color=COLOR_FOREST, title_size=16, bullet_size=11)
    add_formatted_card(s18, Inches(6.85), Inches(4.5), Inches(5.68), Inches(2.3), "DECISION 04", "Selective LangGraph vs. Whole-App Graphs", [
        "Tradeoff: LangGraph gives cyclic graph control; Temporal gives durable execution.",
        "Defense: LangGraph is brilliant for bounded multi-turn reflection (e.g., evaluating an ad draft). Temporal acts as the parent orchestrator; LangGraph runs inside an Activity."
    ], tag_color=COLOR_OLIVE, title_size=16, bullet_size=11)

    # Slide 19: Strategic Roadmap
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "18 // Execution Roadmap", "The Alandas Roadmap: Starting Tier 1 Today",
               "Stabilize operations at Tier 1 immediately, scale to 50 accounts with Tier 2, and unlock 100 accounts full-time freedom with Tier 3.")
    add_footer(s19, 19, total_slides=19)
    roadmap = [
        ("MONTHS 1–3 // START TODAY", "Sprint 1: Tier 1 Launch", [
            "Target: 25 ➔ 40 Active Accounts (€5k/mo)",
            "Stabilize Dolibarr CRM with automated daily cloud backups.",
            "Restore Hermes AI WhatsApp order parsing with deterministic rules.",
            "Deploy OpenReply Instagram comment-to-DM loop on B2B page.",
            "Standardize €19 discovery kit featuring shatter-resistant teapot.",
            "Sidy handles 10–20 WhatsApp chats daily with AI drafting."
        ]),
        ("MONTHS 4–6 // SCALING UP", "Sprint 2: Tier 2 Governance", [
            "Target: 40 ➔ 70 Active Accounts (€12k/mo)",
            "Deploy Policy Engine & Decision Contracts for Meta ad spend.",
            "Automate Day-25 predictive refills via Dolibarr WhatsApp alerts.",
            "Add OpenTelemetry tracing & audit log for all AI decisions.",
            "Deploy barista table talkers and QR counter refill portals.",
            "Sidy reduces administrative hours to < 4 hours/week."
        ]),
        ("MONTHS 7–12 // FULL FREEDOM", "Sprint 3: Tier 3 Platform", [
            "Target: 100 Active Accounts (€20k–€30k/mo)",
            "Closed-loop revenue flywheel: LTV data drives Meta ad creative.",
            "MCP capability layer connects multi-city logistics and warehouse.",
            "Multi-agent coordination across Germany, Austria & Switzerland.",
            "Predictable recurring gross margin of €15,000–€30,000/month.",
            "Sidy quits Swiss job to be his own boss 100% full-time."
        ])
    ]
    for i, (tag, title, bullets) in enumerate(roadmap):
        add_formatted_card(s19, Inches(0.8) + i * (w_up + gap_up), Inches(2.0), w_up, Inches(4.8), tag, title, bullets, tag_color=COLOR_OLIVE if i==0 else (COLOR_OCHRE if i==1 else COLOR_FOREST), title_size=18, bullet_size=11.5)

    prs.save(output_pptx_path)
    print(f"[SUCCESS] Native PowerPoint Presentation generated at: {output_pptx_path}")

if __name__ == "__main__":
    html_path = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\Alandas_Tiered_Architecture_Presentation.html"
    pptx_path = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\Alandas_Tiered_Architecture_System.pptx"
    build_html_presentation(html_path)
    build_pptx_presentation(pptx_path)
