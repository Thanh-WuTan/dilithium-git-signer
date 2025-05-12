# Dilithium Git Commit Signer

A CLI tool to sign and verify Git commits using the CRYSTALS-Dilithium post-quantum digital signature scheme, built with [`dilithium-py`](https://github.com/GiacomoPope/dilithium-py). This tool is for educational purposes only and should not be used in production due to lack of side-channel protections.


# Features
- Generate Dilithium key pairs for different security levels (2, 3, 5).
- Sign Git commits with your private key and store signatures in Git notes (`refs/notes/signatures`).
- Export/import public keys to/from files for team collaboration.
- Automatic signing via a `post-commit` Git hook.
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

**Initialize the tool (generate keys and set up the post-commit hook):**
```bash
dilithium-signer init --level 2 --email example@email
```

**Export public key to share:**
```bash
dilithium-signer export-key --output </path/to/output/file>
```

**Save a public key to local registry:**
```bash
dilithium-signer import-key <path/to/public/key/file>
```

**List public keys in local registry:**
```bash
dilithium-signer list-keys
```

**Sign a commit (automatic via the post-commit hook or manual):**
```bash
# Automatically:
git commit -m "Commit message"
# Or manually:
dilithium-signer sign <commit-hash>
```

**Verify a commit:**
```bash
dilithium-signer verify <commit-hash>
```

**View a commit’s signature: Signatures are stored in Git notes (refs/notes/signatures). View with:**
```bash
git notes --ref=signatures show <commit-hash>
```

Example output:
```bash
{"email": "exmaple@email", "signature": "<hex-signature>"}
```

**Manually set up hook (if needed):**
```bash
dilithium-signer setup-hook
```


# Workflow

This tool facilitates signing your Git commits and verifying commits from others in your team.

**Scenario 1: Individual Setup and Signing**

1.  **Alice (you) initializes the tool:**

    ```bash
    dilithium-signer init --level 2 --email alice@example.com
    ```

      * This creates a unique Dilithium key pair (private and public) for Alice.
      * The private key is stored securely at `~/.dilithium-signer/keys.json`.
      * Alice's public key is also added to her local "registry" (`~/.dilithium-signer/registry/alice@example.com.json`).
      * A `post-commit` Git hook is set up in the current Git repository to automatically sign new commits.

2.  **Alice makes a commit:**

    ```bash
    git commit -m "My important feature"
    ```

      * The `post-commit` hook automatically runs `dilithium-signer sign <new_commit_hash>`.
      * The commit is signed using Alice's private key.
      * The signature, along with Alice's email, is stored in Git notes (`refs/notes/signatures`) associated with the commit.

**Scenario 2: Sharing Your Public Key and Team Verification**

1.  **Alice exports her public key:**

    ```bash
    dilithium-signer export-key --output alice_public_key.json
    ```

      * Alice sends the `alice_public_key.json` file to her teammate, Bob.

2.  **Bob imports Alice's public key:**

      * Bob needs to have `dilithium-git-signer` installed on his machine.
      * Bob runs:
        ```bash
        dilithium-signer import-key /path/to/alice_public_key.json
        ```
      * Alice's public key is now stored in Bob's local registry (`~/.dilithium-signer/registry/alice@example.com.json`).

3.  **Bob fetches Alice's changes and verifies a commit:**

      * Bob pulls Alice's branch, which includes her signed commits and their associated Git notes.
      * Bob can then verify a specific commit from Alice:
        ```bash
        dilithium-signer verify <commit_hash_from_alice>
        ```
      * The tool uses Alice's public key (from Bob's registry) to check the signature stored in the Git notes for that commit. Bob will see a "Valid" or "Invalid" message.

**Scenario 3: Manual Signing**

If automatic signing via the hook is disabled, or if you want to sign an older commit:

```bash
dilithium-signer sign <commit_hash_to_sign>
```

This requires you to have run `init` or `keygen` previously to have a private key.


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
