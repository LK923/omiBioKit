from dataclasses import dataclass, field
from omibio.bio.analysis_result import AnalysisResult
from omibio.bio.seq_interval import SeqInterval
from omibio.utils import ensure_iterable
from typing import Iterator, Union


@dataclass(slots=True)
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
    itv = SeqInterval(1, 10)
    res = IntervalResult(intervals=itv)
    print(repr(res))


if __name__ == "__main__":
    main()
