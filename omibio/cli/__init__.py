import click


@click.group()
def cli():
    """A lightweight and easy-to-use python bioinformatics toolkit."""
    pass


@cli.command()
def version():
    """Show the version."""
    from omibio import __version__
    click.echo(f"Version: {__version__}")


def register_commands():
    from .fasta_cli import fasta_group
    from .gc_cli import gc_group
    from .orf_cli import orf
    from .random_fasta_cli import random_fasta

    cli.add_command(gc_group, name="gc")
    cli.add_command(fasta_group, name="fasta")
    cli.add_command(orf)
    cli.add_command(random_fasta)


register_commands()
