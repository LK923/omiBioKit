from dataclasses import dataclass, field
from omibio.bio.analysis_result import AnalysisResult
from omibio.bio.seq_interval import SeqInterval
from omibio.utils import ensure_iterable, check_if_exsit
from typing import Iterator, Union
from pathlib import Path
import csv


@dataclass()
class IntervalResult(AnalysisResult):
    """Store data returned by analytical functions for interval types,
    is a subclass of AnalysisResult.

    Args:
        intervals(tuple[SeqInterval] | SeqInterval):
            A tuple of SeqInterval objects or a single SeqInterval object.

    Raises:
        TypeError:
            If the input types are incorrect.
    """

    intervals: tuple[SeqInterval, ...] = field(default_factory=tuple)

    def __post_init__(self):
        if not isinstance(
            self.intervals, (Union[list, tuple, set], SeqInterval)
        ):
            raise TypeError(
                "IntervalResult argument 'intervals' must be Iterable or "
                f"a single SeqInterval, got {type(self.intervals).__name__}"
            )
        self.intervals = tuple(ensure_iterable(self.intervals))

    def info(self) -> None:
        func = self.plot_func.__name__ if self.plot_func else "N/A"
        message = f"""
{type(self)}
    Type: {check_if_exsit(self.type)!r}
    {len(self.intervals)} intervals
    Seq id: {check_if_exsit(self.seq_id)!r}
    Plot function: {func}
    Available metadata: {list(self.metadata.keys())!r}
        """
        print(message)

    def to_csv(self, path: Path | str, sep: str = "\t"):
        attributes = ["seq_id", "start", "end"]
        match self.type:
            case "ORF":
                attributes.extend(["strand", "frame", "length"])
                if self.metadata.get("include_str_seq", False) is True:
                    attributes.append("nt_seq")
                if self.metadata.get("translate", False) is True:
                    attributes.append("aa_seq")
            case "sliding_gc":
                attributes.append("gc")

        rows = [attributes]
        for itv in self.intervals:
            rows.append(itv.get_attributes(attributes))

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=sep)
            writer.writerows(rows)

    def __len__(self) -> int:
        return len(self.intervals)

    def __iter__(self) -> Iterator[SeqInterval]:
        return iter(self.intervals)

    def __getitem__(
        self, idx: int | slice
    ) -> SeqInterval | tuple[SeqInterval, ...]:
        return self.intervals[idx]

    def __repr__(self) -> str:
        return (
            f"IntervalResult(intervals={self.intervals!r}, "
            f"seq_id={self.seq_id!r}, type={self.type!r})"
        )

    def __str__(self) -> str:
        return str(self.intervals)


def main():
    import omibio as ob
    seqs = ob.read_fasta(
        "./examples/data/example_single_long_seq.fasta"
    ).seqs()
    result = ob.find_orfs(seqs[0], min_length=6)
    result.to_csv("./examples/output/to_csv_gc.tsv")
    print("./examples/output/to_csv_gc.tsv")


if __name__ == "__main__":
    main()
