import click
from omibio.cli import cli
from omibio.io import read_fasta, write_fasta


@cli.command()
@click.argument("fasta_file", type=click.Path(exists=True))
@click.option(
    "-o", "--output",
    type=click.Path(),
    required=True,
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

    res = {}
    rng = random.Random(seed)

    seqs = read_fasta(fasta_file, strict=False).seq_dict()

    for name, seq in seqs.items():
        seq_seed = rng.randint(0, 2**32 - 1)
        shuffled = shuffle_seq(seq, seed=seq_seed, as_str=True)
        res[name] = shuffled

    write_fasta(output, res)
    click.echo(f"Success: file writed to {output}")
