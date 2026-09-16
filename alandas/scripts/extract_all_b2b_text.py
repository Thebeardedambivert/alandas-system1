import os
import sys
import pypdfium2 as pdfium
from rapidocr_onnxruntime import RapidOCR

PDF_PATH = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\Alandas_B2B.pdf"
OUT_MD = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\docs\ALANDAS_B2B_CATALOG_FULL_TEXT.md"

def extract_all():
    print("Initializing RapidOCR...")
    engine = RapidOCR()
    
    print(f"Opening PDF: {PDF_PATH}")
    pdf = pdfium.PdfDocument(PDF_PATH)
    total_pages = len(pdf)
    print(f"Total pages: {total_pages}")
    
    full_output = []
    full_output.append("# Complete Text Extraction: Alandas B2B Wholesale Catalog\n")
    full_output.append(f"**Source Document:** `Alandas_B2B.pdf` (24 Pages)  ")
    full_output.append(f"**Target Business:** Alandas Tea Berlin (Sidy Sow)  ")
    full_output.append(f"**Classification:** Official Wholesale Pitch Deck & Product Catalog (Gastro / HoReCa)  \n")
    full_output.append("---\n")
    
    for i in range(total_pages):
        page_num = i + 1
        print(f"Processing Page {page_num}/{total_pages}...")
        page = pdf[i]
        # Render at 2x scale for crisp OCR
        img = page.render(scale=2.0).to_pil()
        
        # Save temp image or pass directly to RapidOCR
        temp_img_path = rf"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\temp_ocr_p{page_num}.png"
        img.save(temp_img_path)
        
        result, elapse_list = engine(temp_img_path)
        
        # Clean up temp image
        try:
            os.remove(temp_img_path)
        except Exception:
            pass
            
        page_lines = []
        if result:
            for item in result:
                # item format: [box, text, score]
                text = item[1]
                page_lines.append(text)
                
        page_text = "\n".join(page_lines)
        print(f"  -> Extracted {len(page_lines)} lines on Page {page_num}")
        
        full_output.append(f"## PAGE {page_num}\n")
        if page_text.strip():
            full_output.append(page_text + "\n")
        else:
            full_output.append("*(Visual / Graphic page - no text detected)*\n")
        full_output.append("\n---\n")
        
    final_content = "\n".join(full_output)
    
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"\n[SUCCESS] Extracted all 24 pages to: {OUT_MD}")

if __name__ == "__main__":
    extract_all()
