# Dilithium Git Commit Signer

A CLI tool to sign and verify Git commits using the CRYSTALS-Dilithium post-quantum digital signature scheme, built with [`dilithium-py`](https://github.com/GiacomoPope/dilithium-py). This tool is for educational purposes only and should not be used in production due to lack of side-channel protections.


# Features
- Generate Dilithium key pairs for different security levels (2, 3, 5).
- Sign Git commits with your private key and store signatures in Git notes (refs/notes/signatures).
- Automatic signing via a post-commit Git hook.
- View signatures stored in Git notes.

# Installation

**1. Clone the repository:**
```bash
git clone https://github.com/Thanh-WuTan/dilithium-git-signer.git
cd dilithium-git-signer
```

**2. Install dependencies and the tool:**
```bash
pip install .
```
Ensure `~/.local/bin` is in your `PATH`:
```bash
export PATH=$PATH:~/.local/bin
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

**3. Verify setup**
```bash
dilithium-signer --help
```

# Usage

**1. Initialize the tool (generate keys and set up the post-commit hook):**
```bash
dilithium-signer init --level 2 --email example@email
```

**2. Sign a commit (automatic via the post-commit hook or manual):**
```bash
# Automatically:
git commit -m "Commit message"
# Or manually:
dilithium-signer sign <commit-hash>
```

**3. Verify a commit:**
```bash
dilithium-signer verify <commit-hash>
```


**4. View a commit’s signature: Signatures are stored in Git notes (refs/notes/signatures). View with:**
```bash
git notes --ref=signatures show <commit-hash>
```

Example output:
```bash
{"email": "exmaple@email", "signature": "<hex-signature>"}
```

**5. Manually set up hook (if needed):**
```bash
dilithium-signer setup-hook
```

# Uninstallation and Hook Removal

To stop using the tool:
**1. Remove the Git hook:**
```bash
rm .git/hooks/post-commit
```

Verify it’s gone:
```bash
ls .git/hooks/post-commit
```

**2. Uninstall the package:**
```bash
pip uninstall dilithium-git-signer -y
```

**3. Remove configuration files:**
```bash
rm -rf ~/.dilithium-signer/
```




# Acknowledgments

Built with `dilithium-py`, a pure-Python implementation of CRYSTALS-Dilithium.

Inspired by post-quantum cryptography research and Git workflows.