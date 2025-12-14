from dataclasses import dataclass, field
from omibio.bio.analysis_result import AnalysisResult
from typing import Iterator


@dataclass
class KmerResult(AnalysisResult):

    k: int = field(default_factory=int)
    counts: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.counts, dict):
            raise TypeError(
                "KmerResult argument 'counts' must be dict, got "
                + type(self.counts).__name__
            )

    def items(self):
        return self.counts.items()

    def keys(self):
        return self.counts.keys()

    def values(self):
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
    ...


if __name__ == "__main__":
    main()
