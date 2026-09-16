import os
import json
import time

# 設定路徑 (與 check_new_files.py 保持一致)
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
            if ".obsidian" in root or ".git" in root or "20_LLM_Wiki/01_System" in root: continue
            for f in filenames:
                if f.startswith(".") or f.endswith(".DS_Store"): continue
                full_path = os.path.join(root, f)
                files[full_path] = os.path.getmtime(full_path)
    return files

def main():
    # 獲取當前所有檔案狀態
    current_state = get_file_list(WATCH_DIRS)
    
    # 確保目錄存在
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    
    # 寫回狀態文件
    with open(STATE_FILE, "w") as f:
        json.dump(current_state, f, indent=2, ensure_ascii=False)
    
    print("STATE_UPDATED")

if __name__ == "__main__":
    main()
