from bioKit.sequence.sequenceAnalysis import Sequence


def complement(seq: Sequence | str, as_str: bool = False) -> str:
    """Complement a given sequence.

    Args:
        seq (Sequence | str): Input sequence.
        as_str (bool, optional):
        Whether to return the result as a string. Defaults to False.

    Raises:
        TypeError: If the input sequence is not of type Sequence or string.

    Returns:
        str: Complemented sequence.
    """

    # Validate input type
    if not isinstance(seq, (Sequence, str)):
        raise TypeError("Sequence must be of type Sequence or string")

    if isinstance(seq, str):
        seq = Sequence(seq)
    res = seq.complement()
    return (res.sequence if as_str is True else res)


def rev_complement(seq: Sequence | str, as_str: bool = False) -> str:
    """Reverse complement a given sequence.

    Args:
        seq (Sequence | str): Input sequence.
        as_str (bool, optional):
        Whether to return the result as a string. Defaults to False.

    Raises:
        TypeError: If the input sequence is not of type Sequence or string.

    Returns:
        str: Reverse complemented sequence.
    """

    # Validate input type
    if not isinstance(seq, (Sequence, str)):
        raise TypeError("Sequence must be of type Sequence or string")

    if isinstance(seq, str):
        seq = Sequence(seq)
    res = seq.rev_complement()
    return (res.sequence if as_str is True else res)


def main():
    seq = "AAU"
    print([complement(seq, as_str=True)])
    print([rev_complement(seq)])


if __name__ == "__main__":
    main()
