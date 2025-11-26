def truncate_repr(seq: str, max_len: int = 30) -> str:
    if len(seq) <= max_len:
        return repr(seq)
    half = (max_len - 3) // 2
    truncated = seq[:half] + "..." + seq[-half:]
    return repr(truncated)


def main():
    seq = "ACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTG"
    print(truncate_repr(seq))


if __name__ == "__main__":
    main()
