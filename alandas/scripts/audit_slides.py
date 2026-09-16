import re

with open('Alandas_Master_Growth_System.backup.html', 'r', encoding='utf-8') as f:
    text = f.read()

slides = re.findall(r'<!-- SLIDE (\d+): (.*?) -->\s*<section class="slide([^"]*)">(.*?)</section>', text, re.DOTALL)
print(f"Total slides found: {len(slides)}")

for num, name, extra, body in slides:
    grids = re.findall(r'class="[^"]*(grid-\d+|table-container)[^"]*"', body)
    h3s = re.findall(r'<h3>(.*?)</h3>', body)
    lis = re.findall(r'<li>(.*?)</li>', body)
    print(f"Slide {int(num):02d}: {name[:32]:<32} | Grids: {grids} | Cards: {len(h3s)} | Bullets: {len(lis)}")
