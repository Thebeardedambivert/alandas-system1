import os
import subprocess

def render_all():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    tasks = [
        {
            "name": "mockup_whatsapp_tier1",
            "html": os.path.join(assets_dir, "mockup_whatsapp_tier1.html"),
            "out": os.path.join(assets_dir, "mockup_whatsapp_tier1.png"),
            "width": 640,
            "height": 940
        },
        {
            "name": "mockup_dolibarr_crm",
            "html": os.path.join(assets_dir, "mockup_dolibarr_crm.html"),
            "out": os.path.join(assets_dir, "mockup_dolibarr_crm.png"),
            "width": 880,
            "height": 680
        }
    ]

    for t in tasks:
        url = "file:///" + t["html"].replace("\\", "/")
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={t['width']},{t['height']}",
            f"--screenshot={t['out']}",
            url
        ]
        print(f"Rendering {t['name']}...")
        subprocess.run(cmd, check=True)
        print(f"Generated {t['out']} (size: {os.path.getsize(t['out'])} bytes)")

    # Render SVGs via helper HTML wrapper
    svgs = [
        ("tier1_flowchart.svg", "tier1_flowchart.png", 1400, 2400),
        ("tier2_flowchart.svg", "tier2_flowchart.png", 1400, 1500),
        ("tier3_flowchart.svg", "tier3_flowchart.png", 1400, 1200),
    ]

    for svg_file, png_file, w, h in svgs:
        svg_path = os.path.join(base_dir, svg_file)
        png_path = os.path.join(assets_dir, png_file)
        wrapper_html = os.path.join(assets_dir, f"temp_{svg_file}.html")
        
        with open(svg_path, "r", encoding="utf-8") as sf:
            svg_content = sf.read()
            
        html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #F9F7F2; display: flex; justify-content: center; align-items: flex-start; padding: 30px; }}
  svg {{ max-width: 100%; height: auto; display: block; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
        with open(wrapper_html, "w", encoding="utf-8") as wf:
            wf.write(html_doc)
            
        url = "file:///" + wrapper_html.replace("\\", "/")
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={w},{h}",
            f"--screenshot={png_path}",
            url
        ]
        print(f"Rendering {svg_file} -> {png_file}...")
        subprocess.run(cmd, check=True)
        print(f"Generated {png_path} (size: {os.path.getsize(png_path)} bytes)")
        if os.path.exists(wrapper_html):
            os.remove(wrapper_html)

if __name__ == "__main__":
    render_all()
