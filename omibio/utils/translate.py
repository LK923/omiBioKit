DNA_CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F',  # Phenylalanine
    'TTA': 'L', 'TTG': 'L',  # Leucine
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',  # Serine
    'TAT': 'Y', 'TAC': 'Y',  # Tyrosine
    'TAA': '*', 'TAG': '*',  # Stop codons
    'TGT': 'C', 'TGC': 'C',  # Cysteine
    'TGA': '*',              # Stop codon
    'TGG': 'W',              # Tryptophan

    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',  # Leucine
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',  # Proline
    'CAT': 'H', 'CAC': 'H',  # Histidine
    'CAA': 'Q', 'CAG': 'Q',  # Glutamine
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',  # Arginine

    'ATT': 'I', 'ATC': 'I', 'ATA': 'I',  # Isoleucine
    'ATG': 'M',                          # Methionine (Start)
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',  # Threonine
    'AAT': 'N', 'AAC': 'N',  # Asparagine
    'AAA': 'K', 'AAG': 'K',  # Lysine
    'AGT': 'S', 'AGC': 'S',  # Serine
    'AGA': 'R', 'AGG': 'R',  # Arginine

    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',  # Valine
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',  # Alanine
    'GAT': 'D', 'GAC': 'D',  # Aspartic acid
    'GAA': 'E', 'GAG': 'E',  # Glutamic acid
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',  # Glycine
}

RNA_CODON_TABLE = {
    'UUU': 'F', 'UUC': 'F',  # Phenylalanine
    'UUA': 'L', 'UUG': 'L',  # Leucine
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',  # Serine
    'UAU': 'Y', 'UAC': 'Y',  # Tyrosine
    'UAA': '*', 'UAG': '*',  # Stop codons
    'UGU': 'C', 'UGC': 'C',  # Cysteine
    'UGA': '*',              # Stop codon
    'UGG': 'W',              # Tryptophan

    'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',  # Leucine
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',  # Proline
    'CAU': 'H', 'CAC': 'H',  # Histidine
    'CAA': 'Q', 'CAG': 'Q',  # Glutamine
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',  # Arginine

    'AUU': 'I', 'AUC': 'I', 'AUA': 'I',  # Isoleucine
    'AUG': 'M',                          # Methionine (Start)
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',  # Threonine
    'AAU': 'N', 'AAC': 'N',  # Asparagine
    'AAA': 'K', 'AAG': 'K',  # Lysine
    'AGU': 'S', 'AGC': 'S',  # Serine
    'AGA': 'R', 'AGG': 'R',  # Arginine

    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',  # Valine
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',  # Alanine
    'GAU': 'D', 'GAC': 'D',  # Aspartic acid
    'GAA': 'E', 'GAG': 'E',  # Glutamic acid
    'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',  # Glycine
}


def rnaTranslate(
    rna_seq: str,
    stop_symbol: bool = True,
    to_stop: bool = False,
    frame: int = 0,
    augStart: bool = False
) -> str:
    """Translate an RNA sequence into an amino acid sequence."""

    if not rna_seq or len(rna_seq) < 3:
        return ""

    if frame not in (0, 1, 2):
        raise ValueError(f"Invalid frame: {frame}, Frame must be 0, 1, or 2.")

    aa_seq = []
    start_idx = 0
    seq = rna_seq.upper()[frame:]

    if augStart:
        for j in range(0, len(seq) - 2, 3):
            if seq[j: j+3] == "AUG":
                start_idx = j
                break
        else:
            return ""

    for i in range(start_idx, len(seq) - 2, 3):
        codon = seq[i: i+3]

        amino = RNA_CODON_TABLE.get(codon, "X")

        if amino == "*":
            if to_stop:
                break
            if not stop_symbol:
                continue

        aa_seq.append(amino)
    return "".join(aa_seq)


def dnaTranslate(
    seq: str,
    stop_symbol: bool = True,
    to_stop: bool = False,
    frame: int = 0,
    atgStart: bool = False
) -> str:
    """ Translate DNA sequence to amino acid sequence.

    Translate a CODING STRAND DNA sequence to correspond amino acid sequence.

    Args:
    seq:  the coding strand DNA sequence that will be translate.

    Returns:
    A amino acid sequence.
    Example:

        str("MIVRTYLRSLLYTK*")

    """

    if not seq or len(seq) < 3:
        return ""

    if frame not in (0, 1, 2):
        raise ValueError(f"Invalid frame: {frame}, Frame must be 0, 1, or 2.")

    aa_seq = []
    start_idx = 0
    seq = seq.upper()[frame:]

    if atgStart:
        for j in range(0, len(seq) - 2, 3):
            if seq[j: j+3] == "ATG":
                start_idx = j
                break
        else:
            return ""

    for i in range(start_idx, len(seq) - 2, 3):
        codon = seq[i: i + 3]
        amino = DNA_CODON_TABLE.get(codon, "X")

        if amino == "*":
            if to_stop:
                break
            if not stop_symbol:
                continue

        aa_seq.append(amino)

    return "".join(aa_seq)


def main() -> None:
    aa = dnaTranslate("ATGCGTATACTTAA", stop_symbol=True)
    print(aa)


if __name__ == "__main__":
    main()
