from fastaReader import read
import matplotlib.pyplot as plt


def gcContent(
    seq: str, percent: bool = False, accuracy: int = 5
) -> float | str:
    seq = seq.upper()
    gc_content = (seq.count("C") + seq.count("G")) / len(seq)

    return (round(gc_content, accuracy) if not percent
            else f"{gc_content * 100:.2f}%")


def sliding_gc(seq: str, window: int = 100, step: int = 10) -> list[tuple]:
    if window <= 0 or step <= 0:
        raise ValueError("window and step should be positive numbers")
    if window >= len(seq):
        return gcContent(seq)

    seq = seq.upper()

    first_window = seq[:window]
    gc_count = sum(1 for b in first_window if b in 'GC')
    gc_list = [((0, window, round(gcContent(first_window) * 100, 2)))]

    for i in range(step, len(seq) - window + 1, step):
        bases_seen = seq[i-step: i]
        gc_count -= sum(1 for b in bases_seen if b in 'GC')

        new_bases = seq[i+window-step: i+window]
        gc_count += sum(1 for b in new_bases if b in 'GC')

        gc_percent = round(gc_count / window * 100, 2)
        gc_list.append((i, i+window, gc_percent))

    return gc_list


def draw_sliding_gc(gc_list: list[tuple]) -> None:
    positions = [(start + end) / 2 for start, end, _ in gc_list]
    gc_vals = [gc for _, _, gc in gc_list]
    avg_gc = sum(gc_vals)/len(gc_vals)

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
    draw_sliding_gc(sliding_gc(sequence))


if __name__ == "__main__":
    main()
