import click
from omibio.io import read


@click.group
def cli():
    """A lightweight and easy-to-use python bioinformatics toolkit"""
    pass


@cli.command()
@click.argument("fasta_file", type=click.Path(exists=True))
def gc(fasta_file: str) -> None:
    """"Calculate the GC content of a sequence from a fasta file."""
    seqs = read(fasta_file)
    for name, seq in seqs.items():
        gc_val = seq.gc_content(percent=True)
        click.echo(f"{name}\t{gc_val}")
