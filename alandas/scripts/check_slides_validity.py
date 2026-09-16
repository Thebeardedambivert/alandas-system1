import re
import sys
sys.path.append('scripts')
from test_rework import rework

new_slides_html = rework()

# Check each slide
slides = re.findall(r'<!-- SLIDE (\d+): (.*?) -->\s*<section class="slide[^"]*" id="slide-\d+">(.*?)</section>', new_slides_html, re.DOTALL)
print(f"Total parsed: {len(slides)}")

for num, name, body in slides:
    open_divs = len(re.findall(r'<div\b', body))
    close_divs = len(re.findall(r'</div>', body))
    h1 = re.findall(r'<h1\b', body)
    if open_divs != close_divs or len(h1) != 1:
        print(f"Slide {num} ({name}): open_divs={open_divs}, close_divs={close_divs}, h1s={len(h1)}")
print("Check completed.")
