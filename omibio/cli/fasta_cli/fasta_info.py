import click
from omibio.cli.fasta_cli import fasta_group
from omibio.io import read_fasta_iter


@fasta_group.command()
@click.argument("fasta_file", type=click.Path(exists=True))
def info(fasta_file):
    result = [e.seq for e in read_fasta_iter(fasta_file)]

    seq_num = len(result)
    total_len = sum(len(seq) for seq in result)
    gc = round((sum(seq.gc_content() for seq in result) / seq_num) * 100, 2)
    at = round((sum(seq.at_content() for seq in result) / seq_num) * 100, 2)
    ambiguous_bases = {"R", "Y", "S", "W", "K", "M", "B", "D", "H", "V"}
    ambiguous = sum(
        seq.count(base) for base in ambiguous_bases for seq in result
    )
    ns = sum(seq.count("N") for seq in result)

    click.echo(
        f"File: {fasta_file}\n"
        "\n"
        f"Sequences:\t{seq_num}\n"
        f"Total length:\t{total_len} bp\n"
        f"Longest:\t{len(max(result, key=len))} bp\n"
        f"Shortest:\t{len(min(result, key=len))} bp\n"
        f"Average length:\t{total_len // seq_num} bp\n"
        f"Median length:\t{len(sorted(result, key=len)[len(result)//2])} bp\n"
        "\n"
        f"GC content:\t{gc}%\n"
        f"AT content:\t{at}%\n"
        f"N content:\t{round((ns / total_len) * 100, 2)}% ({ns} Ns)\n"
        f"Ambiguous:\t{round((ambiguous / total_len) * 100, 2)}% ({ambiguous} Ambiguous)\n"  # noqa
    )
