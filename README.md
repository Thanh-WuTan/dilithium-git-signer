# Dilithium Git Commit Signer

A CLI tool to sign and verify Git commits using the CRYSTALS-Dilithium post-quantum digital signature scheme, built with [`dilithium-py`](https://www.google.com/search?q=%5Bhttps://github.com/GiacomoPope/dilithium-py%5D\(https://github.com/GiacomoPope/dilithium-py\)).

**Important Note:** This tool is for **educational purposes only** and **should not be used in production environments** due to a lack of side-channel protections.

# Features

  * Generate Dilithium key pairs (private and public keys) for different security levels (2, 3, 5).
  * Sign Git commits with your private key and store signatures in Git notes (`refs/notes/signatures`).
  * Export/import public keys to/from files for team collaboration.
  * Automatic signing via a `post-commit` Git hook.
  * View signatures stored in Git notes.

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

Ensure `~/.local/bin` is in your `PATH` (this is common if you install Python packages for the current user without a virtual environment, or if `pip install .` doesn't automatically place the script in a directory already in your `PATH`):

```bash
export PATH=$PATH:~/.local/bin
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc # For bash users
# For zsh users, use ~/.zshrc instead of ~/.bashrc
# For other shells, consult their documentation
source ~/.bashrc # Or source ~/.zshrc
```

*Note: If you are using a Python virtual environment, the script might already be placed in a location within your `PATH` for that environment, and the `PATH` configuration step above might not be necessary.*

**3. Verify setup**

```bash
dilithium-signer --help
```

You should see a list of available commands if the installation was successful.

# Usage

**Initialize the tool (generate keys and set up the post-commit hook):**

```bash
dilithium-signer init --level 2 --email example@example.com
```

  * `--level`: Dilithium security level (choose 2, 3, or 5). Defaults to 2.
  * `--email`: Your email for signature identification.

**Export public key to share:**

```bash
dilithium-signer export-key --output </path/to/output_file.json>
```

Example: `dilithium-signer export-key --output my_public_key.json`

**Save a public key to local registry:**

```bash
dilithium-signer import-key <path/to/public_key_file.json>
```

**List public keys in local registry:**

```bash
dilithium-signer list-keys
```

**Sign a commit (automatic via the post-commit hook or manual):**

```bash
# Automatically (after running 'init' in the Git repository):
git commit -m "Commit message"

# Or manually:
dilithium-signer sign <commit-hash>
```

**Verify a commit:**

```bash
dilithium-signer verify <commit-hash>
```

**View a commit’s signature:**
Signatures are stored in Git notes (reference `refs/notes/signatures`). View with:

```bash
git notes --ref=signatures show <commit-hash>
```

Example output:

```json
{"email": "example@example.com", "signature": "<hex_signature_string>"}
```

**Manually set up hook (if needed):**
If you don't want to run `init` but still want to set up the auto-signing hook in the current Git repository (assuming you already have keys from `keygen`):

```bash
dilithium-signer setup-hook
```

# Command Outputs and Data Formats

Understanding the output of commands and the structure of data files can be helpful.

**1. General Command Output:**

  * **Success:** Most commands provide a clear confirmation message upon successful execution.

      * `init`: "Generated Dilithium-2 key pair for example@example.com..." and "Installed Git hook at..."
      * `keygen`: "Generated Dilithium-2 key pair for example@example.com..."
      * `sign`: "Signed commit \<commit\_hash\> with Dilithium-2 by example@example.com"
      * `verify`: "Signature verification for \<commit\_hash\> by example@example.com: Valid" (or "Invalid")
      * `export-key`: "Exported public key to \<output\_file\>"
      * `import-key`: "Imported public key for example@example.com to registry"
      * `setup-hook`: "Installed Git hook at \<hook\_path\>"

  * **Errors:** If a command fails, it will typically output an error message. Common errors include:

      * "Error: No keys found. Run 'init' or 'keygen' first." (e.g., when trying to `sign` or `export-key` without keys)
      * "Error: No valid signature found for this commit." (e.g., when `verify`ing an unsigned commit)
      * "Error: No public key found for example@example.com." (e.g., when `verify`ing a commit from an unknown signer)
      * "Error: Invalid key file format..." (e.g., when `import-key`ing a malformed file)
      * Git-related errors if Git commands fail.

**2. Data File Formats:**

All data files are stored in JSON format.

  * **User's Key Pair (`~/.dilithium-signer/keys.json`):**

      * This file stores your primary key pair and email. **The `secret_key` should be kept confidential.**

    <!-- end list -->

    ```json
    {
        "public_key": "a1b2c3d4...", // Your public key (hexadecimal string)
        "secret_key": "e5f6g7h8...", // Your private key (hexadecimal string) - KEEP THIS SECRET!
        "level": "2",                 // Dilithium security level (e.g., "2", "3", "5")
        "email": "example@example.com"  // Your email address
    }
    ```

  * **Exported Public Key File (e.g., `my_public_key.json`):**

      * This file contains only the public information safe to share.

    <!-- end list -->

    ```json
    {
        "email": "example@example.com",
        "public_key": "a1b2c3d4...", // Public key (hexadecimal string)
        "level": "2"                  // Dilithium security level
    }
    ```

  * **Local Public Key Registry (`~/.dilithium-signer/registry/<email>.json`):**

      * When you import someone's public key, it's stored in this directory, with one file per email. The format is identical to the exported public key file. Your own public key is also stored here after `init` or `keygen`.

  * **Git Notes Data (for a specific commit):**

      * As shown in the `Usage` section, `git notes --ref=signatures show <commit-hash>` will display a JSON string like this:

    <!-- end list -->

    ```json
    {"email": "example@example.com", "signature": "c8d9e0f1..."}
    ```

      * `email`: Email of the signer.
      * `signature`: The Dilithium signature for the commit (hexadecimal string).

**3. `list-keys` Output:**
The `list-keys` command displays public keys from your local registry in a tabular format:

```
Public Keys in Registry:
------------------------------------------------------------
Email                          Public Key (truncated) Level
------------------------------------------------------------
example@example.com              a1b2c3d4e5f6g7h8...    2
another.user@domain.com        1x2y3z4w5v6u7t8s...    3
------------------------------------------------------------
```

# Uninstallation and Hook Removal

To stop using the tool:

**1. Remove the Git hook (in each Git repository where you ran `init` or `setup-hook`):**
Navigate to the root directory of the Git repository and run:

```bash
rm .git/hooks/post-commit
```

Verify it’s gone:

```bash
ls .git/hooks/post-commit
```

(The `ls` command will report an error like "No such file or directory" if successfully removed).

**2. Uninstall the package:**

```bash
pip uninstall dilithium-git-signer -y
```

**3. Remove configuration files:**
This action will delete all your keys and configurations for this tool.

```bash
rm -rf ~/.dilithium-signer/
```

# Acknowledgments

  * Built with `dilithium-py`, a pure-Python implementation of CRYSTALS-Dilithium.
  * Inspired by post-quantum cryptography research and Git workflows.

-----