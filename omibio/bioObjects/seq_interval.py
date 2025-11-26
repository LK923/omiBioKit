from dataclasses import dataclass
from typing import Optional, Union
from omibio.sequence.sequence import Sequence
from omibio.sequence.polypeptide import Polypeptide
from omibio.utils.translate import translate_nt


@dataclass(frozen=True)
class SeqInterval:
    """
    Stores information about the sequence range.
    """

    start: int
    end: int

    nt_seq: str

    type: Optional[str] = None
    seq_id: Optional[str] = None
    strand: str = "+"

    aa_seq: Optional[str] = None
    frame: Optional[int] = None

    def __post_init__(self):
        if not isinstance(self.nt_seq, (str, Sequence)):
            raise TypeError(
                "SeqInterval argument 'nt_seq' must be str or Sequence, got "
                + type(self.nt_seq).__name__
            )
        if isinstance(self.nt_seq, Sequence):
            object.__setattr__(self, 'nt_seq', str(self.nt_seq))

        if (
            self.aa_seq is not None
            and not isinstance(self.aa_seq, (Polypeptide, str))
        ):
            raise TypeError(
                "SeqInterval argument 'aa_seq' must "
                f"be str or Polypeptide, got {type(self.aa_seq).__name__}"
            )
        if isinstance(self.aa_seq, Polypeptide):
            object.__setattr__(self, 'aa_seq', str(self.aa_seq))

        if self.strand not in {"+", "-"}:
            raise ValueError(f"strand must be '+' or '-', got {self.strand!r}")
        if self.start < 0 or self.end < 0:
            raise ValueError("start and end must be non-negative integers")
        if self.start > self.end:
            raise ValueError(
                f"Invalid interval: start ({self.start}) > end ({self.end})"
            )

    @property
    def length(self) -> int:
        return self.end - self.start

    def same_seq_as(self, other) -> bool:
        if not isinstance(other, SeqInterval):
            return False
        return self.seq_id == other.seq_id

    def overlaps(self, other: "SeqInterval") -> bool:
        if not self.same_seq_as(other):
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
        if not self.same_seq_as(other):
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

    def to_sequence(
        self,
        rna: Optional[bool] = None,
        strict: bool = False
    ) -> Sequence:

        return Sequence(
            self.nt_seq, rna=rna, strict=strict
        )

    def to_polypeptide(self, strict: bool = False) -> Polypeptide:
        if self.aa_seq is not None:

            return Polypeptide(self.aa_seq, strict=strict)
        else:
            raise ValueError(
                "Cannot create Polypeptide: aa_seq is not set. "
                "Use translate_nt() method instead"
            )

    def translate_nt(
        self,
        strict: bool = False,
        as_str: bool = False,
        stop_symbol: bool = False,
        to_stop: bool = False,
        frame: int = 0,
        require_start: bool = False
    ) -> Union[Polypeptide, str]:

        return translate_nt(
            self.nt_seq,
            strict=strict,
            as_str=as_str,
            stop_symbol=stop_symbol,
            to_stop=to_stop,
            frame=frame,
            require_start=require_start
        )

    def __len__(self) -> int:
        return self.length

    def __repr__(self) -> str:
        from omibio.utils.truncate_repr import truncate_repr
        seq_repr = truncate_repr(self.nt_seq)
        info = (
            f"SeqInterval({seq_repr}, "
            f"{self.start}-{self.end}({self.strand}), "
            f"length={self.length}"
        )
        extras = []

        if self.type is not None:
            extras.append(f"type={self.type!r}")
        if self.seq_id is not None:
            extras.append(f"seq_id={self.seq_id!r}")

        if self.aa_seq is not None:
            aa_seq_repr = truncate_repr(self.aa_seq)
            extras.append(f"aa_seq={aa_seq_repr}")
        if self.frame is not None:
            extras.append(f"frame={self.frame}")

        if extras:
            info += ", " + ", ".join(extras)

        return info + ")"

    def __str__(self):
        return self.nt_seq


def main():
    seq = SeqInterval(
        start=0, end=12,
        nt_seq='ATGAAAAAATAA',
        seq_id='a',
        aa_seq="MKK",
        type="ORF",
        frame=1
    )
    print(repr(seq))


if __name__ == "__main__":
    main()
