import urllib.request
import json
import os
import zipfile
import io

def download_repo_zip(repo_full_name, extract_to):
    print(f"Downloading {repo_full_name} zip archive...")
    zip_url = f"https://github.com/{repo_full_name}/archive/refs/heads/main.zip"
    req = urllib.request.Request(zip_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            zip_bytes = resp.read()
    except Exception as e:
        print(f"Failed with main.zip, trying master.zip: {e}")
        zip_url = f"https://github.com/{repo_full_name}/archive/refs/heads/master.zip"
        req = urllib.request.Request(zip_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            zip_bytes = resp.read()

    print(f"Extracting to {extract_to}...")
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        z.extractall(extract_to)
    print(f"[SUCCESS] Extracted {repo_full_name} to {extract_to}")

if __name__ == "__main__":
    download_repo_zip("zarazhangrui/frontend-slides", r"c:\Users\Cyril Uzochukwu\.gemini\antigravity-ide\scratch\alandas\extracted_skills\frontend-slides")
