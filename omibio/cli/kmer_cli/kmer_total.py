import click
from omibio.cli.kmer_cli import kmer_group
from omibio.io import read_fasta_iter
from omibio.analysis import kmer
from collections import Counter
from typing import TextIO
import csv


@kmer_group.command()
@click.argument(
    "source",
    type=click.File("r"),
    required=False,
    default="-",
)
@click.option(
    "-k",
    type=int,
    required=True,
    help="Length of the k-mers to count."
)
@click.option(
    "--top",
    type=int,
    default=None,
    help="Number of top k-mers to display. Defaults to all."
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Directory to save plots",
)
@click.option(
    "--min-count", "-min",
    default=1,
    help="Minimum count threshold for k-mers. Defaults to 1."
)
@click.option(
    "--canonical", "-c",
    is_flag=True,
    help="Whether to count canonical k-mers."
)
@click.option(
    "--summary", "-s",
    is_flag=True,
    help="Whether to print a summary instead of full counts."
)
@click.option(
    "--no-sort",
    is_flag=True,
    help="Whether nto to sort k-mer results in a decreasing order."
)
def total(
    source: TextIO,
    k: int,
    canonical: bool,
    top: int | None,
    summary: bool,
    output: str | None,
    no_sort: bool,
    min_count: int
):
    """Count k-mers in total for all sequence in a FASTA file."""

    entries = read_fasta_iter(source)
    total_counts: dict[str, int] = Counter()
    total = 0

    for entry in entries:
        counts = kmer(
            entry.seq, k=k, canonical=canonical
        )
        for km, c in counts.items():
            total_counts[km] += c
            total += c

    tops = [
        key for key in total_counts.keys()
        if total_counts[key] >= min_count
    ]
    if (not no_sort) or (top is not None):
        tops = sorted(tops, key=lambda n: total_counts[n], reverse=True)

    if summary:
        click.echo(f"k = {k}")
        click.echo(f"Total:\t{k}")
        click.echo(f"Unique:\t{len(total_counts)}\n")
        for top_kmer in tops[:top]:
            click.echo(f"{top_kmer}:\t{total_counts[top_kmer]}")
    else:
        if top is not None:
            results = [
                ["total", k, key, total_counts[key]] for key in tops[:top]
            ]
        else:
            results = [
                ["total", k, key, total_counts[key]] for key in tops
            ]
        rows = [["seq_id", "k", "kmer", "count"]] + results
        if output is not None:
            with open(output, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter="\t")
                writer.writerows(rows)
                click.echo(f"Written to {output}")
        else:
            for row in rows:
                click.echo("\t".join(map(str, row)))
