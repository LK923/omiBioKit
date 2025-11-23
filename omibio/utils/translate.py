def rnaTranslate(
    rna_seq: str, stopSign: bool = False,
    frame: int = 0, augStart: bool = False
) -> str:
    """Translate an RNA sequence into an amino acid sequence."""

    if not rna_seq or len(rna_seq) < 3:
        return ""

    if frame not in (0, 1, 2):
        raise ValueError(f"Invalid frame: {frame}, Frame must be 0, 1, or 2.")

    codon_table = {  # Standard genetic code
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

    aa = []
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

        amino = codon_table.get(codon)
        if amino is None:
            raise ValueError(f"Invalid codon '{codon}' in RNA sequence")

        if amino == "*":
            if stopSign:
                aa.append("*")
            break

        aa.append(amino)

    return "".join(aa)


def dnaTranslate(seq: str, stopSign: bool = True) -> str:
    """ Translate DNA sequence to amino acid sequence.

    Translate a CODING STRAND DNA sequence to correspond amino acid sequence.

    Args:
    seq:  the coding strand DNA sequence that will be translate.

    Returns:
    A amino acid sequence.
    Example:

        str("MIVRTYLRSLLYTK*")

    """
    # Bulid a dictionary that contains Amino Acids as Keys
    # And list of its correspond Coding Strand DNA Codon as Values.
    codon_groups = {
        "M": ["ATG"],  # Start codon
        "F": ["TTT", "TTC"],
        "L": ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],
        "I": ["ATT", "ATC", "ATA"],
        "V": ["GTT", "GTC", "GTA", "GTG"],
        "S": ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
        "P": ["CCT", "CCC", "CCA", "CCG"],
        "T": ["ACT", "ACC", "ACA", "ACG"],
        "A": ["GCT", "GCC", "GCA", "GCG"],
        "Y": ["TAT", "TAC"],
        "H": ["CAT", "CAC"],
        "Q": ["CAA", "CAG"],
        "N": ["AAT", "AAC"],
        "K": ["AAA", "AAG"],
        "D": ["GAT", "GAC"],
        "E": ["GAA", "GAG"],
        "C": ["TGT", "TGC"],
        "W": ["TGG"],
        "R": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
        "G": ["GGT", "GGC", "GGA", "GGG"],
        "*": ["TAA", "TAG", "TGA"],  # Stop codons
    }

    # Expand the codon_groups dictionary to a new dictionary that contains
    # Every codon as key and its correspond amino acid as value.
    codon_table = {
        codon: aa for aa, codons in codon_groups.items()
        for codon in codons
        }

    aa_seq = []
    # Translate every codon in sequence to amino acid.
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i: i + 3]
        if not stopSign:
            if codon_table[codon] == "*":
                continue
        aa_seq.append(codon_table[codon])
    # Returns a string of the sequence of amino acid.
    return "".join(aa_seq)


def main() -> None:
    aa = dnaTranslate("ATGCGTATACTTAA", stopSign=True)
    print(aa)


if __name__ == "__main__":
    main()
