from omibio.analysis import find_motifs
from omibio.sequence import Sequence
import re


def find_potential_introns_example():
    genomic = Sequence(
        "ATGCTGCAGGTGAGTTTCCCAAATGCTATGCTACGTATTGTAGCTAGCTTTTTCAGGTACTGACCGTA"
    )
    pattern = re.compile(r"GT[ACGTN]{20,1000}AG")
    donor_sites = find_motifs(seq=genomic, pattern=pattern)

    for site in donor_sites:
        print(
            f"Potential intron: {site.nt_seq} "
            f"at {site.start}-{site.end}({site.strand})"
        )


if __name__ == "__main__":
    find_potential_introns_example()
