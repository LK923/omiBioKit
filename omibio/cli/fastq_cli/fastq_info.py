import click
from omibio.cli.fastq_cli import fastq_group
from omibio.io import read_fastq_iter
import sys


@fastq_group.command()
@click.argument(
    "fastq_file",
    type=click.File("r"),
    required=False
)
def info(fastq_file):
    """Display information about a FASTQ file."""
    fh = fastq_file or sys.stdin
    entries = read_fastq_iter(fh)
    result = []
    sum_q = 0
    min_q = 100
    max_q = 0
    q_20 = 0
    q_30 = 0

    for entry in entries:
        result.append(entry.seq)
        for c in entry.qual:
            q = ord(c) - 33
            sum_q += q
            min_q = min(min_q, q)
            max_q = max(max_q, q)
            if q >= 20:
                q_20 += 1
            if q >= 30:
                q_30 += 1

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
        "\n"
        f"Average qual:\t{(sum_q / total_len):.2f}\n"
        f"Min qual:\t{min_q}\n"
        f"Max qual:\t{max_q}\n"
        f"q20 bases:\t{round((q_20 / total_len) * 100, 2)}% ({q_20} q20 bases)\n"  # noqa
        f"q30 bases:\t{round((q_30 / total_len) * 100, 2)}% ({q_30} q30 bases)\n"  # noqa
    )
