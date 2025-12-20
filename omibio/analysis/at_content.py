from omibio.sequence.sequence import Sequence
from omibio.utils import to_percentage


def at(seq: Sequence | str, percent: bool = False) -> float | str:
    """Calculate the AT content of a sequence.

    Args:
        seq (Sequence | str):
            input sequence
        percent (bool, optional):
            If True, return AT content as a percentage string.
            Defaults to False.

    Returns:
        float | str: AT content as a float or percentage string.
    """
    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "at() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )
    if isinstance(seq, Sequence):
        return seq.at_content(percent=percent)
    elif isinstance(seq, str):
        if not seq:
            return 0.0 if not percent else "0.00%"
        at_content = (seq.count("A") + seq.count("T")) / len(seq)
        return (
            round(at_content, 4) if not percent
            else to_percentage(at_content)
        )


def main():
    print(at("ATG", percent=False))


if __name__ == "__main__":
    main()
