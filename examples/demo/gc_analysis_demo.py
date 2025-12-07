from omibio.analysis import sliding_gc
from omibio.io import read_fasta


def analyze_gc_example():
    seq_dict = read_fasta("./examples/data/example_single_long_seq.fasta")
    dna = seq_dict["example"]

    result = sliding_gc(dna, window=200, step=20)
    result.plot(show=True)  # or: plot_sliding_gc(result, show=True)


if __name__ == "__main__":
    analyze_gc_example()
