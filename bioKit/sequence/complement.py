def complement(seq: str, reversed: bool = False) -> str:
    if not seq:
        return ""
    if not isinstance(seq, str):
        raise TypeError(f"Expected str, got {type(seq).__name__}")
    if invalid := set(seq) - {"A", "C", "T", "G", "N"}:
        raise ValueError(f"Invalid base(s): {invalid}")

    table = str.maketrans("ATCG", "TAGC")
    return (seq.translate(table) if not reversed
            else seq.translate(table)[::-1])


def main():
    seq = "NATCG"
    print(complement(seq, reversed=True))


if __name__ == "__main__":
    main()
