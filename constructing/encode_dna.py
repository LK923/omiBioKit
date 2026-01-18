import numpy as np
from omibio.sequence import Sequence
from omibio.bio import SeqEntry, SeqInterval
from typing import Union


DNA_CODES = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3,
    'U': 3,   # RNA → treat as T
    'N': 4,   # unknown
    'R': 5,   # A/G
    'Y': 6,   # C/T
    'S': 7,   # G/C
    'W': 8,   # A/T
    'K': 9,   # G/T
    'M': 10,  # A/C
    'B': 11,
    'D': 12,
    'H': 13,
    'V': 14,
    '-': 15,  # gap
}


def build_table():
    table = np.full(256, -1, dtype=np.int8)

    for key, val in DNA_CODES.items():
        table[ord(key)] = val
        table[ord(key.lower())] = val

    return table


DNA_ENCODE = build_table()
DNA_DECODE = np.array(list("ACGTNRYSWKMBDHV-"), dtype="U1")


def encode_dna(seq: Union[str, SeqInterval, SeqEntry, Sequence]) -> np.ndarray:
    """Encode a DNA sequence into a numpy array of integers.

    Args:
        seq (Union[str, SeqInterval, SeqEntry, Sequence]):
            Input DNA sequence.

    Raises:
        TypeError:
            If the input sequence is not of type Sequence, SeqInterval,
            SeqEntry, or string.

    Returns:
        np.ndarray:
            Numpy array of integers representing the encoded DNA sequence.
    """

    if not isinstance(seq, (str, SeqInterval, SeqEntry, Sequence)):
        raise TypeError(
            "encode_dna() argument 'seq' must be Sequence, SeqInterval, "
            f"SeqEntry or str, not {type(seq).__name__}"
        )
    seq_str = str(seq)
    raw = np.frombuffer(seq_str.encode("ascii"), dtype=np.uint8)
    encoded = DNA_ENCODE[raw]

    return encoded


def decode_dna(arr: np.ndarray) -> str:
    """Decode a numpy array of integers back into a DNA sequence string.

    Args:
        arr (np.ndarray):
            Numpy array of integers to be decoded.

    Returns:
        str:
            Decoded DNA sequence string.
    """
    if not isinstance(arr,  np.ndarray):
        raise TypeError(
            "decode_dna() argument 'arr' must be np.ndarray, not "
            + type(arr).__name__
        )
    return "".join(DNA_DECODE[arr])


def main():
    seq = Sequence("ACTGACTGACTGACGACTGATGCGTATGCATCACA")
    result = encode_dna(seq)
    print(result)
    print(decode_dna(result))
    print(seq)


if __name__ == "__main__":
    main()
