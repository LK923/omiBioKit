import click
from omibio.cli.fasta_cli import fasta_group
from omibio.io import read_fasta_iter, write_fasta
from typing import TextIO


@fasta_group.command()
@click.argument(
    "source",
    type=click.File("r"),
    required=False,
    default="-",
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    help="Output file path."
)
@click.option(
    "-f", "--frame",
    type=int,
    default=0,
    help="Frame offset (0, 1, or 2). Defaults to 0."
)
@click.option(
    "-p", "--prefix",
    type=str,
    default=None,
    help="Prefix for amino acid sequence names."
)
@click.option(
    "-ss", "--stop-symbol",
    is_flag=True,
    help="Whether to include stop codon symbol '*'."
)
@click.option(
    "-ts", "--to-stop",
    is_flag=True,
    help="Whether to stop translation at the first stop codon."
)
@click.option(
    "-rs", "--require-start",
    is_flag=True,
    help="Whether to start translation at the first start codon."
)
def translate(
    source: TextIO,
    output: str | None,
    frame: int,
    stop_symbol: bool,
    to_stop: bool,
    require_start: bool,
    prefix: str | None
):
    result = read_fasta_iter(source)
    aa_dict = {}
    count = 1

    for entry in result:
        aa_seq = entry.seq.translate_nt(
            frame=frame, stop_symbol=stop_symbol,
            to_stop=to_stop, require_start=require_start
        )
        if prefix is None:
            aa_dict[f"{entry.seq_id}_amino_acids"] = aa_seq
        else:
            aa_dict[f"{prefix}_{count}"] = aa_seq
            count += 1

    if output is not None:
        write_fasta(seqs=aa_dict, file_name=output)
    else:
        for line in write_fasta(seqs=aa_dict):
            click.echo(line)
