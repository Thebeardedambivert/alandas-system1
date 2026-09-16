"""
Build Master Excalidraw Suite for All 3 Tiers & Update Interactive Viewer
Outputs:
- tier1_essential_automation_flowchart.excalidraw
- tier2_governed_intelligence_flowchart.excalidraw
- tier3_autonomous_platform_flowchart.excalidraw
- waterfall_enrichment_engine.excalidraw
- tiered_revenue_architecture.excalidraw
- All 5 standalone SVGs
- excalidraw_canvas_viewer.html (with 5 tabs, one for each tier + waterfall + 3-tier comparison)
"""

import json
import os
from generate_tiered_flowcharts_excalidraw import (
    build_tier1_flowchart,
    build_tier2_flowchart,
    build_tier3_flowchart
)
from generate_excalidraw import (
    build_waterfall_excalidraw,
    build_tiered_architecture_excalidraw
)
from export_excalidraw_svg import excalidraw_to_svg

def main():
    base_dir = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas"
    
    # 1. Build all docs
    t1_doc, h1 = build_tier1_flowchart()
    t2_doc, h2 = build_tier2_flowchart()
    t3_doc, h3 = build_tier3_flowchart()
    wf_doc = build_waterfall_excalidraw()
    comp_doc = build_tiered_architecture_excalidraw()
    
    # Save .excalidraw files
    docs = [
        ("tier1_essential_automation_flowchart.excalidraw", t1_doc, 1000, 2340),
        ("tier2_governed_intelligence_flowchart.excalidraw", t2_doc, 1000, 1600),
        ("tier3_autonomous_platform_flowchart.excalidraw", t3_doc, 1000, 1300),
        ("waterfall_enrichment_engine.excalidraw", wf_doc, 1320, 740),
        ("tiered_revenue_architecture.excalidraw", comp_doc, 1300, 800)
    ]
    
    for filename, doc, w, h in docs:
        filepath = os.path.join(base_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2)
        print(f"[SUCCESS] Saved: {filepath}")
        
        # Export SVG
        svg_name = filename.replace(".excalidraw", ".svg")
        svg_path = os.path.join(base_dir, svg_name)
        excalidraw_to_svg(doc, w, h, svg_path)

    # 2. Build 5-Tab Interactive Viewer HTML
    viewer_path = os.path.join(base_dir, "excalidraw_canvas_viewer.html")
    
    t1_json = json.dumps(t1_doc)
    t2_json = json.dumps(t2_doc)
    t3_json = json.dumps(t3_doc)
    wf_json = json.dumps(wf_doc)
    comp_json = json.dumps(comp_doc)
    
    viewer_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Alandas Architecture Canvas — Excalidraw Tiered Flowcharts</title>
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
      padding: 10px 24px;
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
      font-size: 16px;
      font-weight: 700;
      color: #FFF;
    }}
    .nav-tabs {{
      display: flex;
      gap: 5px;
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
      font-size: 13px;
      padding: 6px 14px;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }}
    .tab-btn.active {{
      background: var(--olive);
      color: #FFF;
    }}
    .tab-btn.ochre.active {{
      background: var(--ochre);
      color: #FFF;
    }}
    .tab-btn.forest.active {{
      background: var(--forest);
      color: #FFF;
    }}
    .actions {{
      display: flex;
      gap: 8px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #282C25;
      color: #E8E6DF;
      border: 1px solid var(--border);
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      padding: 6px 12px;
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
      padding: 24px;
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

    footer {{
      background: #181B16;
      border-top: 1px solid var(--border);
      padding: 8px 24px;
      font-size: 12px;
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
    <button class="tab-btn active" id="tabT1" onclick="switchTab('t1')">Tier 1: Automation Flow</button>
    <button class="tab-btn ochre" id="tabT2" onclick="switchTab('t2')">Tier 2: Governed Decision Flow</button>
    <button class="tab-btn forest" id="tabT3" onclick="switchTab('t3')">Tier 3: Autonomous Flywheel</button>
    <button class="tab-btn" id="tabWf" onclick="switchTab('wf')">Waterfall Enrichment Pipeline</button>
    <button class="tab-btn" id="tabComp" onclick="switchTab('comp')">3-Tier Comparison Matrix</button>
  </div>

  <div class="actions">
    <a class="btn" id="btnDownload" href="#" download="tier1_essential_automation_flowchart.excalidraw">Download .excalidraw</a>
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
  <div id="footerNotice"><strong>Tier 1 Architecture:</strong> Human-directed durable execution with 5-stage waterfall & Sidy 1-tap WhatsApp approval gate.</div>
  <div>Alandas Tea Berlin  •  Architecture by Cyril Uzochukwu</div>
</footer>

<script>
  const t1Data = {t1_json};
  const t2Data = {t2_json};
  const t3Data = {t3_json};
  const wfData = {wf_json};
  const compData = {comp_json};

  let currentTab = 't1';

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
    const tabs = ['t1', 't2', 't3', 'wf', 'comp'];
    tabs.forEach(t => {{
      const btn = document.getElementById('tab' + t.charAt(0).toUpperCase() + t.slice(1));
      if (btn) btn.classList.remove('active');
    }});

    const activeBtn = document.getElementById('tab' + tab.charAt(0).toUpperCase() + tab.slice(1));
    if (activeBtn) activeBtn.classList.add('active');

    const btnDown = document.getElementById('btnDownload');
    const svgStage = document.getElementById('svgStage');
    const viewportArea = document.getElementById('viewportArea');
    const footerNotice = document.getElementById('footerNotice');

    viewportArea.scrollTop = 0;

    if (tab === 't1') {{
      svgStage.setAttribute('viewBox', '0 0 1000 2340');
      svgStage.setAttribute('width', '1000');
      svgStage.setAttribute('height', '2340');
      renderExcalidrawToSvg(t1Data, svgStage);
      btnDown.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(t1Data, null, 2));
      btnDown.download = 'tier1_essential_automation_flowchart.excalidraw';
      footerNotice.innerHTML = '<strong>Tier 1 Architecture:</strong> Human-directed durable execution with 5-stage waterfall & Sidy 1-tap WhatsApp approval gate.';
    }} else if (tab === 't2') {{
      svgStage.setAttribute('viewBox', '0 0 1000 1620');
      svgStage.setAttribute('width', '1000');
      svgStage.setAttribute('height', '1620');
      renderExcalidrawToSvg(t2Data, svgStage);
      btnDown.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(t2Data, null, 2));
      btnDown.download = 'tier2_governed_intelligence_flowchart.excalidraw';
      footerNotice.innerHTML = '<strong>Tier 2 Architecture:</strong> Policy engines, typed decision contracts, delta thresholds & post-action verification query.';
    }} else if (tab === 't3') {{
      svgStage.setAttribute('viewBox', '0 0 1000 1320');
      svgStage.setAttribute('width', '1000');
      svgStage.setAttribute('height', '1320');
      renderExcalidrawToSvg(t3Data, svgStage);
      btnDown.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(t3Data, null, 2));
      btnDown.download = 'tier3_autonomous_platform_flowchart.excalidraw';
      footerNotice.innerHTML = '<strong>Tier 3 Architecture:</strong> Multi-agent coordination via Temporal, MCP standardized tools, circuit breakers & closed-loop flywheel.';
    }} else if (tab === 'wf') {{
      svgStage.setAttribute('viewBox', '0 0 1320 740');
      svgStage.setAttribute('width', '1320');
      svgStage.setAttribute('height', '740');
      renderExcalidrawToSvg(wfData, svgStage);
      btnDown.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(wfData, null, 2));
      btnDown.download = 'waterfall_enrichment_engine.excalidraw';
      footerNotice.innerHTML = '<strong>Waterfall Pipeline:</strong> Cheapest tool first (Impressum ➔ GitLeads ➔ Prospeo ➔ LeadMagic ➔ MillionVerifier) saving 87% in data costs.';
    }} else {{
      svgStage.setAttribute('viewBox', '0 0 1300 800');
      svgStage.setAttribute('width', '1300');
      svgStage.setAttribute('height', '800');
      renderExcalidrawToSvg(compData, svgStage);
      btnDown.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(compData, null, 2));
      btnDown.download = 'tiered_revenue_architecture.excalidraw';
      footerNotice.innerHTML = '<strong>3-Tier Maturity Model:</strong> Non-destructive evolution from durable automation to governed intelligence to autonomous platform.';
    }}
  }}

  // Initial load
  switchTab('t1');
</script>
</body>
</html>
"""
    with open(viewer_path, "w", encoding="utf-8") as f:
        f.write(viewer_html)
    print(f"[SUCCESS] Multi-tier interactive viewer generated at: {viewer_path}")

if __name__ == "__main__":
    main()
