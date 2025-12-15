import click
from omibio.cli.kmer_cli import kmer_group
from omibio.io import read_fasta_iter
from omibio.analysis import kmer
from typing import TextIO
import csv


@kmer_group.command()
@click.argument(
    "source",
    type=click.File("r"),
    required=False,
    default="-"
)
@click.option(
    "-k",
    type=int,
    required=True,
    help="Length of the k-mers to count."
)
@click.option(
    "--min-count", "-min",
    type=int,
    default=1,
    help="Minimum count threshold for k-mers. Defaults to 1."
)
@click.option(
    "--top",
    type=int,
    help="Number of top k-mers to display. Defaults to all."
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Write details to a file in csv format"
)
@click.option(
    "--canonical", "-c",
    is_flag=True,
    help="Whether to count canonical k-mers."
)
@click.option(
    "--no-sort",
    is_flag=True,
    help="Whether nto to sort k-mer results in a decreasing order."
)
def count(
    source: TextIO,
    k: int,
    min_count: bool,
    canonical: bool,
    output: str | None,
    top: int | None,
    no_sort: bool
):
    """Count k-mers for each sequence in a FASTA file."""

    entries = read_fasta_iter(source)

    results: list[list[str | int]] = []

    for entry in entries:
        counts = kmer(
            entry.seq, k=k, canonical=canonical, min_count=min_count
        )
        for km, c in counts.items():
            results.append([entry.seq_id, k, km, c])

    if (not no_sort) or (top is not None):
        tops = sorted(
            results, reverse=True, key=lambda res: res[-1]
        )
    else:
        tops = results

    if top is not None:
        rows = [["seq_id", "k", "kmer", "count"]] + tops[:top]
    else:
        rows = [["seq_id", "k", "kmer", "count"]] + tops
    if output is not None:
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerows(rows)
            click.echo(f"Written to {output}")
    else:
        for row in rows:
            click.echo("\t".join(map(str, row)))
