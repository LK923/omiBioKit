import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from omibio.bio import SeqInterval
from omibio.bio.analysis_result import AnalysisResult


def plot_sliding_gc(
    gc_list: list[SeqInterval] | AnalysisResult,
    window_avg: bool = True,
    ax: Axes | None = None,
    show: bool = False,
    seq_id: str | None = None,
    figsize: tuple = (9, 3)
) -> Axes:
    """Visualize GC content from sliding window analysis.

    Args:
        gc_list (list[tuple]): List of tuples with (start, end, GC%).
        seq (Sequence | str | None, optional):
            Original sequence for total GC content reference.
            If seq, the total GC content of the sequence will be plotted
            in the chart. Defaults to None.
        window_avg (bool, optional):
            Whether to plot window average GC content.Defaults to True.

    Raises:
        TypeError:
            If seq is not Sequence or str.
    """
    if not gc_list:
        if ax is None:
            ax = plt.subplots(figsize=figsize)[1]
        return ax

    if isinstance(gc_list, AnalysisResult):
        seq_id = seq_id or gc_list.seq_id

    positions = [
        (window.start + window.end) / 2
        for window in gc_list if window.gc is not None
    ]
    gc_vals = [
        window.gc for window in gc_list
        if window.gc is not None
    ]
    window_average = sum(gc_vals) / len(gc_vals)

    if ax is None:
        ax = plt.subplots(figsize=(9, 3))[1]

    if window_avg:
        ax.axhline(
            y=window_average, color="#E14040",
            linestyle='--', label=f'Window average GC%: {window_average:.2f}'
        )

        ax.plot(positions, gc_vals, color="#005AEB", linewidth=1)

    if seq_id is not None:
        ax.set_title(f"Sliding Window GC% of {seq_id}")
    else:
        ax.set_title("Sliding Window GC%")
    ax.set_xlabel("Position in Sequence")
    ax.set_ylabel("GC%")
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper right')

    if show:
        plt.show()
    return ax


def main():
    from omibio.analysis.sliding_gc import sliding_gc
    from omibio.io.read_fasta import read_fasta
    seq = read_fasta(
        "./examples/data/example_single_long_seq.fasta"
    )["example"]
    gc_list = sliding_gc(seq, seq_id="test")
    plot_sliding_gc(gc_list)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
