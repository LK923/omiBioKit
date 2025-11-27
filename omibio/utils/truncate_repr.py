def truncate_repr(seq: str | None, max_len: int = 30) -> str | None:
    if not seq:
        return None
    if len(seq) <= max_len:
        return repr(seq)
    half = (max_len - 3) // 2
    truncated = seq[:half] + "..." + seq[-half:]
    return repr(truncated)


def main():
    seq = None
    print(truncate_repr(seq))


if __name__ == "__main__":
    main()
