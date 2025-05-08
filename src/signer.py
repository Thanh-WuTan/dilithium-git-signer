from pathlib import Path
from dilithium_py.dilithium import Dilithium2, Dilithium3, Dilithium5

# Configuration
CONFIG_DIR = Path.home() / ".dilithium-signer"
KEY_FILE = CONFIG_DIR / "keys.json"
REGISTRY_DIR = CONFIG_DIR / "registry"

def ensure_config_dir(): 
    CONFIG_DIR.mkdir(exist_ok=True)
    REGISTRY_DIR.mkdir(exist_ok=True)
