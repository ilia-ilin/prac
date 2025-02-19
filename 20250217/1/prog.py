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

def get_commit(repo_path, branch):
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
    return body.decode()
    
def get_tree(repo_path, commit_sha):
    obj_path = Path(repo_path) / ".git/objects" / commit_sha[:2] / commit_sha[2:]
    with open(obj_path, "rb") as f:
        raw = zlib.decompress(f.read())
    
    _, _, body = raw.partition(b'\x00')
    tree_entries = []
    while body:
        mode_name, _, rest = body.partition(b'\x00')
        sha = rest[:20].hex()
        body = rest[20:]
        mode, name = mode_name.split(b' ', 1)
        tree_entries.append(f"{mode.decode()} {sha}    {name.decode()}")
    return "\n".join(tree_entries)

def show_tree(repo_path, branch):
    commit_body = get_commit(repo_path, branch)
    tree_line = next(line for line in commit_body.split('\n') if line.startswith('tree'))
    tree_sha = tree_line.split()[1]
    print(get_tree(repo_path, tree_sha))

def walk_history(repo_path, branch):
    ref_path = Path(repo_path) / ".git/refs/heads" / branch
    current_sha = ref_path.read_text().strip()
    
    while current_sha:
        commit_body = get_commit(repo_path, current_sha)
        tree_line = next(line for line in commit_body.split('\n') if line.startswith('tree'))
        tree_sha = tree_line.split()[1]
        print(f"TREE for commit {current_sha}")
        tree_content = get_tree(repo_path, tree_sha)
        print(tree_content)
        parents = [line.split()[1] for line in commit_body.split('\n') if line.startswith('parent')]
        current_sha = parents[0] if parents else None

def show_commit(repo_path, branch):
    commit_body = get_commit(repo_path, branch)
    print(commit_body)
    show_tree(repo_path, branch)
    walk_history(repo_path, branch)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: prog.py REPO_PATH [BRANCH]")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    if len(sys.argv) == 2:
        list_branches(repo_path)
    elif len(sys.argv) == 3:
        show_commit(sys.argv[1], sys.argv[2])