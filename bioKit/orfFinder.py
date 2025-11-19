from bioKit.fastaReader import read
import re

# TODO: Convert this to a more universal and more easy-to-use tool.


def main() -> None:
    input_file = r".\data\example_fa.fasta"
    output_file_name = r".\output\orf_example_output.txt"
    sequences = read(input_file)

    write_orfs(sequences, output_file_name)


def find_orfs(seq: str, overLap: bool = False) -> list:
    """ Find non-overlapping ORFs in a sequence.

    Find all non-overlapping Open Reading Frames (ORFs) in the given sequence.

    Args:
    seq: The seq where ORFs will be found.

    Returns:
    A list that contains informations about all ORFs.
    Example:

        [
        "ATGGGCTAG
        start=1, end=9, lenth=9
        amino acid sequence: MG*",
        "ORF1: ATGTTTTAA
        start=1, end=9, length=9
        amino acid sequence: MF*"
        ]

    """
    outputs = []
    # Build the pattern of ORF for regular expression.
    if overLap:
        pattern = re.compile(r"(?=(ATG(?:[ACTG]{3})*?(?:TAA|TGA|TAG)))")
    else:
        pattern = re.compile(r"ATG(?:[ATGC]{3})*?(?:TAA|TAG|TGA)")
    # Find all ORFs in sequences.
    for match in pattern.finditer(seq):
        # Get the start/ end position of ORF in sequence
        # And the lenth of the ORF.
        orf = match.group(1) if overLap else match.group(0)
        start_pos = match.start() + 1
        end_pos = start_pos + len(orf) - 1
        # Append information for every ORF to outputs list.
        # Get amino acid sequence of ORFs through calling translate().
        outputs.append(
            f"{orf}\n"
            f"start={start_pos}, end={end_pos}, length={len(orf)}\n"
            f"amino acid sequence: {translate(orf)}\n\n"
        )
    return outputs


def translate(seq: str, stopSign: bool = True) -> str:
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


def write_orfs(sequences: dict, output_file_name: str) -> None:
    """ Write ORFs to output file.

    Write the results of orfs from sequences
    In a text file called "orf_output.txt".

    Args:
    sequences: a dictionary that contains sequence name and the sequence.
    example:

    {
    "seq1": AAAATGCCCTTTGGGTAA,
    "seq2": AGCTAGTCTGTTATCGTA
    }

    Write:
    For every sequence, write the name of the sequence,
    Every ORFs in every sequence,
    and the total number of ORFs in the sequences.
    Example:

        "
        >seq1:
        ORF1: ATGCCCTAA
        start=1, end=9, length=9
        amino acid sequence: MP*

        ORF2: ATGGGGTAG
        start=10, end=18, length=9
        amino acid sequence: MG*

        Total ORFs found in seq1: 2

        ----------------------------
        "
    """
    with open(output_file_name, "w") as f:
        # Write results for every sequence.
        for key in sequences.keys():
            orfs_in_seq = find_orfs(sequences[key])
            f.write(f">{key}:\n")
            for i, orf in enumerate(orfs_in_seq, start=1):
                f.write(f"ORF{i}: {orf}")
            f.write(
                f"Total ORFs found in {key}: {len(orfs_in_seq)}\n\n"
                "----------------------------\n"
            )
    print(f"Output file: {output_file_name}")  # Notify user


if __name__ == "__main__":
    main()
