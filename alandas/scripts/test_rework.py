import re

def rework():
    with open('Alandas_Master_Growth_System.backup.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for slides
    pattern = re.compile(r'<!-- SLIDE (\d+): (.*?) -->\s*<section class="slide([^"]*)">(.*?)</section>', re.DOTALL)
    slides = pattern.findall(content)
    print(f"Loaded {len(slides)} slides from backup.")

    # Let's inspect each slide's content and prepare the clean 1920x1080 slide wrapper
    new_slides = []
    
    for num_str, name, extra_class, body in slides:
        num = int(num_str)
        is_first = (num == 1)
        active_class = " active visible" if is_first else ""
        
        # Clean up body: remove any existing slide padding / style overrides
        # Extract kicker, slide-title, slide-lead if present
        kicker_match = re.search(r'<div class="kicker">(.*?)</div>', body, re.DOTALL)
        title_match = re.search(r'<h1 class="slide-title"[^>]*>(.*?)</h1>', body, re.DOTALL)
        lead_match = re.search(r'<p class="slide-lead"[^>]*>(.*?)</p>', body, re.DOTALL)
        
        # Extract remaining content after header
        # Check if header is inside a <div> ... </div>
        header_div_match = re.search(r'^\s*<div>(.*?)</div>\s*(<div class="grid|<div class="table|<div style)', body, re.DOTALL)
        
        kicker_html = kicker_match.group(0).strip() if kicker_match else ""
        title_html = title_match.group(0).strip() if title_match else ""
        lead_html = lead_match.group(0).strip() if lead_match else ""
        
        # Build clean header
        header_html = f"""      <header class="slide-header reveal">
        {kicker_html}
        {title_html}
        {lead_html}
      </header>"""

        # Now extract the content body (grids, tables, stat-boxes, etc.)
        # Remove the header portion from body
        cleaned_body = body
        if kicker_match:
            cleaned_body = cleaned_body.replace(kicker_match.group(0), '')
        if title_match:
            cleaned_body = cleaned_body.replace(title_match.group(0), '')
        if lead_match:
            cleaned_body = cleaned_body.replace(lead_match.group(0), '')
        
        # Remove empty <div></div> from the top if left behind
        cleaned_body = re.sub(r'^\s*<div>\s*</div>\s*', '', cleaned_body, flags=re.DOTALL)
        
        # Check for bottom note / footer note in original
        footer_note_match = re.search(r'<div style="font-size: 0\.75rem;[^"]*">(.*?)</div>', cleaned_body, re.DOTALL)
        footer_note_text = ""
        if footer_note_match:
            footer_note_text = re.sub(r'<[^>]+>', ' ', footer_note_match.group(1)).strip()
            footer_note_text = re.sub(r'\s+', ' ', footer_note_text)
            cleaned_body = cleaned_body.replace(footer_note_match.group(0), '')
        
        if not footer_note_text:
            footer_note_text = "ALANDAS TEA BERLIN • COMMERCIAL GROWTH ARCHITECTURE • NATIONWIDE GERMANY"
        
        # Add reveal classes to cards and stat boxes for staggered smooth animations
        # We can add reveal and reveal-delay-X to cards
        def add_reveal_to_cards(grid_match):
            grid_html = grid_match.group(0)
            # Find all top-level children with class "card" or "stat-box"
            card_matches = re.split(r'(<div class="(?:card|stat-box)[^"]*">)', grid_html)
            out = []
            delay_idx = 1
            for part in card_matches:
                if part.startswith('<div class="card') or part.startswith('<div class="stat-box'):
                    # add reveal reveal-delay-X
                    part = part.replace('class="', f'class="reveal reveal-delay-{min(delay_idx, 6)} ')
                    delay_idx += 1
                out.append(part)
            return "".join(out)
        
        # Process grids
        cleaned_body = re.sub(r'<div class="grid grid-\d+">.*?</div>\s*(?=(?:<div class="grid|<div class="table|<div style|$))', add_reveal_to_cards, cleaned_body, flags=re.DOTALL)
        
        # If table, add reveal to table-container
        cleaned_body = cleaned_body.replace('<div class="table-container">', '<div class="table-container reveal reveal-delay-2">')

        # Format slide HTML
        slide_block = f"""    <!-- SLIDE {num}: {name} -->
    <section class="slide{active_class}" id="slide-{num}">
{header_html}
      <div class="slide-body">
{cleaned_body.strip()}
      </div>
      <footer class="slide-footer reveal">
        <span class="footer-meta">{footer_note_text}</span>
        <span class="footer-counter">{str(num).zfill(2)} / {str(len(slides)).zfill(2)}</span>
      </footer>
    </section>"""
        new_slides.append(slide_block)

    print(f"Generated {len(new_slides)} new slides.")
    return "\n\n".join(new_slides)

if __name__ == '__main__':
    rework()
