"""
build_luxury_pdf_with_skill.py
Uses the newly installed `pdf` skill toolset (pypdfium2, pypdf, Chrome engine) to:
1. Create a print-optimized 16:9 widescreen HTML document (1920x1080 per slide).
2. Render ultra-high-definition PDF via Chromium engine with true Google Fonts (Playfair Display, Plus Jakarta Sans, JetBrains Mono).
3. Inject executive metadata using pypdf.
4. Render high-res inspection images of every page using pypdfium2 to visually verify quality.
"""

import os
import re
import subprocess
import pypdf
import pypdfium2 as pdfium

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_src = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck.html")
    html_print = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck_Print.html")
    pdf_out = os.path.join(base_dir, "Alandas_Sidy_Cheat_Sheet_Deck.pdf")
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    print("Step 1: Preparing Print-Optimized 16:9 HTML Template...")
    with open(html_src, "r", encoding="utf-8") as f:
        html = f.read()

    # Inject print-specific CSS rules for 1920x1080 per page
    print_css = """
    <style id="print-perfect-styles">
      @page {
        size: 1920px 1080px;
        margin: 0;
      }
      @media print, screen {
        html, body {
          width: 1920px !important;
          height: auto !important;
          overflow: visible !important;
          background: #0C0F0C !important;
          margin: 0 !important;
          padding: 0 !important;
        }
        .deck-viewport {
          position: static !important;
          display: block !important;
          overflow: visible !important;
          width: 1920px !important;
          height: auto !important;
          background: #0C0F0C !important;
        }
        .deck-stage {
          position: static !important;
          width: 1920px !important;
          height: auto !important;
          transform: none !important;
          box-shadow: none !important;
          border-radius: 0 !important;
          display: block !important;
          background: transparent !important;
        }
        .slide {
          position: relative !important;
          width: 1920px !important;
          height: 1080px !important;
          display: flex !important;
          opacity: 1 !important;
          visibility: visible !important;
          pointer-events: auto !important;
          page-break-after: always !important;
          break-after: page !important;
          page-break-inside: avoid !important;
          break-inside: avoid !important;
          margin: 0 !important;
          padding: 64px 84px 54px 84px !important;
          background: #F9F7F2 !important;
          background-image: radial-gradient(1400px 900px at 50% 0%, #FFFFFF 0%, #F9F7F2 60%, #EDE7D8 100%) !important;
          box-sizing: border-box !important;
        }
        .deck-nav, .flowchart-modal, .flowchart-toggle-group, .modal-backdrop {
          display: none !important;
        }
        .view-panel {
          display: none !important;
        }
        .view-panel.active, #slide-6-cards, #slide-7-cards, #slide-8-cards {
          display: flex !important;
        }
      }
    </style>
    """

    # Ensure all view-panels on slides 6, 7, 8 display the executive cards by default in print
    html_print_content = html.replace("</head>", f"{print_css}\n</head>")
    
    with open(html_print, "w", encoding="utf-8") as f:
        f.write(html_print_content)
    print(f"[SUCCESS] Print HTML created: {html_print}")

    print("\nStep 2: Rendering Ultra-Luxury PDF via Chromium Engine...")
    url = "file:///" + html_print.replace(os.sep, "/")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=5000",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_out}",
        url
    ]
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] PDF generated via Chromium: {pdf_out} (size: {os.path.getsize(pdf_out)} bytes)")

    print("\nStep 3: Injecting Executive Document Metadata via pypdf...")
    reader = pypdf.PdfReader(pdf_out)
    writer = pypdf.PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)

    metadata = {
        "/Title": "Alandas Tea Berlin — Sidy's Revenue Roadmap & Cheat Sheet",
        "/Author": "Cyril Uzochukwu & Sidy Sow",
        "/Subject": "Wholesale Growth Architecture: The Path from 25 to 100 Cafes (€15k–€30k/mo)",
        "/Creator": "Alandas Executive Architecture System (PDF Skill)",
        "/Producer": "Google Antigravity & PDF Engine",
        "/Keywords": "Alandas, B2B Tea, Dolibarr CRM, Temporal, WhatsApp Automation, Berlin, Munich"
    }
    writer.add_metadata(metadata)

    with open(pdf_out, "wb") as f_out:
        writer.write(f_out)
    print(f"[SUCCESS] Metadata successfully written. Total pages: {len(reader.pages)}")

    print("\nStep 4: Inspecting and Verifying Pages via pypdfium2...")
    pdf_doc = pdfium.PdfDocument(pdf_out)
    print(f"Verified {len(pdf_doc)} pages in PDF document.")
    
    # Render page 1, 4, 6, 11 to PNG for instant visual proof
    verify_pages = [0, 3, 5, 10]
    for p_idx in verify_pages:
        page = pdf_doc[p_idx]
        bitmap = page.render(scale=1.5)
        img = bitmap.to_pil()
        preview_path = os.path.join(base_dir, f"temp_preview_page_{p_idx + 1}.png")
        img.save(preview_path, "PNG")
        print(f"Saved preview for Page {p_idx + 1}: {preview_path} ({os.path.getsize(preview_path)} bytes)")

    # Clean up temp print html
    if os.path.exists(html_print):
        os.remove(html_print)

    print("\n[COMPLETE] Executive PDF rework finished flawlessly!")

if __name__ == "__main__":
    main()
