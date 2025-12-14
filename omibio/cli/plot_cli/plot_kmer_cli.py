import click
from collections import defaultdict
from omibio.cli.plot_cli import plot_group
from omibio.viz import plot_kmer
import matplotlib.pyplot as plt
from typing import TextIO, cast
from pathlib import Path
import os
import sys
import csv


@plot_group.command()
@click.argument(
    "source",
    type=click.File("r"),
    required=False
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Directory to save plots"
)
@click.option(
    "--no-show",
    is_flag=True,
    help="Whether not to show the plots."
)
def kmer(
    source: str | TextIO | os.PathLike,
    output: str,
    no_show: bool,
):
    source = source or sys.stdin
    if hasattr(source, "read"):
        fh = cast(TextIO, source)
    else:
        file_path = Path(source)
        if not file_path.exists():
            raise FileNotFoundError(f"File '{source}' not found.")
        fh = open(file_path, "r")

    if output is not None:
        os.makedirs(output, exist_ok=True)

    try:
        results: dict[str, dict[str, int]] = defaultdict(dict)
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            results[row["seq_id"]][row["kmer"]] = int(row["count"])
    finally:
        if not hasattr(source, "read"):
            fh.close()

    plot_kmer(list(results.values()))

    if output is not None:
        plt.tight_layout()
        output_path = os.path.join(
            output, "kmer_heatmap.png"
        )
        plt.savefig(output_path)
        if no_show:
            plt.close()

    if not no_show:
        plt.show()
