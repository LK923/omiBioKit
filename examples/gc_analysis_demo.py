from bioKit.analysis import sliding_gc, draw_sliding_gc
from bioKit.io import read


def analyze_gc():
    """Run GC content analysis on example sequence and plot results."""
    seq_dict = read("./examples/data/gc.fa")
    dna = seq_dict["example"]
    print(f"Total GC content: {dna.gc_content(percent=True)}")
    gc_list = sliding_gc(dna)
    draw_sliding_gc(gc_list, seq=dna, window_avg=True)


if __name__ == "__main__":
    analyze_gc()
