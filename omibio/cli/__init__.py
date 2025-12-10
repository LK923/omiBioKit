import click


@click.group()
def cli():
    """A lightweight and easy-to-use python bioinformatics toolkit."""
    pass


@cli.command()
def version():
    """Show the version of omibio."""
    from omibio import __version__
    click.echo(f"Version: {__version__}")


def register_commands():
    from .clean_cli import clean
    from .gc_cli import gc_group
    from .orf_cli import orf
    from .shuffle_cli import shuffle
    from .random_fasta_cli import random_fasta

    cli.add_command(clean)
    cli.add_command(gc_group, name="gc")
    cli.add_command(orf)
    cli.add_command(shuffle)
    cli.add_command(random_fasta)


register_commands()
