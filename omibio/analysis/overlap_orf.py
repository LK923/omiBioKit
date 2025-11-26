from omibio.io.read_fasta import read  # noqa
from omibio.utils.complement import complement
from omibio.utils.translate import translate_nt
import re

# TODO: Needs modifications.


def main() -> None:
    ...


def find_overlap_orf(sequence: str) -> list[str]:
    inputs = [sequence] + [complement(sequence, as_str=True)]
    outputs = []
    pattern = re.compile(r"(?=(ATG(?:[ACTG]{3})*?(?:TAA|TGA|TAG)))")

    for seq in inputs:
        for match in pattern.findall(seq):
            amino_acid_seq = translate_nt(match, stop_symbol=False)
            if amino_acid_seq not in outputs:
                outputs.append(amino_acid_seq)

    return outputs


main()
