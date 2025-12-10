import click
from omibio.io import read_fasta
from omibio.cli.gc_cli import gc_group
from omibio.sequence import Polypeptide
import csv


@gc_group.command()
@click.argument("fasta_file", type=click.Path(exists=True))
@click.option(
    "-o", "--output",
    type=click.Path(),
    default=None,
    help="Output file path."
)
def compute(fasta_file: str, output: str) -> None:
    """Calculate the GC content of a sequence from a FASTA file."""

    seqs = read_fasta(fasta_file, strict=False).seq_dict()
    lines = []

    for name, seq in seqs.items():
        if isinstance(seq, Polypeptide):
            raise TypeError(
                f"Cannot calculate gc for amino acid sequences: {name}"
            )
        gc_val = seq.gc_content(percent=True)
        lines.append((name, gc_val))

    if output is None:
        for line in lines:
            click.echo("\t".join(line))
    else:
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["seq_id", "gc"])
            writer.writerows(lines)
        click.echo(f"Result written to {output}")
