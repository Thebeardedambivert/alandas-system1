import re

with open('Alandas_Master_Growth_System.html', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'<!-- SLIDE (\d+): (.*?) -->\s*<section class="slide[^"]*">(.*?)</section>', re.DOTALL)
slides = pattern.findall(text)

print(f"Total slides found: {len(slides)}")
for num, name, body in slides:
    print(f"Slide {num}: {name} ({len(body)} chars)")
