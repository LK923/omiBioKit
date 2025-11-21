class Sequence:
    """
    A class representing a sequence with methods for analysis.
    """

    _VALID_DNA_BASES = {"A", "T", "C", "G", "N"}
    _VALID_RNA_BASES = {"A", "U", "C", "G", "N"}

    def __init__(self, sequence: str | None = None, rna: bool | None = None):
        """Initialize with a sequence string."""
        self._is_rna = rna
        self.sequence = sequence if sequence is not None else ""

    @property
    def sequence(self) -> str:
        """Getter, returns the sequence."""
        return self._sequence

    @property
    def is_rna(self) -> bool:
        return self._is_rna

    @property
    def type(self) -> str:
        """Return 'DNA' or 'RNA' indicating the sequence type."""
        return "RNA" if self._is_rna else "DNA"

    @sequence.setter
    def sequence(self, sequence):
        """Setter, sets the sequence after validation."""
        if sequence is None:
            sequence = ""
        elif not isinstance(sequence, str):
            raise TypeError("Sequence must be a string")

        sequence = sequence.upper()  # Convert to uppercase
        if self._is_rna is None:
            contains_t = "T" in sequence
            contains_u = "U" in sequence
            if contains_t and contains_u:
                raise ValueError(
                    "Ambiguous sequence: contains both 'T' and 'U'"
                )
            valid_bases = (
                self._VALID_RNA_BASES if contains_u
                else self._VALID_DNA_BASES
            )
        else:
            valid_bases = (
                self._VALID_RNA_BASES if self._is_rna
                else self._VALID_DNA_BASES
            )

        if invalid := set(sequence) - valid_bases:
            seq_typ = "RNA" if valid_bases is self._VALID_RNA_BASES else "DNA"
            # Validate sequence contains only A, C, G, T，N
            raise ValueError(
                f"Invalid base(s) for {seq_typ} "
                f"sequence found: {invalid}"
            )
        self._sequence = sequence
        if self._is_rna is None:
            self._is_rna = ("U" in sequence)

    def gc_content(self, percent: bool = False) -> float | str:
        """Calculate and return the GC content of the sequence."""
        seq_length = len(self.sequence)
        if seq_length == 0:
            return 0.0 if not percent else "0.00%"

        gc = self.sequence.count("G") + self.sequence.count("C")

        return (round(gc / seq_length, 4) if not percent
                else f"{(gc / seq_length) * 100:.2f}%")

    def sliding_gc(self, window=100, step=10):
        from bioKit.analysis.gcContent import sliding_gc
        return sliding_gc(self.sequence, window, step)

    def complement(self) -> "Sequence":
        """Return the complement of the sequence."""
        if self._is_rna is True:
            comp_table = str.maketrans("AUCGN", "UAGCN")
        else:
            comp_table = str.maketrans("ATCGN", "TAGCN")
        comp = self.sequence.translate(comp_table)
        return Sequence(comp, rna=self._is_rna)

    def reverse_complement(self) -> "Sequence":
        """Return the reverse complement of the sequence."""
        if self._is_rna is True:
            rev_comp_table = str.maketrans("AUCGN", "UAGCN")
        else:
            rev_comp_table = str.maketrans("ATCGN", "TAGCN")
        rev_comp = self.sequence.translate(rev_comp_table)[::-1]
        return Sequence(rev_comp, rna=self._is_rna)

    def set_base(self, idx: int, new_base: str) -> None:
        """Set a specific base in the sequence."""
        seq_list = list(self.sequence)
        seq_list[idx] = new_base
        self.sequence = "".join(seq_list)

    def replace_seq(self, start: int, end: int, new_seq: str) -> None:
        self.sequence = (
            self.sequence[:start]
            + new_seq
            + self.sequence[end:]
        )

    def transcribe(self, strand: str = "+") -> "Sequence":
        if self._is_rna is True:
            return self
        if strand not in {"+", "-"}:
            raise ValueError("strand should be either '+' or '-'")
        if strand == "+":
            rna_seq = self.sequence.replace("T", "U")
        else:
            rna_seq = self.complement().sequence.replace("T", "U")
        return Sequence(rna_seq, rna=True)

    def reverse_transcribe(self) -> "Sequence":
        if self._is_rna is False:
            return self
        return Sequence(self.sequence.replace("U", "T"), rna=False)

    def __len__(self) -> int:
        """Return the length of the sequence."""
        return len(self.sequence)

    def __str__(self) -> str:
        """Return string representation of the sequence."""
        return self.sequence

    def __repr__(self) -> str:
        return f"Sequence('{self.sequence}', rna={self._is_rna})"

    def __getitem__(self, idx) -> str:
        return self.sequence[idx]

    def __iter__(self):
        return iter(self.sequence)

    def __contains__(self, item) -> bool:
        return item in self.sequence

    def __eq__(self, other) -> bool:
        if isinstance(other, Sequence):
            return self.sequence == other.sequence
        elif isinstance(other, str):
            return self.sequence == other.upper()
        return False


def main():
    dna = Sequence("ACACAGCTCGTACACAACAGTCA", rna=False)
    print(dna.sliding_gc())


if __name__ == "__main__":
    main()
