from src.fastaReader import read

# TODO: Convert this to a more universal and more easy-to-use tool.


def main() -> None:
    input_file = './data/translate_input.fasta'
    output_file = './output/translate_output.txt'
    results = []

    for rna_seq in list(read(input_file).values()):
        results.append(translate(rna_seq))

    write_output(results, output_file)


def translate(rna_seq: str) -> str:
    """Translate an RNA sequence into an amino acid sequence."""
    amino_acid_to_codons = {  # Standard genetic code
        'F': ['UUU', 'UUC'],
        'L': ['UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'],
        'S': ['UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'],
        'Y': ['UAU', 'UAC'],
        '*': ['UAA', 'UAG', 'UGA'],
        'C': ['UGU', 'UGC'],
        'W': ['UGG'],
        'P': ['CCU', 'CCC', 'CCA', 'CCG'],
        'H': ['CAU', 'CAC'],
        'Q': ['CAA', 'CAG'],
        'R': ['CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],
        'I': ['AUU', 'AUC', 'AUA'],
        'M': ['AUG'],
        'T': ['ACU', 'ACC', 'ACA', 'ACG'],
        'N': ['AAU', 'AAC'],
        'K': ['AAA', 'AAG'],
        'V': ['GUU', 'GUC', 'GUA', 'GUG'],
        'A': ['GCU', 'GCC', 'GCA', 'GCG'],
        'D': ['GAU', 'GAC'],
        'E': ['GAA', 'GAG'],
        'G': ['GGU', 'GGC', 'GGA', 'GGG']
    }

    codon_table = {
        codon: aa for aa, codons in amino_acid_to_codons.items()
        for codon in codons
        }  # Invert the mapping

    seq_length = len(rna_seq)  # Length of the RNA sequence
    amino_acid_seq = []

    # Iterate over the RNA sequence in steps of 3 (codon length)
    for i in range(0, seq_length - 2, 3):
        # Extract codon
        codon = rna_seq[i: i+3]
        if codon_table[codon] == '*':
            break  # Stop translation at stop codon
        amino_acid_seq.append(codon_table[codon])

    return "".join(amino_acid_seq)


def write_output(amino_acid_seq, output_file) -> None:
    """Write the amino acid sequences to the output file."""
    with open(output_file, "w") as f:
        f.write("---------\n")
        for result in amino_acid_seq:
            f.write(f"{result}\n")
            f.write("---------\n")
    print(output_file)  # Print the output file path


if __name__ == "__main__":
    main()
