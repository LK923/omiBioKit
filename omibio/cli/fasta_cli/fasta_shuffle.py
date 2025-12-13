import click
from omibio.cli.fasta_cli import fasta_group
from omibio.io import read_fasta, write_fasta
import sys


@fasta_group.command()
@click.argument(
    "fasta_file",
    type=click.File("r"),
    required=False
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    help="Output file path."
)
@click.option(
    "--seed",
    type=int,
    default=None,
    help="Output file path."
)
def shuffle(
    fasta_file: str,
    output: str,
    seed: int
):
    """
    Shuffle the sequences in the FASTA file
    and output them to the specified file.
    """
    from omibio.sequence.seq_utils.shuffle_seq import shuffle_seq
    import random

    fh = fasta_file or sys.stdin
    res = {}
    rng = random.Random(seed)

    seqs = read_fasta(fh).seq_dict()

    for name, seq in seqs.items():
        seq_seed = rng.randint(0, 2**32 - 1)
        shuffled = shuffle_seq(seq, seed=seq_seed, as_str=True)
        res[name] = shuffled

    if output is not None:
        write_fasta(file_name=output, seqs=res)
    else:
        for line in write_fasta(seqs=res):
            click.echo(line)
