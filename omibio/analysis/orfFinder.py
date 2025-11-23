from omibio.io.fastaReader import read
from omibio.bioObjects.orf import ORF
from omibio.sequence import Sequence

STOP_CODONS = {"TAA", "TAG", "TGA"}


def find_orfs_in_frame(
    seq: str,
    strand: str,
    frame: int
) -> list[ORF]:

    orf_list = []
    curr_start = None

    i = frame
    seq_len = len(seq)
    while i + 3 <= seq_len:
        codon = seq[i: i+3]
        if codon in STOP_CODONS:
            if curr_start is not None:
                start_idx = curr_start
                end_idx = i + 3
                nt_seq = seq[start_idx: end_idx]
                orf_length = end_idx - start_idx
                orf_list.append(
                    ORF(
                        start=start_idx+1, end=end_idx,
                        nt_seq=nt_seq, length=orf_length,
                        strand=strand, frame=frame+1
                    )
                )
                curr_start = None
        else:
            if codon == "ATG" and curr_start is None:
                curr_start = i
        i += 3

    return orf_list


def find_orfs(
    seq: Sequence | str,
    include_reverse: bool = True,
    sort_by_length: bool = True
) -> list[ORF]:

    if isinstance(seq, str):
        seq = Sequence(seq)

    seq_length = len(seq)
    results = []

    for frame in (0, 1, 2):
        results.extend(
            find_orfs_in_frame(seq.sequence, strand='+', frame=frame)
        )

    if include_reverse:
        rev_seq = seq.reverse_complement()
        for frame in (0, 1, 2):
            rev_orfs = find_orfs_in_frame(
                rev_seq.sequence, strand='-', frame=frame
                )
            for orf in rev_orfs:
                start = seq_length - orf.end + 1
                end = seq_length - orf.start + 1
                orf_length = orf.length
                nt_seq = orf.nt_seq
                results.append(
                    ORF(
                        start=start, end=end,
                        nt_seq=nt_seq, length=orf_length,
                        strand='-', frame=-orf.frame
                    )
                )

    if sort_by_length:
        results.sort(key=lambda orf: orf.length, reverse=True)

    return results


def main():
    seq_dict = read(r"./examples/data/orf.fasta")
    seq = seq_dict["example"]
    res = find_orfs(seq)
    print(res)
    print(len(res))


if __name__ == "__main__":
    main()
