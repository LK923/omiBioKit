from omibio.sequence.sequence import Sequence
from omibio.bioObjects.seq_interval import SeqInterval
from typing import Pattern
import re


def find_motif(
    seq: Sequence | str,
    pattern: str | Pattern,
    seq_id: str | None = None,
    ignore_case: bool = True
) -> list[SeqInterval]:

    if not isinstance(seq, (str, Sequence)):
        raise TypeError(
            ...
        )

    seq_str = str(seq)

    if isinstance(pattern, str):
        if not pattern:
            raise ValueError(
                ...
            )
        compiled_pat = (
            re.compile(re.escape(pattern), flags=re.IGNORECASE) if ignore_case
            else re.compile(re.escape(pattern))
        )
    elif isinstance(pattern, Pattern):
        flags = pattern.flags
        if ignore_case:
            flags |= re.IGNORECASE
        else:
            flags &= ~re.IGNORECASE  # Remove IGNORECASE if present
        compiled_pat = re.compile(pattern.pattern, flags=flags)
    else:
        raise TypeError(
            ...
        )

    results = []

    for match in compiled_pat.finditer(seq_str):
        start, end = match.span()
        nt_seq = seq[start: end]
        results.append(
            SeqInterval(
                start=start, end=end, nt_seq=nt_seq,
                type='motif', seq_id=seq_id
            )
        )

    return results


def main():
    sequence = Sequence("AGTCAGCTATCTATTATAGCGATCATGCTGATGCTGATCTGATGC")
    pattern = re.compile(r"AT[ACTG]")
    print(find_motif(sequence, pattern))


if __name__ == "__main__":
    main()
