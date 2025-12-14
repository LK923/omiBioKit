import click
from omibio.cli.kmer_cli import kmer_group
from omibio.io import read_fasta_iter
from omibio.analysis import kmer
import sys
import csv


@kmer_group.command()
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
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Write details to a file in csv format"
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
    output: str,
    top: int | None,
):
    """Count k-mers in a FASTA file."""
    fh = fasta_file or sys.stdin
    entries = read_fasta_iter(fh)

    results: list[list[str | int]] = []

    for entry in entries:
        counts = kmer(
            entry.seq, k=k, canonical=canonical, min_count=min_count
        )
        for km, c in counts.items():
            results.append([entry.seq_id, k, km, c])

    tops = sorted(
        results, reverse=True, key=lambda res: res[-1]
    )

    if top is not None:
        rows = [["seq_id", "k", "kmer", "count"]] + tops[:top]
    else:
        rows = [["seq_id", "k", "kmer", "count"]] + results
    if output is not None:
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerows(rows)
            click.echo(f"Written to {output}")
    else:
        for row in rows:
            click.echo("\t".join(map(str, row)))
