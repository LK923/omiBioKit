import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_kmer(
    kmer_counts: list[dict[str, int]] | dict[str, int],
    top_n: int = 20,
    ax=None,
    cmap="viridis",
    annot=True,
    fmt=".2f",
    show: bool = False
):
    if isinstance(kmer_counts, dict):
        kmer_counts = [kmer_counts]
    kmers = []
    k = len(list(kmer_counts[0].keys())[0])

    for i, count in enumerate(kmer_counts):
        kmers.append(pd.Series(count, name=f"seq_{i+1}"))
    df = pd.DataFrame(kmers).fillna(0)

    top_kmers = df.sum().sort_values(ascending=False).head(top_n).index
    df_top = df[top_kmers]

    df_top = df_top.div(df_top.sum(axis=1), axis=0)

    if ax is None:
        ax = plt.subplots(
            figsize=(max(8, top_n*0.5), max(6, len(kmer_counts)*0.5))
        )[1]
    sns.heatmap(df_top, annot=annot, fmt=fmt, cmap=cmap)
    ax.set_ylabel("Sequence ID")
    ax.set_xlabel(f"{k}-mers")
    ax.set_title(f"{k}-mer Heatmap")

    if show:
        plt.show()

    return ax


def main():
    from omibio.io import read_fasta_iter
    from omibio.analysis import kmer
    kmer_counts = []
    k = 3

    source = "./examples/data/example_short_seqs.fasta"
    for entry in read_fasta_iter(source):
        kmer_counts.append(kmer(entry.seq, k))
        if len(kmer_counts) == 5:
            break
    plot_kmer(kmer_counts)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
