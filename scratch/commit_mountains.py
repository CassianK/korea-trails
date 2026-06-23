import os
import subprocess

WORKSPACE_DIR = "/Users/mac/korea-trails"

def main():
    # Find all playbook files in root
    playbooks = [f for f in os.listdir(WORKSPACE_DIR) if f.endswith("-playbook.html")]
    
    for p in playbooks:
        m_id = p.replace("-playbook.html", "")
        
        # Check if modified
        status_root = subprocess.run(["git", "status", "--porcelain", p], cwd=WORKSPACE_DIR, capture_output=True, text=True)
        en_p = f"en/{p}"
        status_en = subprocess.run(["git", "status", "--porcelain", en_p], cwd=WORKSPACE_DIR, capture_output=True, text=True)
        
        to_commit = []
        if status_root.stdout.strip():
            to_commit.append(p)
        if status_en.stdout.strip():
            to_commit.append(en_p)
            
        if to_commit:
            print(f"Staging and committing: {m_id}")
            for item in to_commit:
                subprocess.run(["git", "add", item], cwd=WORKSPACE_DIR)
            
            commit_msg = f"chore({m_id}): update drawer navigation to link cycling and maps"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=WORKSPACE_DIR)

if __name__ == "__main__":
    main()
