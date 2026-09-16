"""
extract_skills.py
Unpacks gemini_skills.zip and copies each skill to:
- Global: C:\\Users\\Cyril Uzochukwu\\.gemini\\config\\skills
- Workspace: .agents\\skills
"""

import os
import zipfile
import shutil

def extract_and_install():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_path = os.path.join(base_dir, "gemini_skills.zip")
    
    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} not found.")
        return

    global_skills_dir = r"C:\Users\Cyril Uzochukwu\.gemini\config\skills"
    workspace_skills_dir = os.path.join(base_dir, ".agents", "skills")

    os.makedirs(global_skills_dir, exist_ok=True)
    os.makedirs(workspace_skills_dir, exist_ok=True)

    installed_skills = []
    with zipfile.ZipFile(zip_path, "r") as zf:
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

        print(f"Scanning {len(skill_candidates)} directories in archive...")

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
    print(f"  -> Global Root: {global_skills_dir}")
    print(f"  -> Workspace Root: {workspace_skills_dir}")
    print("\nInstalled Skills List:")
    for i, s in enumerate(installed_skills, 1):
        print(f"  {i:02d}. {s}")

    # Remove temporary zip file to keep workspace tidy
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print("\nCleaned up gemini_skills.zip.")

if __name__ == "__main__":
    extract_and_install()
