from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from omibio.sequence.sequence import Sequence


def gc(seq: Union["Sequence", str], percent: bool = False) -> float | str:
    """Calculate the GC content of a sequence.

    Args:
        seq (str):
            input sequence
        percent (bool, optional):
            If True, return GC content as a percentage string.
            Defaults to False.

    Returns:
        float | str: GC content as a float or percentage string.
    """
    from omibio.sequence.sequence import Sequence
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "gc() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )
    if isinstance(seq, Sequence):
        return seq.gc_content(percent=percent)
    elif isinstance(seq, str):
        gc_content = (seq.count("C") + seq.count("G")) / len(seq)
        return (
            round(gc_content, 4) if not percent
            else f"{round(gc_content * 100, 2)}%"
        )


def main():
    print(gc("AC"))
    print(gc("AC", percent=True))


if __name__ == "__main__":
    main()
