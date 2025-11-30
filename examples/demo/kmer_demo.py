from omibio.io import read
from omibio.analysis.kmer import kmer
from omibio.viz import plot_kmer, plt


def kmer_example():
    sequence = read("./examples/data/example_single_long_seq.fasta")["example"]
    kmer_result = kmer(seq=sequence, k=2, min_count=1)
    plot_kmer(kmer_result, cmap="Blues")
    plt.show()


if __name__ == "__main__":
    kmer_example()
