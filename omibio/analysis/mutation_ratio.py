TRANSITIONS = {("A", "G"), ("G", "A"), ("T", "C"), ("C", "T")}

# TODO: Needs modifications.


def main():
    seq1 = "ATGCATGCTGAAGCTACTGATGTGCAGCATCAGCTAGCGTATGCACACAC"
    seq2 = "AGCTAGCGAGCATTATACATATACGCGATCAGTCACTAGCTATTAGCATA"
    print(mutation_ratio(seq1, seq2))


def mutation_ratio(seq1: str, seq2: str) -> float:
    if len(seq1) != len(seq2):
        raise ValueError("Needs two sequences of the same length")

    seq1, seq2 = seq1.upper(), seq2.upper()
    ts_count = tv_count = 0

    for a, b in zip(seq1, seq2):
        if a != b:
            if (a, b) in TRANSITIONS:
                ts_count += 1
            else:
                tv_count += 1

    return (ts_count / tv_count)


if __name__ == "__main__":
    main()
