from dataclasses import dataclass, field
from omibio.bio.analysis_result import AnalysisResult
from typing import Iterator, Iterable
from omibio.utils import check_if_exist
from pathlib import Path
import csv


@dataclass()
class KmerResult(AnalysisResult):
    """lass to hold kmer counting results. is a subclass of AnalysisResult.

    Args:
        k (int):
            The length of the kmer.
        counts (dict[str, int]):
            A dictionary mapping kmers to their counts.

    Raises:
        TypeError:
            If the input types are incorrect.
    """

    type = 'kmer'
    k: int = field(default_factory=int)
    counts: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.counts, dict):
            raise TypeError(
                "KmerResult argument 'counts' must be dict, got "
                + type(self.counts).__name__
            )
        for kmer in self.counts.keys():
            if len(kmer) != self.k:
                raise TypeError(
                    f"Kmer length does not match k: {kmer!r} and {self.k}"
                )

    def info(self) -> None:
        func = self.plot_func.__name__ if self.plot_func else "N/A"

        message = f"""
{type(self)}
    Type: {check_if_exist(self.type)!r}
    {len(self.counts)} kmers, k={self.k}
    Seq id: {check_if_exist(self.seq_id)!r}
    Plot function: {func}
    Available metadata: {list(self.metadata.keys())!r}
        """

        print(message)

    def to_csv(self, path: Path | str, sep: str = "\t") -> None:
        """Write kmer counts to a csv file.

        Args:
            path (Path | str):
                The path to the output csv file.
            sep (str, optional):
                The separator to use in the csv file. Defaults to "\\t".
        """

        rows: list[list[str | int]] = [["seq_id", "k", "kmer", "count"]]
        seq_id = check_if_exist(self.seq_id)
        for kmer, count in self.counts.items():
            rows.append([seq_id, self.k, kmer, count])

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=sep)
            writer.writerows(rows)

    def items(self) -> Iterable[tuple[str, int]]:
        """Return an iterator over the (kmer, count) pairs."""
        return self.counts.items()

    def keys(self) -> Iterable[str]:
        """Return an iterator over the kmers."""
        return self.counts.keys()

    def values(self) -> Iterable[int]:
        """Return an iterator over the counts."""
        return self.counts.values()

    def __len__(self) -> int:
        return len(self.counts)

    def __iter__(self) -> Iterator[str]:
        return iter(self.counts)

    def __getitem__(self, key: str) -> int:
        return self.counts[key]

    def __repr__(self) -> str:
        return (
            f"KmerResult(counts={self.counts!r}, "
            f"seq_id={self.seq_id!r}, type={self.type!r})"
        )

    def __str__(self) -> str:
        return str(self.counts)


def main():
    import omibio as ob
    seqs = ob.read_fasta(
        "./examples/data/example_single_long_seq.fasta"
    ).seqs()
    result = ob.kmer(seqs[0], 2, seq_id='test')
    result.to_csv("./examples/output/kmer_to_csv.csv")


if __name__ == "__main__":
    main()
