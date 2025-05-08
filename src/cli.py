import click 
import json
import subprocess
from pathlib import Path
from src.signer import ensure_config_dir, load_keys, generate_keypair, sign_commit, verify_commit, load_public_key
from src.git_integration import run_git_command, setup_hook

@click.group()
@click.option('--verbose', is_flag=True, help="Show detailed polynomial operations")
@click.pass_context
def cli(ctx, verbose):
    """Dilithium Git Commit Signer: Sign and verify Git commits with Dilithium."""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ensure_config_dir()

@cli.command()
@click.option('--level', type=click.Choice(['2', '3', '5']), default='2', help="Dilithium security level")
@click.option('--email', required=True, help="User's email for identification")
def init(level, email):
    """Initialize the signer, generating keys and setting up hooks."""
    keys = load_keys()
    if keys:
        click.confirm("Keys already exist. Overwrite?", abort=True)
    
    keys = generate_keypair(level, email)
    hook_path = setup_hook(email)
    click.echo(f"Generated Dilithium-{level} key pair for {email} and saved to {Path.home() / '.dilithium-signer'}")
    click.echo(f"Installed Git hook at {hook_path}")

@cli.command()
@click.option('--level', type=click.Choice(['2', '3', '5']), default='2', help="Dilithium security level")
@click.option('--email', required=True, help="User's email for identification")
def keygen(level, email):
    """Generate a new Dilithium key pair."""
    keys = generate_keypair(level, email)
    click.echo(f"Generated Dilithium-{level} key pair for {email}: {Path.home() / '.dilithium-signer/keys.json'}")



@cli.command()
@click.argument('commit_hash')
@click.pass_context
def sign(ctx, commit_hash):
    """Sign a Git commit with Dilithium."""
    keys = load_keys()
    if not keys:
        raise click.ClickException("No keys found. Run 'init' or 'keygen' first.")
    
    sk = bytes.fromhex(keys['secret_key'])
    email = keys['email']
    level = keys['level']
    
    # Get commit message
    commit_msg = run_git_command(['show', '-s', '--format=%B', commit_hash]).encode()
    
    # Sign commit
    sig = sign_commit(commit_msg, sk, level, ctx.obj['verbose'])
    
    # Store signature and email in Git notes
    note_data = json.dumps({"email": email, "signature": sig.hex()})
    run_git_command(['notes', '--ref=signatures', 'add', '-f', '-m', note_data, commit_hash])
    click.echo(f"Signed commit {commit_hash} with Dilithium-{level} by {email}")

@cli.command()
@click.argument('commit_hash')
@click.pass_context
def verify(ctx, commit_hash):
    """Verify a Git commit's Dilithium signature."""
    # Get signature and email from Git notes
    try:
        note_data = run_git_command(['notes', '--ref=signatures', 'show', commit_hash])
        note_json = json.loads(note_data)
        email = note_json['email']
        sig_hex = note_json['signature']
        sig = bytes.fromhex(sig_hex)
    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
        raise click.ClickException("No valid signature found for this commit.")
    
    # Load public key from registry
    key_data = load_public_key(email)
    if not key_data:
        raise click.ClickException(f"No public key found for {email}. Import it with 'import-key'.")
    
    pk = bytes.fromhex(key_data['public_key'])
    level = key_data['level']
    
    # Get commit message
    commit_msg = run_git_command(['show', '-s', '--format=%B', commit_hash]).encode()
    
    # Verify signature
    is_valid = verify_commit(commit_msg, sig, pk, level, ctx.obj['verbose'])
    click.echo(f"Signature verification for {commit_hash} by {email}: {'Valid' if is_valid else 'Invalid'}")


if __name__ == '__main__':
    cli()