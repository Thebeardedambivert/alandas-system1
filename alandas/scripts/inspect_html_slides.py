import re

with open('Alandas_Master_Growth_System.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'<!-- SLIDE (\d+): (.*?) -->\s*<section class="slide[^"]*">(.*?)</section>', re.DOTALL)
matches = pattern.findall(html)
print(f'Matches count: {len(matches)}')

for num, name, body in matches:
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.DOTALL)
    title = title_match.group(1).replace('\n', ' ').strip() if title_match else 'NO H1'
    title = re.sub(r'<[^>]+>', ' ', title)
    title = ' '.join(title.split())
    grids = re.findall(r'class="grid (grid-\d+)"', body)
    has_table = '<table>' in body
    print(f'Slide {num:2s}: [{name:32s}] | H1: {title[:45]:45s} | Grids: {str(grids):20s} | Table: {has_table}')
