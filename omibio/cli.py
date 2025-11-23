import click
from omibio.io.fastaReader import read
from omibio.analysis.orfFinder import find_orfs


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


@cli.command()
@click.argument("fasta_file", type=click.Path(exists=True))
def orf(fasta_file: str) -> None:
    """Find orfs of a sequence from a fasta file."""
    seqs = read(fasta_file)
    for name, seq in seqs.items():
        click.echo(f"----------------{name}----------------")
        orfs = find_orfs(seq)
        for orf in orfs:
            start, end = orf.start, orf.end
            strand = orf.strand
            frame = f"{orf.frame:+}" if orf.frame > 0 else orf.frame
            click.echo(
                f"ORF of {name}\t{start}-{end}\t{strand}\t{frame}"
            )
        click.echo(f"Total: {len(orfs)}\n")
