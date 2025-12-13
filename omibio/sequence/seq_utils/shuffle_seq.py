import random
from omibio.sequence import Sequence, Polypeptide


def shuffle_seq(
    seq: Sequence | Polypeptide | str,
    seed: int | None = None,
    as_str: bool = False
) -> Sequence | str | Polypeptide:

    if not isinstance(seq, (Sequence, str, Polypeptide)):
        raise TypeError(
            "shuffle_seq() argument 'seq' must be Sequence or str, not "
            + type(seq).__name__
        )

    rng = random.Random(seed)

    chars = list(seq)
    rng.shuffle(chars)
    shuffled = "".join(chars)

    if not as_str:
        if isinstance(seq, Polypeptide):
            return Polypeptide(shuffled)
        else:
            return Sequence(shuffled)
    return shuffled


def main():
    seq = Sequence("ACGTATGATTATAGCGAGCGAGCGGGAGTTGCTGATATCTGTAC")
    print(seq.gc_content())
    shuffled = shuffle_seq(seq)
    print(shuffled)
    print(shuffled.gc_content())


if __name__ == "__main__":
    main()
