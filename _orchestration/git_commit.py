import os
import json
import subprocess

INVENTORY_PATH = "_orchestration/inventory.json"
BRANCH_NAME = "feat/premium-photos-ui"

# Load inventory
with open(INVENTORY_PATH, "r") as f:
    inventory = json.load(f)

def run_git(args):
    print("Running:", "git " + " ".join(args))
    res = subprocess.run(["git"] + args, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Git Error: {res.stderr}")
    return res

def main():
    # 1. Checkout new branch
    run_git(["checkout", "-b", BRANCH_NAME])
    
    # 2. Commit each mountain's files
    for m in inventory:
        m_id = m["id"]
        m_name = m["name_en"]
        
        # Track files to stage for this mountain
        files_to_stage = []
        
        # Check image assets
        img_dir = f"assets/img/{m_id}"
        if os.path.exists(img_dir):
            files_to_stage.append(img_dir)
            
        # Check playbook file
        file_name = m.get("file")
        if file_name and os.path.exists(file_name):
            files_to_stage.append(file_name)
            
        if files_to_stage:
            # Stage files
            for path in files_to_stage:
                run_git(["add", path])
                
            # Check if there are changes to commit
            status = run_git(["status", "--porcelain"])
            if status.stdout.strip():
                commit_msg = f"feat(photos): add photographic assets and upgrade playbook for {m_name}"
                run_git(["commit", "-m", commit_msg])
                print(f"Committed {m_name} changes.")
            else:
                print(f"No changes to commit for {m_name}.")
                
    # 3. Commit index.html changes
    if os.path.exists("index.html"):
        run_git(["add", "index.html"])
        # Check brand assets
        brand_dir = "assets/brand"
        if os.path.exists(brand_dir):
            run_git(["add", brand_dir])
            
        status = run_git(["status", "--porcelain"])
        if status.stdout.strip():
            run_git(["commit", "-m", "feat(ui): upgrade index page cards with photographic thumbnails"])
            print("Committed index.html changes.")
            
    # 4. Commit documentation and orchestration files
    files_docs = ["CREDITS.md", "ORCHESTRATION-UPGRADE.md", "_orchestration/"]
    for path in files_docs:
        if os.path.exists(path):
            run_git(["add", path])
            
    status = run_git(["status", "--porcelain"])
    if status.stdout.strip():
        run_git(["commit", "-m", "chore(docs): add photo credits, manifests, and orchestration reports"])
        print("Committed docs and orchestration reports.")
        
    print("\nGit atomic commits complete! Recent commits:")
    res = run_git(["log", "-n", "30", "--oneline"])
    print(res.stdout)

if __name__ == "__main__":
    main()
