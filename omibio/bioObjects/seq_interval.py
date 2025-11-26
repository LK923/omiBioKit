from dataclasses import dataclass
from typing import Optional, Union


@dataclass(frozen=True)
class SeqInterval:
    start: int
    end: int

    nt_seq: str

    type: Optional[str] = None
    seq_id: Optional[str] = None
    strand: str = "+"

    aa_seq: Optional[str] = None
    frame: Optional[int] = None

    @property
    def length(self) -> int:
        return self.end - self.start

    def overlaps(self, other: "SeqInterval") -> bool:
        if not isinstance(other, SeqInterval):
            return False
        if self.seq_id != other.seq_id:
            return False
        return self.start < other.end and other.start < self.end

    def contains(self, other: Union[int, "SeqInterval"]) -> bool:
        if isinstance(other, int):
            return self.start <= other < self.end
        elif isinstance(other, SeqInterval):
            return (
                self.start <= other.start and other.end <= self.end
                and self.seq_id == other.seq_id
            )
        else:
            return False

    def distance_to(self, other: "SeqInterval") -> int:
        if not isinstance(other, SeqInterval):
            raise TypeError(
                "distance_to() argument 'other' must be SeqInterval, got "
                + type(other).__name__
            )
        if self.seq_id != other.seq_id:
            raise ValueError(
                "Cannot compare the distance between intervals "
                "on two different sequences: "
                f"{self.seq_id!r} vs {other.seq_id!r}"
            )
        if self.overlaps(other):
            return 0
        if self.start >= other.end:
            return self.start - other.end
        else:
            return other.start - self.end

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        info = (
            f"SeqInterval({self.nt_seq!r}, "
            f"location=[{self.start}: {self.end}]({self.strand}), "
            f"length={self.length}"
        )
        extras = []

        if self.type is not None:
            extras.append(f"type={self.type!r}")
        if self.seq_id is not None:
            extras.append(f"seq_id={self.seq_id!r}")

        if self.aa_seq is not None:
            extras.append(f"aa_seq={self.aa_seq!r}")
        if self.frame is not None:
            extras.append(f"frame={self.frame}")

        if extras:
            info += ", " + ", ".join(extras)

        return info + ")"


def main():
    seq1 = SeqInterval(
        start=1, end=10, nt_seq='AAAAAAAAA', seq_id='a'
    )
    seq2 = SeqInterval(
        start=2, end=7, nt_seq="UU"
    )
    print(seq1.distance_to(seq2))


if __name__ == "__main__":
    main()
