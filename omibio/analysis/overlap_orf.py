from omibio.io.read_fasta import read
from omibio.utils.complement import complement
from omibio.utils.translate import translate_nt
import re

# TODO: Needs modifications.


def main() -> None:
    input_file = r".\data\orf_test_seqs.fasta"
    sequences = read(input_file).values()
    for sequence in sequences:
        outputs = find_overlap_orf(sequence)
        [print(output) for output in outputs]


def find_overlap_orf(sequence: str) -> list[str]:
    inputs = [sequence] + [complement(sequence)]
    outputs = []
    pattern = re.compile(r"(?=(ATG(?:[ACTG]{3})*?(?:TAA|TGA|TAG)))")

    for seq in inputs:
        for match in pattern.findall(seq):
            amino_acid_seq = translate_nt(match, stop_symbol=False)
            if amino_acid_seq not in outputs:
                outputs.append(amino_acid_seq)

    return outputs


main()
