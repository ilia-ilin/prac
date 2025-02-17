import sys
from pathlib import Path

def list_branches(repo_path):
    git_dir = Path(repo_path) / ".git"
    heads_dir = git_dir / "refs/heads"
    if not heads_dir.exists():
        raise ValueError("Not a valid git repository")
    
    for branch in heads_dir.glob("*"):
        print(branch.name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: prog.py REPO_PATH [BRANCH]")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    if len(sys.argv) == 2:
        list_branches(repo_path)