import subprocess
import os
from pathlib import Path

HOOK_PATH = ".git/hooks/post-commit"

def run_git_command(args):
    """Run a Git command and return output."""
    result = subprocess.run(['git'] + args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr}")
    return result.stdout.strip()

def setup_hook():
    """Install Git hook for automatic commit signing."""
    hook_dir = Path('.git/hooks')
    hook_dir.mkdir(exist_ok=True)
    
    hook_content = f"""
#!/bin/sh
# Dilithium Git Commit Signer Hook
dilithium-signer sign $(git rev-parse HEAD)
"""
    with open(hook_dir / 'post-commit', 'w') as f:
        f.write(hook_content)
    os.chmod(hook_dir / 'post-commit', 0o755)
    return HOOK_PATH