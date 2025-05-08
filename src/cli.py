import click 
from pathlib import Path
from src.signer import ensure_config_dir, load_keys, generate_keypair
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


if __name__ == '__main__':
    cli()