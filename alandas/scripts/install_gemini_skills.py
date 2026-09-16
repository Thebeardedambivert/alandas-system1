"""
install_gemini_skills.py
Downloads the gemini-skills zipball from GitHub and installs all skills into:
1. Global Customizations Root: C:\\Users\\Cyril Uzochukwu\\.gemini\\config\\skills\\
2. Workspace Customizations Root: .agents\\skills\\
"""

import os
import io
import shutil
import zipfile
import urllib.request

def install_skills():
    zip_url = "https://github.com/skytiger6724/gemini-skills/archive/refs/heads/main.zip"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    print(f"Downloading {zip_url}...")
    req = urllib.request.Request(zip_url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    print(f"Downloaded {len(data)} bytes. Extracting archive...")

    global_skills_dir = r"C:\Users\Cyril Uzochukwu\.gemini\config\skills"
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workspace_skills_dir = os.path.join(workspace_dir, ".agents", "skills")

    os.makedirs(global_skills_dir, exist_ok=True)
    os.makedirs(workspace_skills_dir, exist_ok=True)

    installed_skills = []
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        namelist = zf.namelist()
        root_prefix = namelist[0].split("/")[0] + "/"

        skill_candidates = set()
        for name in namelist:
            if not name.startswith(root_prefix):
                continue
            rel = name[len(root_prefix):].strip("/")
            parts = rel.split("/")
            if len(parts) >= 1 and parts[0]:
                skill_candidates.add(parts[0])

        print(f"Discovered {len(skill_candidates)} candidate directories...")

        for skill in sorted(skill_candidates):
            prefix = f"{root_prefix}{skill}/"
            skill_files = [n for n in namelist if n.startswith(prefix)]
            has_skill_md = any(n.endswith("SKILL.md") for n in skill_files)

            if not has_skill_md:
                continue

            for target_base in [global_skills_dir, workspace_skills_dir]:
                target_skill_dir = os.path.join(target_base, skill)
                os.makedirs(target_skill_dir, exist_ok=True)
                for member in skill_files:
                    if member.endswith("/"):
                        continue
                    member_rel = member[len(prefix):]
                    out_path = os.path.join(target_skill_dir, member_rel.replace("/", os.sep))
                    os.makedirs(os.path.dirname(out_path), exist_ok=True)
                    with zf.open(member) as src, open(out_path, "wb") as dst:
                        dst.write(src.read())

            installed_skills.append(skill)

    print(f"\n[SUCCESS] Successfully installed {len(installed_skills)} skills into:")
    print(f"  -> Global: {global_skills_dir}")
    print(f"  -> Workspace: {workspace_skills_dir}")
    print("\nInstalled Skills:")
    for i, s in enumerate(installed_skills, 1):
        print(f"  {i:02d}. {s}")

if __name__ == "__main__":
    install_skills()
