import click
from omibio.cli.kmer_cli import kmer_group
from omibio.io import read_fasta_iter
from omibio.analysis import kmer
from collections import Counter
import sys


@kmer_group.command(name="kmer")
@click.argument(
    "fasta_file",
    type=click.File("r"),
    required=False
)
@click.option(
    "-k",
    type=int,
    required=True
)
@click.option(
    "--min-count", "-min",
    type=int,
    default=1
)
@click.option(
    "--top",
    type=int,
    default=10
)
@click.option(
    "--canonical", "-c",
    is_flag=True
)
def count(
    fasta_file,
    k: int,
    min_count: bool,
    canonical: bool,
    top: int
):
    """Count k-mers in a FASTA file."""
    fh = fasta_file or sys.stdin
    entries = read_fasta_iter(fh)

    total_counts: dict[str, int] = Counter()
    total = 0

    for entry in entries:
        counts = kmer(
            entry.seq, k=k, canonical=canonical, min_count=min_count
        )
        for km, c in counts.items():
            total_counts[km] += c
            total += c

    tops = sorted(
        total_counts.keys(), key=lambda n: total_counts[n], reverse=True
    )

    click.echo(f"k = {k}")
    click.echo(f"Total:\t{k}")
    click.echo(f"Unique:\t{len(total_counts)}\n")
    for top_kmer in tops[:top]:
        click.echo(f"{top_kmer}:\t{total_counts[top_kmer]}")
