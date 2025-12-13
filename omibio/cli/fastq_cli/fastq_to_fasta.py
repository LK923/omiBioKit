import click
from omibio.cli.fastq_cli import fastq_group
from omibio.io import read_fastq_iter, write_fasta
import sys


@fastq_group.command()
@click.argument(
    "fastq_file",
    type=click.File("r"),
    required=False
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None
)
@click.option(
    "--line-len", "-l",
    type=int,
    default=60
)
@click.option(
    "--prefix", "-p",
    type=str,
    default=None
)
def to_fasta(
    fastq_file: str,
    output: str,
    line_len: int,
    prefix: str
):
    fh = fastq_file or sys.stdin
    result = read_fastq_iter(fh)

    if prefix is not None:
        count = 1
        seqs = {}
        for e in result:
            seqs[f"{prefix}_{count}"] = e.seq
            count += 1
    else:
        seqs = {e.seq_id: e.seq for e in result}

    if output is not None:
        write_fasta(seqs=seqs, file_name=output, line_len=int(line_len))
        click.echo(f"Written to {output}")
    else:
        for line in write_fasta(seqs=seqs, line_len=int(line_len)):
            click.echo(line)
