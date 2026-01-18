from omibio.io import read_fasta


if __name__ == "__main__":
    entries = read_fasta(
        "./huge_data/huge.fasta", warn=False
    )
