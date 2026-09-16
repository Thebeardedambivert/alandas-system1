import re

path = r"C:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\brain\445482c0-bd2f-4c3e-a494-05a43b97af77\.system_generated\steps\583\content.md"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Look for github links
gh = set(re.findall(r"https?://github\.com/[a-zA-Z0-9_\-\./]+", text))
print("=== GITHUB LINKS ===")
for g in sorted(gh):
    print(g)

# Look for headers
print("\n=== HEADERS ===")
headers = re.findall(r"<h[1-4][^>]*>(.*?)</h[1-4]>", text, re.DOTALL)
for h in headers:
    clean = re.sub(r"<[^>]+>", "", h).strip()
    if clean:
        print(clean)

# Look for skills or list items
print("\n=== SKILL BLOCKS OR TITLES ===")
# Search for patterns like '1. ', '2. ', or skills
for m in re.finditer(r"(?:skill|ppt|slide|agent|star|github)[^<>\n]{0,100}", text, re.IGNORECASE):
    pass
