from omibio.bioObjects.seq_interval import SeqInterval


def same_seq_as(a, b) -> bool:
    """Checks if two SeqInterval instances are on the same sequence."""
    if not isinstance(a, SeqInterval) or not isinstance(b, SeqInterval):
        return False
    return a.seq_id == b.seq_id


def overlaps(a: SeqInterval, b: SeqInterval) -> bool:
    """Checks if two SeqInterval instances overlap."""
    if not same_seq_as(a, b):
        return False
    return a.start < b.end and b.start < a.end


def contains(a: SeqInterval, b: int | SeqInterval) -> bool:
    """
    Checks if the SeqInterval contains a position or another SeqInterval.
    """
    if isinstance(b, int):
        return a.start <= b < a.end

    elif isinstance(b, SeqInterval):
        return (
            a.start <= b.start and b.end <= a.end
            and a.seq_id == b.seq_id
        )

    else:
        return False


def distance_to(a: SeqInterval, b: SeqInterval) -> int:
    """Calculates the distance to another SeqInterval."""
    if not isinstance(b, SeqInterval):
        raise TypeError(
            "distance_to() argument 'other' must be SeqInterval, got "
            + type(b).__name__
        )
    if not same_seq_as(a, b):
        raise ValueError(
            "Cannot compare the distance between intervals "
            "on two different sequences: "
            f"{a.seq_id!r} vs {b.seq_id!r}"
        )

    if overlaps(a, b):
        return 0
    if a.start >= b.end:
        return a.start - b.end
    else:
        return b.start - a.end


def main():
    seq1 = SeqInterval(start=6, end=12)
    seq2 = SeqInterval(start=3, end=19)
    print(overlaps(seq1, seq2))
    print(same_seq_as(seq1, seq2))
    print(distance_to(seq1, seq2))
    print(contains(seq1, seq2))
    print(contains(seq1, 9))


if __name__ == "__main__":
    main()
