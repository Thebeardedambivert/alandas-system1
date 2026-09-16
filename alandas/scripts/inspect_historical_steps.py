import json
import re

TRANSCRIPT = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\brain\445482c0-bd2f-4c3e-a494-05a43b97af77\.system_generated\logs\transcript_full.jsonl"

def inspect_steps():
    with open(TRANSCRIPT, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            obj = json.loads(line)
            step = obj.get("step_index")
            t_calls = obj.get("tool_calls") or []
            for tc in t_calls:
                args = tc.get("args", {})
                tf = args.get("TargetFile", "")
                if step in [107, 125, 144, 146]:
                    print(f"=== STEP {step}: {tc.get('name')} on {tf} ===")
                    content = args.get("CodeContent", "")
                    if tf.endswith(".html"):
                        titles = re.findall(r'<h[12][^>]*>(.*?)</h[12]>', content, re.DOTALL)
                        print("Titles found in HTML:")
                        for t in titles[:10]:
                            print("  -", t.strip().replace("\n", " "))
                    elif tf.endswith(".md"):
                        headers = [l for l in content.split("\n") if l.startswith("#")][:10]
                        print("Headers found in MD:")
                        for h in headers:
                            print("  -", h)
                    elif tf.endswith(".py"):
                        print(f"Python file length: {len(content)} bytes")

if __name__ == "__main__":
    inspect_steps()
