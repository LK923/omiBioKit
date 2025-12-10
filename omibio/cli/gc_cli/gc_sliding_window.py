import click
from omibio.io import read_fasta
from omibio.cli.gc_cli import gc_group
from omibio.analysis import sliding_gc
from math import ceil
import matplotlib.pyplot as plt
import os
import csv
import warnings


@gc_group.command()
@click.argument("fasta_file", type=click.Path(exists=True))
@click.option(
    "--window", "-w",
    type=int,
    default=100,
    help="window size. Defaults to 100."
)
@click.option(
    "--step", "-s",
    type=int,
    default=10,
    help="step size. Defaults to 10."
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Write details to a file in csv format"
)
@click.option(
    "--save-image-to",
    type=str,
    default=None,
    help=(
        "Wether to save images to a directory. "
    )
)
@click.option(
    "--per-page",
    type=int,
    default=3,
    help="Number of plots per page if saving images. Defaults to 3."
)
@click.option(
    "--show",
    is_flag=True,
    help="Whether to show the plots."
)
@click.option(
    "--no-warn",
    is_flag=True,
    help="Suppress warnings about large memory usage."
)
def sliding_window(
    fasta_file: str,
    window: int,
    step: int,
    save_image_to: str,
    output: str,
    show: bool,
    per_page: int,
    no_warn: bool,
):
    """
    Calculate and plot sliding window GC content for sequences in a FASTA file.
    """

    if save_image_to is not None:
        os.makedirs(save_image_to, exist_ok=True)

    per_page = int(per_page)
    if per_page <= 0:
        raise ValueError(
            "omibio gc sliding-window argument 'per-page' must be a "
            f"non-negative number, got {per_page}"
        )

    entries = read_fasta(fasta_file)
    if (len(entries) > 100) and (save_image_to or show) and (not no_warn):
        warnings.warn(
            f"\033[33mCreating sliding window gc image for {len(entries)} "
            "sequences will consume a large amout of memory\033[0m"
        )
        input("Press enter to confirm...")

    analysis_results = []
    figs = []

    for entry in entries:
        gc_vals = []

        result = sliding_gc(
            entry.seq, window=window, step=step, seq_id=entry.seq_id
        )
        analysis_results.append(result)

        for interval in result:
            if (gc_val := interval.gc) is not None:
                gc_vals.append(gc_val)

        average = sum(gc_vals) / len(gc_vals)
        click.echo(
            f"{entry.seq_id}:\tmean {average:.2f}%, "
            f"max {max(gc_vals)}%, min {min(gc_vals)}%"
        )

    if output is not None:
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["seq_id", "start", "end", "gc%"])
            for res in analysis_results:
                rows = [
                    [itv.seq_id, itv.start, itv.end, itv.gc] for itv in res
                ]
                writer.writerows(rows)
                rows.clear()
        click.echo(f"Written to {output}")

    if (show) or (save_image_to is not None):
        seq_dict = {
            res.seq_id: res for res in analysis_results
        }
        seq_ids = list(seq_dict.keys())
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
                seq_dict[seq_id].plot(ax=ax, figsize=(6, 2))

            if save_image_to is not None:
                fig.tight_layout()
                output_path = os.path.join(
                    save_image_to, f"gc_page_{page+1}.png"
                )
                fig.savefig(output_path)
                if not show:
                    plt.close(fig)
                else:
                    figs.append(fig)
                click.echo(f"Image saved to {output_path}")

        if show:
            plt.show()

        for fig in figs:
            plt.close(fig)
