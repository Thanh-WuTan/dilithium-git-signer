import json
from pathlib import Path
from dilithium_py.dilithium import Dilithium2, Dilithium3, Dilithium5

# Configuration
CONFIG_DIR = Path.home() / ".dilithium-signer"
KEY_FILE = CONFIG_DIR / "keys.json"
REGISTRY_DIR = CONFIG_DIR / "registry"

# Dilithium security levels
SECURITY_LEVELS = {
    "2": Dilithium2,
    "3": Dilithium3,
    "5": Dilithium5
}

def ensure_config_dir():
    """Create configuration and registry directories if they don't exist."""
    CONFIG_DIR.mkdir(exist_ok=True)
    REGISTRY_DIR.mkdir(exist_ok=True)

def load_keys():
    """Load user's key pair from config file."""
    if not KEY_FILE.exists():
        return None
    with open(KEY_FILE, 'r') as f:
        return json.load(f)
    return None

def save_keys(keys):
    """Save user's key pair to config file."""
    with open(KEY_FILE, 'w') as f:
        json.dump(keys, f)

def save_public_key(email, public_key, level):
    """Save a public key to the registry."""
    key_file = REGISTRY_DIR / f"{email}.json"
    with open(key_file, 'w') as f:
        json.dump({"email": email, "public_key": public_key, "level": level}, f)

def load_public_key(email):
    """Load a public key from the registry by email."""
    key_file = REGISTRY_DIR / f"{email}.json"
    if not key_file.exists():
        return None
    with open(key_file, 'r') as f:
        return json.load(f)
    return None

def generate_keypair(level, email):
    """Generate a new Dilithium key pair and save it."""
    dilithium = SECURITY_LEVELS[level]
    pk, sk = dilithium.keygen()
    keys = {
        "public_key": pk.hex(),
        "secret_key": sk.hex(),
        "level": level,
        "email": email
    }
    save_keys(keys)
    save_public_key(email, pk.hex(), level)
    return keys

def sign_commit(commit_msg, sk, level):
    """Sign a commit message using Dilithium."""
    dilithium = SECURITY_LEVELS[level]
    sig = dilithium.sign(sk, commit_msg)
    return sig

def verify_commit(commit_msg, sig, pk, level):
    """Verify a commit's Dilithium signature."""
    dilithium = SECURITY_LEVELS[level]
    return dilithium.verify(pk, commit_msg, sig)