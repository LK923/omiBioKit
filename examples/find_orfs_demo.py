from omibio.analysis import find_orfs
from omibio.io import read


def find_orfs_and_get_molecular_formula_example():
    seq_dict = read(r"./examples/data/example_single_long_seq.fasta")
    seq = seq_dict["example"]

    orfs = find_orfs(seq, min_length=200, translate=True)
    for orf in orfs:
        polypeptide = orf.to_polypeptide()
        formula = polypeptide.formula()
        print(
            f"{orf.start}-{orf.end}({orf.strand}):\t{polypeptide!r}\t{formula}"
        )


if __name__ == "__main__":
    find_orfs_and_get_molecular_formula_example()
