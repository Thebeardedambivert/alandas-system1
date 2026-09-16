# Alandas Client Engagement & Strategic Workspace

**Client:** Alandas (Alandas Tea Berlin)  
**Website:** [https://alandas.de](https://alandas.de)  
**Founder:** Sidy Sow (Berlin, Germany)  
**Lead Strategist:** Cyril Uzochukwu  

---

## 📁 Workspace Structure

```
alandas/
├── Alandas_Site_Audit_Report.pdf     # Master 8-page executive PDF audit deliverable
├── README.md                          # Workspace index & engagement guide
├── docs/
│   ├── Alandas_Site_Audit_Report.pdf  # PDF report archive
│   └── alandas_comprehensive_site_audit.md # Full Markdown site audit & translation
├── assets/
│   ├── logo.png                       # Official transparent Alandas logo
│   └── hero_bombay.png                # Official brand visual banner
├── data/
│   ├── products.json                  # Complete 26-SKU catalog snapshot
│   └── parsed_analysis.json           # Scraped HTML pages & structured data
└── scripts/
    └── generate_pdf_report.py         # Python ReportLab compilation script
```

---

## 🎯 Strategic Summary & Key Findings

1. **The Core Teardown:**
   * 26 SKUs completely scoped and translated into English: 13 cultural destination blends (*Istanbul, Bombay, Marrakech, Paris, Berlin, Damaskus, London, California, Granada, Manila, Schwarzwald, Himalaya, Budapest*), 6 classics, and 7 teaware/hardware pieces.
   * Unit economics model: **€0.25/pot cost vs. €4.50–€5.90 menu price** (90%+ gross margin for cafes).

2. **The 4 Primary Bottlenecks to Fix:**
   * **Shipping Threshold Conflict:** Product pages state *"Free shipping over €59"*, while the official shipping policy page states *"Free shipping over €40"*.
   * **Sample Box Price Discrepancy:** The B2B Gastro page lists the box at **€19.00**, while the Contact page advertises it at **€9.90 netto**.
   * **Flagship Hardware Bottleneck:** The **Teebar Wooden Shelf (€79.00)** is currently **Out of Stock** online.
   * **Analytics Blind Spot:** Zero Google Analytics 4, zero Google Tag Manager, zero Meta Pixel, and zero email retention automation (Klaviyo).

---

## 🚀 Quick Commands

* **Recompile PDF Report:**
  ```powershell
  python scripts\generate_pdf_report.py
  ```
