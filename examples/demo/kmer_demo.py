from omibio.io import read_fasta
from omibio.analysis.kmer import kmer
from omibio.viz import plot_kmer, plt


def kmer_example():
    input_path = r"./examples/data/example_single_short_seq.fasta"
    sequence = read_fasta(input_path)["example"]
    kmer_result = kmer(seq=sequence, k=2, min_count=5)
    print(repr(kmer_result))
    plot_kmer(kmer_result, cmap="Blues")
    plt.show()


if __name__ == "__main__":
    kmer_example()
