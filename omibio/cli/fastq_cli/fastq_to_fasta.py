import click
from omibio.cli.fastq_cli import fastq_group
from omibio.io import read_fastq_iter, write_fasta


@fastq_group.command()
@click.argument("fastq_file", type=click.Path(exists=True))
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
    result = read_fastq_iter(fastq_file)

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
        lines = write_fasta(seqs=seqs, line_len=int(line_len))
        for line in lines:
            click.echo(line)
