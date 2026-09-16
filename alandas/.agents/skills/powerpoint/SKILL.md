---
name: powerpoint
description: >-
  Comprehensive guide and production workflow for generating executive-grade Microsoft PowerPoint (.pptx)
  presentations using python-pptx. Covers 16:9 widescreen layout, custom luxury and brand color palettes,
  typographic hierarchy, card-based layouts, stat callouts, comparison grids, clean tables, and zero-overlap shape math.
---

# PowerPoint (.pptx) Production Engineering Skill

This skill governs how to programmatically generate polished, executive-ready PowerPoint presentations (`.pptx`) using Python (`python-pptx`).

---

## 1. Core Principles for High-Ticket Pitch Decks

1. **Widescreen 16:9 Standard:**
   - Always set `prs.slide_width = Inches(13.333)` and `prs.slide_height = Inches(7.5)`.
   - Never use standard 4:3 unless explicitly requested.

2. **Curated Color Palettes (Never Generic Defaults):**
   - Define RGB tuples for:
     - Background: Linen (`249, 248, 245`) or Dark Slate (`9, 13, 22`)
     - Primary Ink: Deep Charcoal (`28, 29, 26`) or Off-White (`248, 250, 252`)
     - Accent Primary: Botanical Olive (`85, 91, 62`) or Alandas Gold (`197, 139, 43`)
     - Card Backgrounds: Pure White (`255, 255, 255`) or Translucent Glass
     - Functional Accents: Forest Green (`46, 99, 71`) and Crimson (`146, 52, 52`)

3. **Information Density & Typography:**
   - Slide Header: Kicker (uppercase 10pt bold), Title (serif or bold sans 24–30pt), Subtitle (13–15pt muted).
   - Content Containers: Card-based architecture (`MSO_SHAPE.ROUNDED_RECTANGLE` or `RECTANGLE`) with 1pt subtle borders.
   - Key Stats: Large callout numbers (36–48pt) paired with concise descriptor labels.

4. **Zero Overlapping Math:**
   - Explicitly calculate `left`, `top`, `width`, and `height` for every card and grid cell.
   - Use margins: `left_margin = Inches(1.0)`, `top_margin = Inches(1.6)`, `content_height = Inches(4.8)`.

---

## 2. Technical Python Pattern

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)

# Add background rect, headers, cards, and tables
```
