from omibio.bioObjects.seq_interval import SeqInterval
from omibio.sequence.sequence import Sequence


def sliding_gc(
    seq: Sequence | str,
    window: int = 100,
    step: int = 10,
    seq_id: str | None = None
) -> list[SeqInterval]:
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
    from omibio.sequence.sequence import Sequence
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
        return [
            SeqInterval(
                start=0, end=n, gc=gc_percent, type="GC", seq_id=seq_id
            )
        ]

    is_gc = [1 if b in 'GC' else 0 for b in seq]

    gc_count = sum(is_gc[:window])
    gc_list = [
        SeqInterval(
            start=0, end=window,
            gc=round((gc_count / window) * 100, 2), type="GC", seq_id=seq_id
        )
    ]

    for i in range(step, n - window + 1, step):
        gc_count -= sum(is_gc[i-step: i])
        gc_count += sum(is_gc[i+window-step: i+window])

        gc_percent = round((gc_count / window) * 100, 2)
        gc_list.append(
            SeqInterval(
                start=i, end=i+window,
                gc=gc_percent, type="GC", seq_id=seq_id
                )
        )

    return gc_list


def main():
    from omibio.io.read_fasta import read
    seq = read("./examples/data/example_single_long_seq.fasta")["example"]
    gc_list = sliding_gc(seq)
    print(gc_list)


if __name__ == "__main__":
    main()
