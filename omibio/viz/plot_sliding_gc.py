import matplotlib.pyplot as plt
from omibio.sequence.sequence import Sequence
from typing import Union


def plot_sliding_gc(
    gc_list: list[tuple],
    seq: Union["Sequence", str, None] = None,
    window_avg: bool = True
) -> None:
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
        return
    if seq:
        if not isinstance(seq, (Sequence, str)):
            raise TypeError(
                "sliding_gc() argument 'seq' must be Sequence or str, not "
                + type(seq).__name__
            )
        if isinstance(seq, str):
            seq = Sequence(seq)
        total_avg = float(seq.gc_content()) * 100

    positions = [(start + end) / 2 for start, end, _ in gc_list]
    gc_vals = [gc for _, _, gc in gc_list]
    window_avg = sum(gc_vals) / len(gc_vals)

    plt.figure(figsize=(10, 4))

    if window_avg:
        plt.axhline(
            y=window_avg, color='cyan',
            linestyle='--', label=f'Window average GC%: {window_avg:.2f}%'
        )
    if seq:
        plt.axhline(
            y=total_avg, color='green',
            linestyle='dotted', label=f'Total average GC%: {total_avg:.2f}%'
        )

    plt.plot(positions, gc_vals, color='blue', linewidth=1)

    plt.title("Sliding Window GC%")
    plt.xlabel("Position in Sequence")
    plt.ylabel("GC%")
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()


def main():
    from omibio.analysis.sliding_gc import sliding_gc
    from omibio.io.read_fasta import read
    seq = read("./examples/data/example_single_long_seq.fasta")["example"]
    gc_list = sliding_gc(seq)
    plot_sliding_gc(gc_list, seq=seq)


if __name__ == "__main__":
    main()
