
# TODO: Needs modifications.


def main():
    seq1 = "ATGCATGCTGAAGCTACTGATGTGCAGCATCAGCTAGCGTATGCACACAC"
    seq2 = "AGCTAGCGAGCATTATACATATACGCGATCAGTCACTAGCTATTAGCATA"
    result = point_mutation_counter(seq1, seq2)
    print(f"Number of point mutation is {result}.")


def point_mutation_counter(seq1: str, seq2: str) -> int:
    if len(seq1) != len(seq2):
        raise ValueError("Needs two sequences that have the same lenth.")

    count = 0
    for a, b in zip(seq1, seq2):
        if a != b:
            count += 1

    return count


if __name__ == "__main__":
    main()
