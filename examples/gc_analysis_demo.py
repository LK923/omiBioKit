from omibio.analysis import sliding_gc, draw_sliding_gc
from omibio.sequence import Sequence
from omibio.io import read


def analyze_gc():
    """Run GC content analysis on example sequence and plot results."""
    seq_dict = read("./examples/data/gc.fa")
    dna: Sequence = seq_dict["example"]

    gc_list = sliding_gc(dna, window=200, step=20)
    draw_sliding_gc(gc_list, seq=dna, window_avg=True)


if __name__ == "__main__":
    analyze_gc()
