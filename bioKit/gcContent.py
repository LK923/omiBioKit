from fastaReader import read
import matplotlib.pyplot as plt


def gcContent(
    seq: str, percent: bool = False, accuracy: int = 5
) -> float | str:
    """Calculate the GC content of a DNA sequence.

    Args:
        seq (str): input sequence
        percent (bool, optional):
        If True, return GC content as a percentage string. Defaults to False.
        accuracy (int, optional):
        Decimal places for float output. Defaults to 5.

    Returns:
        float | str: GC content as a float or percentage string.
    """

    if not seq:
        return 0.0 if not percent else "0.00%"
    seq = seq.upper()
    gc_content = (seq.count("C") + seq.count("G")) / len(seq)

    return (round(gc_content, accuracy) if not percent
            else f"{gc_content * 100:.2f}%")


def sliding_gc(seq: str, window: int = 100, step: int = 10) -> list[tuple]:
    """Calculate GC content in a sliding window manner.

    Args:
        seq (str): input sequence
        window (int, optional): window size. Defaults to 100.
        step (int, optional): step size. Defaults to 10.

    Raises:
        ValueError: if window or step is not positive.

    Returns:
        list[tuple]: A list of tuples, each containing (start, end, GC%).
    """

    if not seq:
        return []
    if window <= 0 or step <= 0:
        raise ValueError("window and step should be positive numbers")

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


def draw_sliding_gc(gc_list: list[tuple]) -> None:
    positions = [(start + end) / 2 for start, end, _ in gc_list]
    gc_vals = [gc for _, _, gc in gc_list]
    avg_gc = sum(gc_vals) / len(gc_vals)

    plt.figure(figsize=(10, 4))

    plt.axhline(
        y=avg_gc, color='cyan',
        linestyle='--', label=f'Average GC%: {avg_gc:.2f}%'
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
    input_path = r"./data/gc.fa"
    seq_dict = read(input_path)
    sequence = None
    for seq in seq_dict.values():
        sequence = seq
    res = sliding_gc(sequence)
    draw_sliding_gc(res)


if __name__ == "__main__":
    main()
