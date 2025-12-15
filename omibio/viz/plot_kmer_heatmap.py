import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.axes import Axes
from omibio.bio.kmer_result import KmerResult
from omibio.utils import ensure_iterable


def plot_kmer(
    kmer_counts: list[KmerResult] | KmerResult,
    top_n: int = 20,
    ax=None,
    cmap="viridis",
    annot=True,
    fmt=".2f",
    show: bool = False
) -> Axes:
    """Plot a heatmap of kmer counts from KmerResult objects.

    Args:
        kmer_counts (list[KmerResult] | KmerResult):
            A list of KmerResult objects or a single KmerResult object.
        top_n (int, optional):
            Number of top kmers to display. Defaults to 20.
        ax (_type_, optional):
            Matplotlib Axes object to plot on. If None, a new figure
            and axes are created. Defaults to None.
        cmap (str, optional):
            Colormap for the heatmap. Defaults to "viridis".
        annot (bool, optional):
            Whether to annotate the heatmap cells with values.
            Defaults to True.
        fmt (str, optional):
            String format for annotations. Defaults to ".2f".
        show (bool, optional):
            Whether to display the plot immediately. Defaults to False.

    Raises:
        TypeError:
            If the input types are incorrect.
        ValueError:
            If multiple k values are found in the KmerResult objects.

    Returns:
        Axes:
            The Matplotlib Axes object containing the heatmap.
    """

    if not isinstance(kmer_counts, (list, KmerResult)):
        raise TypeError(
            "plot_kmer() argument 'kmer_counts' must be list[KmerResult] or "
            f"KmerResult, got {type(kmer_counts).__name__}"
        )

    kmer_counts = ensure_iterable(kmer_counts)

    kmers = []
    k_set = set()

    for count in kmer_counts:
        if not isinstance(count, KmerResult):
            raise TypeError(
                "plot_kmer() argument 'kmer_counts' must contains KmerResult, "
                f"got {type(count).__name__}"
            )
        k_set.add(count.k)
        kmers.append(pd.Series(count.counts, name=count.seq_id))

    if len(k_set) > 1:
        raise ValueError(
            f"Got multiple ks for kmers: {k_set}"
        )
    k = k_set.pop()
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

    source = "./examples/data/example_short_seqs.fasta"
    count = 0
    results = []

    for entry in read_fasta_iter(source):
        results.append(kmer(entry.seq, k=3, seq_id="test"))
        count += 1
        if count == 5:
            break

    plot_kmer(results, cmap="Purples")
    plt.show()


if __name__ == "__main__":
    main()
