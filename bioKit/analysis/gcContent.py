import matplotlib.pyplot as plt
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from bioKit.sequence.sequenceAnalysis import Sequence


def gc(seq: Union["Sequence", str], percent: bool = False) -> float | str:
    """Calculate the GC content of a DNA sequence.

    Args:
        seq (str): input sequence
        percent (bool, optional):
        If True, return GC content as a percentage string. Defaults to False.

    Returns:
        float | str: GC content as a float or percentage string.
    """
    from bioKit.sequence.sequenceAnalysis import Sequence
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "gc() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )
    if isinstance(seq, str):
        seq = Sequence(seq)

    return seq.gc_content(percent=percent)


def sliding_gc(
    seq: Union["Sequence", str],
    window: int = 100,
    step: int = 10
) -> list[tuple]:
    """Calculate GC content in a sliding window manner.

    Args:
        seq (str): input sequence
        window (int, optional): window size. Defaults to 100.
        step (int, optional): step size. Defaults to 10.

    Raises:
        ValueError: if window or step is not positive.
        TypeError: if seq is not a string.

    Returns:
        list[tuple]: A list of tuples, each containing (start, end, GC%).
    """
    from bioKit.sequence.sequenceAnalysis import Sequence
    if not seq:
        return []
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "sliding_gc() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )
    if window <= 0 or step <= 0:
        raise ValueError("window and step should be positive numbers")
    if isinstance(seq, Sequence):
        seq = str(seq)

    n = len(seq)
    seq = seq.upper()

    if window >= n:
        gc_count = sum(1 for b in seq if b in 'GC')
        gc_percent = round((gc_count / n) * 100, 2)
        return [(0, n, gc_percent)]

    is_gc = [1 if b in 'GC' else 0 for b in seq]

    gc_count = sum(is_gc[:window])
    gc_list = [(0, window, round((gc_count / window) * 100, 2))]

    for i in range(step, n - window + 1, step):
        gc_count -= sum(is_gc[i-step: i])
        gc_count += sum(is_gc[i+window-step: i+window])

        gc_percent = round((gc_count / window) * 100, 2)
        gc_list.append((i, i+window, gc_percent))

    return gc_list


def draw_sliding_gc(
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
        TypeError: _description_
    """
    from bioKit.sequence.sequenceAnalysis import Sequence
    if not gc_list:
        return
    if seq:
        if not isinstance(seq, (Sequence, str)):
            raise draw_sliding_gc(
                "sliding_gc() argument 'seq' must be Sequence or str, not "
                + type(seq).__name__
            )
        if isinstance(seq, str):
            seq = Sequence(seq)
        total_avg = seq.gc_content() * 100

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
    from bioKit.sequence.sequenceAnalysis import Sequence  # noqa
    print(gc("AGCTAGCTAGTCGTAC"))


if __name__ == "__main__":
    main()
