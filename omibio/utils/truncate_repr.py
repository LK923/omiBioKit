def truncate_repr(seq: str | None, max_len: int = 30) -> str | None:
    """Truncate a sequence representation if it exceeds max_len.

    Args:
        seq (str | None):
            The sequence to truncate.
        max_len (int, optional):
            Maximum length of the representation. Defaults to 30.

    Returns:
        str | None:
            Truncated representation of the sequence or None if seq is None.
    """
    if not seq:
        return None
    if len(seq) <= max_len or max_len <= 3:
        return repr(seq)
    half = (max_len - 3) // 2
    truncated = seq[:half] + "..." + seq[-half:]
    return repr(truncated)


def main():
    seq = "AGCTATGCTGATGCTAGTCTGATGCTGTAGTGCTAGTCTGTAGCACGATGCGAGTCACGATCTGATG"
    print(truncate_repr(seq))
    print(truncate_repr(None))


if __name__ == "__main__":
    main()
