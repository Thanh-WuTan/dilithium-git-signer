import pytest
from src.signer import generate_keypair, sign_commit, verify_commit, load_public_key
from src.signer import CONFIG_DIR, KEY_FILE, REGISTRY_DIR

@pytest.fixture
def setup_keys(tmp_path):
    """Set up temporary key directory."""
    config_dir = tmp_path / ".dilithium-signer"
    config_dir.mkdir()
    registry_dir = config_dir / "registry"
    registry_dir.mkdir()
    
    # Override config paths
    
    global CONFIG_DIR, KEY_FILE, REGISTRY_DIR
    CONFIG_DIR = config_dir
    KEY_FILE = CONFIG_DIR / "keys.json"
    REGISTRY_DIR = CONFIG_DIR / "registry"
    
    return config_dir

def test_generate_keypair(setup_keys):
    """Test key pair generation and storage."""
    keys = generate_keypair("2", "alice@example.com")
    assert keys["email"] == "alice@example.com"
    assert keys["level"] == "2"
    assert len(keys["public_key"]) > 0
    assert len(keys["secret_key"]) > 0
    
    # Check registry
    key_data = load_public_key("alice@example.com")
    assert key_data["email"] == "alice@example.com"
    assert key_data["public_key"] == keys["public_key"]

def test_sign_verify(setup_keys):
    """Test signing and verifying a commit."""
    keys = generate_keypair("2", "alice@example.com")
    commit_msg = b"Test commit"
    sk = bytes.fromhex(keys["secret_key"])
    pk = bytes.fromhex(keys["public_key"])
    
    sig = sign_commit(commit_msg, sk, "2", verbose=False)
    is_valid = verify_commit(commit_msg, sig, pk, "2", verbose=False)
    assert is_valid
    
    # Test with wrong public key
    keys_bob = generate_keypair("2", "bob@example.com")
    pk_bob = bytes.fromhex(keys_bob["public_key"])
    is_valid = verify_commit(commit_msg, sig, pk_bob, "2", verbose=False)
    assert not is_valid