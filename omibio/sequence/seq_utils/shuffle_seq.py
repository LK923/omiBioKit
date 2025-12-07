import random
from omibio.sequence.sequence import Sequence


def shuffle_seq(
    seq: Sequence | str,
    seed: int | None = None,
    as_str: bool = False
) -> Sequence | str:

    if not isinstance(seq, (Sequence, str)):
        raise TypeError(
            "shuffle_seq() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )

    rng = random.Random(seed)

    chars = list(seq)
    rng.shuffle(chars)
    shuffled = "".join(chars)

    return shuffled if as_str else Sequence(shuffled)


def main():
    seq = Sequence("ACGTATGATTATAGCGAGCGAGCGGGAGTTGCTGATATCTGTAC")
    print(seq.gc_content())
    shuffled = shuffle_seq(seq)
    print(shuffled)
    print(shuffled.gc_content())


if __name__ == "__main__":
    main()
