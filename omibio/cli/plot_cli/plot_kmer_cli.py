import click
from omibio.cli.plot_cli import plot_group
from omibio.viz import plot_kmer
from omibio.bio import KmerResult
import matplotlib.pyplot as plt
from typing import TextIO
from csv import DictReader
import os


@plot_group.command()
@click.argument(
    "source",
    type=click.File("r"),
    required=False,
    default="-",
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Directory to save plots"
)
@click.option(
    "--cmap",
    type=str,
    default="viridis",
    help="Colormap to use for the heatmap."
)
@click.option(
    "--fmt",
    type=str,
    default=".2f",
    help="Format string for heatmap annotations."
)
@click.option(
    "--no-annot",
    is_flag=True,
    help="Whether to disable annotations on the heatmap."
)
@click.option(
    "--no-show",
    is_flag=True,
    help="Whether not to show the plots."
)
def kmer(
    source: TextIO,
    output: str,
    no_show: bool,
    cmap: str,
    fmt: str,
    no_annot: bool
):
    """Plot k-mer counts from a TSV file."""

    if output is not None:
        os.makedirs(output, exist_ok=True)

    results: dict[str, KmerResult] = {}
    reader = DictReader(source, delimiter="\t")
    for row in reader:
        seq_id = str(row["seq_id"])
        if seq_id not in results:
            results[seq_id] = KmerResult(
                k=int(row["k"]), counts={row["kmer"]: int(row["count"])},
                seq_id=seq_id
            )
        else:
            if int(row["k"]) != results[seq_id].k:
                raise ValueError(
                    "Got inconsistent k values: "
                    f"{row['k']} vs {results[seq_id].k}"
                )
            results[seq_id].counts[row["kmer"]] = int(row["count"])

    plot_kmer(list(results.values()), cmap=cmap, fmt=fmt, annot=not no_annot)

    if output is not None:
        plt.tight_layout()
        output_path = os.path.join(
            output, "kmer_heatmap.png"
        )
        plt.savefig(output_path)
        if no_show:
            plt.close()

    if not no_show:
        plt.tight_layout()
        plt.show()
