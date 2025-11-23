import random
from omibio.sequence.sequence import Sequence
from omibio.io.write_fasta import write_fasta


def random_seq(
    length: int,
    alphabet: str = "ATCG",
    weights: list[float] | None = None,
    seed: int | None = None,
    as_str: bool = False,
    seq_strict: bool = False
) -> Sequence | str:

    if length < 0:
        raise ValueError(
            f"Length must be a non-negative integer, got {length}"
        )

    if not alphabet:
        raise ValueError("Alphabet cannot be empty")

    if weights is not None:
        if len(weights) != len(alphabet):
            raise ValueError(
                "Length of 'weights' must match length of 'alphabet'"
            )

    if seed is not None:
        random.seed(seed)

    if weights is not None:
        seq = "".join(random.choices(alphabet, weights, k=length))
    else:
        seq = "".join(random.choices(alphabet, k=length))

    return seq if as_str else Sequence(seq, strict=seq_strict)


def random_fasta(
    file_path: str,
    seq_num: int,
    length: int,
    alphabet: str = "ATCG",
    prefix: str = "Sequence",
    weights: list[float] | None = None,
    seed: int | None = None,
) -> None:

    seq_dict = {}
    for i in range(1, seq_num):
        seq_dict[f"{prefix}_{i}"] = random_seq(
            length=length, alphabet=alphabet,
            weights=weights, seed=seed, as_str=True,
        )
    write_fasta(file_path=file_path, seq_dict=seq_dict, space_between=True)


def main():
    random_fasta(r"./examples/data/random.fasta", 30, 200)


if __name__ == "__main__":
    main()
