import re

path = r"C:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\brain\445482c0-bd2f-4c3e-a494-05a43b97af77\.system_generated\steps\583\content.md"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Let's find sections around github links
for g in [
    "Slide-maestro_agents-skill", "slide-writer", "html2pptx", "Powerpoint-fancy-design",
    "starrykit-plugin", "knowledge-cat-ppt-skill", "slide-skill", "slide-creator",
    "image-to-editable-ppt-skill", "AgentBuff-Presentation-Skills", "guizang-ppt-skill",
    "frontend-slides"
]:
    pos = text.find(g)
    if pos != -1:
        snippet = text[max(0, pos-200):min(len(text), pos+400)]
        clean = re.sub(r'<[^>]+>', ' ', snippet)
        clean = ' '.join(clean.split())
        print(f"=== {g} ===")
        print(clean)
        print()
