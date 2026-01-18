import numpy as np
from . import encode_dna


def count_nt(seq):
    seq = encode_dna(str(seq))
    count_arr = np.bincount(seq).astype(int)

    return {b: int(c) for b, c in zip(tuple("ACGTNRYSWKMBDHV-"), count_arr)}


def main():
    seq = "ACTAGCAGGCAATTCGGCGATTTATGCAGGGGCGCCCACTATGCTACGATGC"
    result = count_nt(seq)
    print(result)
    print(result["A"], type(result["A"]))


if __name__ == "__main__":
    main()
