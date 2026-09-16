import json
import os

TRANSCRIPT = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\brain\445482c0-bd2f-4c3e-a494-05a43b97af77\.system_generated\logs\transcript_full.jsonl"
OUT_DIR = r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\reverted_backups"

os.makedirs(OUT_DIR, exist_ok=True)

with open(TRANSCRIPT, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        obj = json.loads(line)
        step = obj.get("step_index")
        for tc in obj.get("tool_calls") or []:
            name = tc.get("name")
            args = tc.get("args", {})
            if step == 107 and name == "write_to_file":
                with open(os.path.join(OUT_DIR, "generate_pdf_report_step107.py"), "w", encoding="utf-8") as out:
                    out.write(args.get("CodeContent", ""))
                print("Extracted generate_pdf_report_step107.py")
                
            elif step == 144 and name == "write_to_file":
                with open(os.path.join(OUT_DIR, "Alandas_Executive_Presentation_step144.html"), "w", encoding="utf-8") as out:
                    out.write(args.get("CodeContent", ""))
                print("Extracted Alandas_Executive_Presentation_step144.html")
                
            elif step == 146 and name == "write_to_file":
                with open(os.path.join(OUT_DIR, "CALL_PREP_SIDY_SOW_BATTLE_CARD_step146.md"), "w", encoding="utf-8") as out:
                    out.write(args.get("CodeContent", ""))
                print("Extracted CALL_PREP_SIDY_SOW_BATTLE_CARD_step146.md")

print("Done extracting target historical steps.")
