from omibio.analysis import sliding_gc
from omibio.viz import plot_sliding_gc, plt
from omibio.io import read


def analyze_gc_example():
    seq_dict = read("./examples/data/example_single_long_seq.fasta")
    dna = seq_dict["example"]

    gc_list = sliding_gc(dna, window=200, step=20)
    plot_sliding_gc(gc_list, seq=dna, window_avg=True)
    plt.show()


if __name__ == "__main__":
    analyze_gc_example()
