import re

# TODO: Needs modification


class Sequence:
    """
    A class representing a sequence with methods for analysis.
    """

    def __init__(self, sequence: str):
        """Initialize with a sequence string."""
        self.sequence = sequence

    @property
    def sequence(self):
        """Getter, returns the sequence."""
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Setter, sets the sequence after validation."""
        sequence = sequence.upper()  # Convert to uppercase

        if not (re.fullmatch(r"[ACGTUN]+", sequence)):
            # Validate sequence contains only A, C, G, T
            raise ValueError("Invalid Sequence")
        self._sequence = sequence

    def gc_content(self, percent: bool = False) -> float | str:
        """Calculate and return the GC content of the sequence."""
        seq_length = len(self.sequence)
        gc = self.sequence.count("G") + self.sequence.count("C")
        return (
            (gc / seq_length) if not percent
            else f"{(gc / seq_length)*100:.2f}%"
            )

    def complement(self) -> str:
        """Return the complement of the sequence."""
        complement_table = {
            "A": "T", "T": "A", "C": "G", "G": "C", "N": "N", "U": "A"
            }
        complemented_seq = (complement_table[base] for base in self.sequence)
        return "".join(complemented_seq)

    def reverse_complement(self) -> str:
        """Return the reverse complement of the sequence."""
        return self.complement()[::-1]

    def __len__(self) -> int:
        """"Return the length of the sequence."""
        return len(self.sequence)

    def __str__(self) -> str:
        """Return string representation of the sequence."""
        return f"Sequence({self.sequence})"


def main():
    dna = Sequence("ACGTTTTACGACCAG")
    print(dna)
    print(f"Complement: {dna.complement()}")
    print(f"Reversed complement: {dna.reverse_complement()}")
    print(f"gc_content: {dna.gc_content(True)}")
    print(f"Length: {len(dna)}")


if __name__ == "__main__":
    main()
