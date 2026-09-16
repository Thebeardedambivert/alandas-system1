import re

with open('Alandas_Master_Growth_System.backup.html', 'r', encoding='utf-8') as f:
    raw_html = f.read()

# Pattern to capture slide comment, slide attributes, and inner content
slide_pattern = re.compile(r'<!-- SLIDE (\d+): (.*?) -->\s*<section class="slide([^"]*)">(.*?)</section>', re.DOTALL)
matches = slide_pattern.findall(raw_html)

print(f"Captured {len(matches)} slides.")
for num, comment_title, extra_class, content in matches:
    # Check if there is a header block
    kicker = re.search(r'<div class="kicker">(.*?)</div>', content)
    title = re.search(r'<h1 class="slide-title"[^>]*>(.*?)</h1>', content, re.DOTALL)
    lead = re.search(r'<p class="slide-lead"[^>]*>(.*?)</p>', content, re.DOTALL)
    footer = re.search(r'<div style="font-size: 0\.75rem;[^"]*">(.*?)</div>', content, re.DOTALL)
    
    kicker_txt = kicker.group(1).strip() if kicker else "None"
    title_txt = re.sub(r'\s+', ' ', title.group(1)).strip() if title else "None"
    print(f"[{num}] {comment_title} | Kicker: {kicker_txt[:25]} | Title: {title_txt[:35]} | Footer: {bool(footer)}")
