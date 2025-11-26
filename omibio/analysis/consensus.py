from omibio.io.read_fasta import read
from omibio.sequence.sequence import Sequence
from collections import defaultdict

IUPAC_CODES = {
    frozenset({'A', 'G'}): 'R', frozenset({'C', 'T'}): 'Y',
    frozenset({'G', 'C'}): 'S', frozenset({'A', 'T'}): 'W',
    frozenset({'G', 'T'}): 'K', frozenset({'A', 'C'}): 'M',
    frozenset({"C", "G", "T"}): "B", frozenset({"A", "G", "T"}): "D",
    frozenset({"A", "C", "T"}): "H", frozenset({"A", "C", "G"}): "V"
}


def find_consensus(
    seq_list: list[str | Sequence],
    as_str: bool = False,
    gap_chars: str = "-?.",
    as_rna: bool = False
) -> str | Sequence:

    if not seq_list:
        return ""
    if not isinstance(seq_list, list):
        raise TypeError(
            "Sequence argument 'strict' must be bool or None, got "
            + type(seq_list).__name__
        )
    seq_list = [str(s).upper() for s in seq_list]

    lengths = set(map(len, seq_list))
    if len(lengths) != 1:
        raise ValueError("All sequences must be of the same length")

    consensus = []

    for i in range(lengths.pop()):
        base_scores = defaultdict(int)
        for seq in seq_list:
            base = seq[i].replace("U", "T")
            if base in gap_chars:
                continue
            base_scores[base] += 1

        if not base_scores:
            consensus.append("N")
            continue

        max_score = max(base_scores.values())
        top_base = [
            b for b, score in base_scores.items() if score == max_score
        ]
        if len(top_base) == 1:
            consensus.append(top_base[0])
        else:
            consensus.append(IUPAC_CODES.get(frozenset(top_base), "N"))

    consensus = (
        Sequence("".join(consensus), strict=False) if not as_rna
        else Sequence("".join(consensus).replace("T", "U"), strict=False)
    )

    return consensus.sequence if as_str else consensus


def main() -> None:
    input_file = r"./examples/data/example_short_seqs.fasta"
    sequence = list(read(input_file).values())
    consensus = find_consensus(sequence, as_rna=False)
    print(consensus)


if __name__ == "__main__":
    main()
