"""
Pure Python SVG Exporter for Excalidraw Documents
Converts any .excalidraw JSON file into a standalone, beautiful SVG with authentic hand-drawn styling and Google Fonts.
"""

import json
import math
import os

def excalidraw_to_svg(doc, width, height, output_path):
    elements = doc.get("elements", [])
    
    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    # Defs: Hand-drawn filter & Fonts
    svg_parts.append('''
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
''')

    for el in elements:
        t = el.get("type")
        x = el.get("x", 0)
        y = el.get("y", 0)
        w = el.get("width", 0)
        h = el.get("height", 0)
        stroke = el.get("strokeColor", "#181916")
        fill = el.get("backgroundColor", "transparent")
        sw = el.get("strokeWidth", 2)
        
        if t == "rectangle":
            rx = 12 if el.get("roundness") else 0
            svg_parts.append(f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" filter="url(#handDrawn)" />')
            
        elif t == "ellipse":
            cx = x + w / 2
            cy = y + h / 2
            rx = w / 2
            ry = h / 2
            svg_parts.append(f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" filter="url(#handDrawn)" />')
            
        elif t == "diamond":
            mid_x = x + w / 2
            mid_y = y + h / 2
            points = f"{mid_x},{y} {x+w},{mid_y} {mid_x},{y+h} {x},{mid_y}"
            svg_parts.append(f'  <polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" filter="url(#handDrawn)" />')
            
        elif t == "text":
            font_size = el.get("fontSize", 16)
            font_family_code = el.get("fontFamily", 1)
            font_family = "JetBrains Mono, monospace" if font_family_code == 3 else ("Caveat, cursive, sans-serif" if font_family_code == 1 else "Plus Jakarta Sans, sans-serif")
            font_weight = "700" if font_size > 17 else "600"
            text_align = el.get("textAlign", "center")
            anchor = "middle" if text_align == "center" else "start"
            text_x = x + w / 2 if text_align == "center" else x
            text_y = y + font_size
            
            raw_text = el.get("text", "")
            lines = raw_text.split("\n")
            
            svg_parts.append(f'  <text x="{text_x}" y="{text_y}" fill="{stroke}" font-size="{font_size}" font-family="{font_family}" font-weight="{font_weight}" text-anchor="{anchor}">')
            for idx, line in enumerate(lines):
                escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                dy = 0 if idx == 0 else int(font_size * 1.32)
                svg_parts.append(f'    <tspan x="{text_x}" dy="{dy}">{escaped}</tspan>')
            svg_parts.append('  </text>')
            
        elif t == "arrow":
            points = el.get("points", [[0, 0], [w, h]])
            start_x = x
            start_y = y
            end_x = x + points[1][0]
            end_y = y + points[1][1]
            
            svg_parts.append(f'  <g filter="url(#handDrawn)">')
            svg_parts.append(f'    <line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" stroke="{stroke}" stroke-width="{sw}" />')
            
            angle = math.atan2(end_y - start_y, end_x - start_x)
            head_len = 13
            p1x = end_x - head_len * math.cos(angle - math.pi / 6)
            p1y = end_y - head_len * math.sin(angle - math.pi / 6)
            p2x = end_x - head_len * math.cos(angle + math.pi / 6)
            p2y = end_y - head_len * math.sin(angle + math.pi / 6)
            
            head_pts = f"{end_x},{end_y} {p1x},{p1y} {p2x},{p2y}"
            svg_parts.append(f'    <polygon points="{head_pts}" fill="{stroke}" />')
            svg_parts.append('  </g>')

    svg_parts.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"[SUCCESS] Exported SVG: {output_path}")

def main():
    base_dir = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas"
    
    files = [
        ("tier1_essential_automation_flowchart.excalidraw", "tier1_flowchart.svg", 1000, 2340),
        ("tier2_governed_intelligence_flowchart.excalidraw", "tier2_flowchart.svg", 1000, 1600),
        ("tier3_autonomous_platform_flowchart.excalidraw", "tier3_flowchart.svg", 1000, 1300),
        ("waterfall_enrichment_engine.excalidraw", "waterfall_enrichment.svg", 1320, 740),
        ("alandas_self_healing_revenue_pipeline.excalidraw", "alandas_revenue_flowchart.svg", 1000, 2340)
    ]
    
    for exc_name, svg_name, w, h in files:
        exc_path = os.path.join(base_dir, exc_name)
        svg_path = os.path.join(base_dir, svg_name)
        if os.path.exists(exc_path):
            with open(exc_path, "r", encoding="utf-8") as f:
                doc = json.load(f)
            excalidraw_to_svg(doc, w, h, svg_path)

if __name__ == "__main__":
    main()
