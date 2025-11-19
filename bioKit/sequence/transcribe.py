def main():
    print(transcribe("ACTG", strand="+"))


def transcribe(dna: str, strict: bool = True, strand: str = "+") -> str:
    """Transcribe a DNA sequence to RNA.

    Args:
        dna (str): input DNA sequence
        strict (bool, optional):
        If True, validate the sequence for valid bases. Defaults to True.
        strand (str, optional):
        Sense or antisense, either '+' or '-'. Defaults to '+'.

    Raises:
        TypeError: if dna is not a string or strick is not a bool
        ValueError: if strand is invalid
        ValueError: if invalid bases are found in strict mode

    Returns:
        str: transcribed RNA sequence
    """

    if not dna:
        return ""
    if not isinstance(dna, str):
        raise TypeError(f"Expected str, got {type(dna).__name__}")
    if not isinstance(strict, bool):
        raise TypeError(f"Expected bool, got {type(dna).__name__}")
    if strand not in ["+", "-"]:
        raise ValueError("strand should be either '+' or '-'")

    dna = dna.upper()

    if strict:
        valid = {"A", "C", "T", "G"}
        if invalid := set(dna) - valid:
            raise ValueError(f"Invalid base(s): {invalid}")

    if strand == "+":
        table = str.maketrans("T", "U")
        return dna.translate(table)
    else:
        table = str.maketrans("ACTG", "UGAC")
        return dna.translate(table)[::-1]


if __name__ == "__main__":
    main()
