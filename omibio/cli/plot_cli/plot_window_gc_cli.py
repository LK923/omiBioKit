import click
from omibio.cli.plot_cli import plot_group
from math import ceil
import matplotlib.pyplot as plt
import os
import sys
from typing import TextIO, cast
from pathlib import Path
import csv
from omibio.bio import SeqInterval
from omibio.viz import plot_sliding_gc
from collections import defaultdict


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
    "--per-page", "-p",
    type=int,
    default=3,
    help="Number of plots per page if saving images. Defaults to 3."
)
@click.option(
    "--no-show",
    is_flag=True,
    help="Whether not to show the plots."
)
def window(
    source: str | TextIO | os.PathLike,
    output: str,
    no_show: bool,
    per_page: int
):
    """
    Calculate and plot sliding window GC content for sequences in a FASTA file.
    """

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

    figs = []

    per_page = int(per_page)
    if per_page <= 0:
        raise ValueError(
            "omibio gc sliding-window argument 'per-page' must be a "
            f"non-negative number, got {per_page}"
        )

    try:
        analysis_results = defaultdict(list)
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            analysis_results[row["seq_id"]].append(
                SeqInterval(
                    start=int(row["start"]), end=int(row["end"]),
                    seq_id=row["seq_id"], gc=float(row["gc"])
                )
            )
    finally:
        if not hasattr(source, "read"):
            fh.close()

    seq_ids = list(analysis_results.keys())
    per_page = per_page
    page_num = ceil(len(seq_ids) / per_page)

    for page in range(page_num):
        start = page * per_page
        end = start + per_page
        page_seq_ids = seq_ids[start: end]
        n = len(page_seq_ids)
        fig, axes = plt.subplots(n, 1, figsize=(9, 3 * n))

        fig.subplots_adjust(hspace=.5)

        axes = [axes] if n == 1 else axes

        for seq_id, ax in zip(page_seq_ids, axes):
            plot_sliding_gc(
                analysis_results[seq_id], ax=ax, figsize=(6, 2)
            )

        if output is not None:
            fig.tight_layout()
            output_path = os.path.join(
                output, f"gc_page_{page+1}.png"
            )
            fig.savefig(output_path)
            if no_show:
                plt.close(fig)
            else:
                figs.append(fig)
            click.echo(f"Image saved to {output_path}")

    if not no_show:
        plt.show()

    for fig in figs:
        plt.close(fig)
