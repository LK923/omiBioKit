from omibio.sequence import Polypeptide


def get_formula(aa_seq: Polypeptide | str) -> str:
    """Return the molecular formula of a polypeptide sequence.

    Args:
        aa_seq (Polypeptide | str):
            A polypeptide sequence as a Polypeptide object or a string.

    Raises:
        TypeError:
            If aa_seq is not a Polypeptide object or a string.

    Returns:
        str:
            The molecular formula of the polypeptide sequence.
    """
    if not isinstance(aa_seq, (Polypeptide, str)):
        raise TypeError(
            "get_formula() argument 'aa_seq' must be Polypeptide or str, got "
            + type(aa_seq).__name__
        )
    if isinstance(aa_seq, str):
        aa_seq = Polypeptide(aa_seq)
    return aa_seq.formula()


def main():
    aa_seq = "MALPSSCHW"
    print(get_formula(aa_seq))


if __name__ == "__main__":
    main()
