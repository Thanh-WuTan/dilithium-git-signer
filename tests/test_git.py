import pytest
import subprocess
import json
from src.signer import CONFIG_DIR, KEY_FILE, REGISTRY_DIR
from src.signer import generate_keypair, sign_commit, verify_commit 
from src.git_integration import run_git_command 

@pytest.fixture
def git_repo(tmp_path):
    """Set up a temporary Git repository."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(['git', 'init'], cwd=repo_dir, capture_output=True)
    subprocess.run(['git', 'config', 'user.email', 'alice@example.com'], cwd=repo_dir, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Alice'], cwd=repo_dir, capture_output=True)
    return repo_dir

def test_sign_verify_commit(git_repo, tmp_path):
    """Test signing and verifying a commit in a Git repo."""
    # Set up keys
    config_dir = tmp_path / ".dilithium-signer"
    global CONFIG_DIR, KEY_FILE, REGISTRY_DIR
    CONFIG_DIR = config_dir
    KEY_FILE = CONFIG_DIR / "keys.json"
    REGISTRY_DIR = CONFIG_DIR / "registry"
    
    keys = generate_keypair("2", "alice@example.com")
    
    # Create a commit
    with open(git_repo / "test.txt", "w") as f:
        f.write("Test file")
    subprocess.run(['git', 'add', 'test.txt'], cwd=git_repo, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Add test file'], cwd=git_repo, capture_output=True)
    commit_hash = run_git_command(['rev-parse', 'HEAD']).strip()
    
    # Sign commit
    commit_msg = run_git_command(['show', '-s', '--format=%B', commit_hash]).encode()
    sk = bytes.fromhex(keys["secret_key"])
    sig = sign_commit(commit_msg, sk, "2", verbose=False)
    
    # Store signature in Git notes
    note_data = json.dumps({"email": "alice@example.com", "signature": sig.hex()})
    run_git_command(['notes', '--ref=signatures', 'add', '-f', '-m', note_data, commit_hash])
    
    # Verify commit
    pk = bytes.fromhex(keys["public_key"])
    is_valid = verify_commit(commit_msg, sig, pk, "2", verbose=False)
    assert is_valid