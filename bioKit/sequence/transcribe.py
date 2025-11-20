def main():
    print(transcribe("ACTG", strand="+"))


def transcribe(seq: str, strict: bool = True, strand: str = "+") -> str:
    """Transcribe a seq sequence to RNA.

    Args:
        seq (str): input seq sequence
        strict (bool, optional):
        If True, validate the sequence for valid bases. Defaults to True.
        strand (str, optional):
        Sense or antisense, either '+' or '-'. Defaults to '+'.

    Raises:
        TypeError: if seq is not a string or strick is not a bool
        ValueError: if strand is invalid
        ValueError: if invalid bases are found in strict mode

    Returns:
        str: transcribed RNA sequence
    """

    if not seq:
        return ""
    if not isinstance(seq, str):
        raise TypeError(f"Expected str, got {type(seq).__name__}")
    if not isinstance(strict, bool):
        raise TypeError(f"Expected bool, got {type(seq).__name__}")
    if strand not in ["+", "-"]:
        raise ValueError("strand should be either '+' or '-'")

    seq = seq.upper()

    if strict:
        valid = {"A", "C", "T", "G"}
        if invalid := set(seq) - valid:
            raise ValueError(f"Invalid base(s): {invalid}")

    if strand == "+":
        table = str.maketrans("T", "U")
        return seq.translate(table)
    else:
        table = str.maketrans("ACTG", "UGAC")
        return seq.translate(table)[::-1]


if __name__ == "__main__":
    main()
