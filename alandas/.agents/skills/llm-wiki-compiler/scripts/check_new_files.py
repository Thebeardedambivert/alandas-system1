import os
import json
import time

# 設定路徑
WATCH_DIRS = [
    "/Users/dwaynejohnson/Library/CloudStorage/OneDrive-個人/Documents/00_KM_核心知識庫/20_LLM_Wiki/02_Raw_原始資料",
    "/Users/dwaynejohnson/Library/CloudStorage/OneDrive-個人/Documents/00_KM_核心知識庫"
]
STATE_FILE = os.path.expanduser("~/.gemini/skills/llm-wiki-compiler/state.json")

def get_file_list(dirs):
    files = {}
    for d in dirs:
        if not os.path.exists(d): continue
        for root, _, filenames in os.walk(d):
            # 排除隱藏資料夾與 .obsidian
            if ".obsidian" in root or ".git" in root or "20_LLM_Wiki/01_System" in root: continue
            for f in filenames:
                if f.startswith(".") or f.endswith(".DS_Store"): continue
                full_path = os.path.join(root, f)
                # 紀錄檔案路徑與最後修改時間
                files[full_path] = os.path.getmtime(full_path)
    return files

def main():
    # 載入舊狀態
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            old_state = json.load(f)
    else:
        old_state = {}

    current_state = get_file_list(WATCH_DIRS)
    
    # 找出新檔案 (包含新增或修改過的)
    new_files = []
    for path, mtime in current_state.items():
        if path not in old_state or mtime > old_state[path]:
            new_files.append(path)

    # 輸出結果
    if new_files:
        print(f"FOUND_NEW_FILES: {json.dumps(new_files, ensure_ascii=False)}")
    else:
        print("NO_NEW_FILES")

    # 更新狀態 (暫不更新，直到確定編譯完成)
    # 這裡的邏輯由 Skill 指令來控制是否寫回狀態

if __name__ == "__main__":
    main()
