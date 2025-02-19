import sys
from pathlib import Path
import zlib

def list_branches(repo_path):
    git_dir = Path(repo_path) / ".git"
    heads_dir = git_dir / "refs/heads"
    if not heads_dir.exists():
        raise ValueError("Not a valid git repository")
    
    for branch in heads_dir.glob("*"):
        print(branch.name)

def show_commit(repo_path, branch):
    git_dir = Path(repo_path) / ".git"
    ref_path = git_dir / "refs/heads" / branch
    if not ref_path.exists():
        raise ValueError(f"Branch {branch} not found")
    
    with open(ref_path, "r") as f:
        commit_sha = f.read().strip()
    
    obj_path = git_dir / "objects" / commit_sha[:2] / commit_sha[2:]
    with open(obj_path, "rb") as f:
        raw = zlib.decompress(f.read())
    
    header, _, body = raw.partition(b'\x00')
    print(body.decode())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: prog.py REPO_PATH [BRANCH]")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    if len(sys.argv) == 2:
        list_branches(repo_path)
    elif len(sys.argv) == 3:
        show_commit(sys.argv[1], sys.argv[2])