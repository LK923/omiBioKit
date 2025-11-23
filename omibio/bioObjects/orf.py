from dataclasses import dataclass


@dataclass
class ORF:
    start: int
    end: int
    nt_seq: str
    length: int
    strand: int
    frame: int
    aa_seq: str | None = None


def main():
    ...


if __name__ == "__main__":
    main()
