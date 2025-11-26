from omibio.sequence.sequence import Sequence
from omibio.bioObjects.seq_interval import SeqInterval


def main():
    sequence = Sequence("AGTCAGCTATCTATTATAGCGATCATGCTGATGCTGATCTGATGC")
    pattern = "TGC"
    print(find_motif(sequence, pattern))


def find_motif(seq: Sequence | str, pattern: str):
    results = []

    n = len(pattern)
    for i in range(0, len(seq) - n + 1):
        candidate = seq[i: i+n]
        if candidate == pattern:
            results.append(
                SeqInterval(start=i, end=i+n, nt_seq=pattern, type='motif')
            )

    return results


if __name__ == "__main__":
    main()
