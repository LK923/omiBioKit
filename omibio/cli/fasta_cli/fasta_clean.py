import click
from omibio.cli.fasta_cli import fasta_group
from omibio.io import read_fasta, write_fasta
from typing import TextIO, Literal


@fasta_group.command()
@click.argument(
    "source",
    type=click.File("r"),
    required=False,
    default="-"
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    help="Output file path."
)
@click.option(
    "--name-policy", "-np",
    type=str,
    default="keep",
    help=(
        "Control the clean behavior of sequence names: "
        "'keep', 'id_only', 'underscores'"
    )
)
@click.option(
    "--gap-policy", "-gp",
    type=str,
    default="keep",
    help=(
        "Control the clean behavior of gaps: "
        "'keep', 'remove', 'collapse'"
    )
)
@click.option(
    "--min-length", "-min",
    type=int,
    default=10,
    help="The shortest length of the sequence to be retained"
)
@click.option(
    "--max-length", "-max",
    type=int,
    default=100_000,
    help="The longest length of the sequence to be retained"
)
@click.option(
    "--allowed-bases", "-ab",
    type=str,
    default="ATCGUNRYKMBVDHSW",
    help="Allowed bases to exist in the sequence."
)
@click.option(
    "--report-to",
    type=click.Path(),
    help="Write clean report to a .txt file"
)
@click.option(
    "--strict", "-s",
    is_flag=True,
    help="Whether to be strict to invalid bases."
)
@click.option(
    "--preserve-cases", "-pc",
    is_flag=True,
    help="Whether to preserve case in sequences."
)
@click.option(
    "--remove-illegal", "-ri",
    is_flag=True,
    help="Whether to remove illegal bases in non-strict mode."
)
@click.option(
    "--remove-empty", "-re",
    is_flag=True,
    help="Whether to remove sequences containing only 'N' or '-'."
)
def clean(
    source: TextIO,
    output: str | None,
    name_policy: Literal["keep", "id_only", "underscores"],
    gap_policy: Literal["keep", "remove", "collapse"],
    strict: bool,
    min_length: int,
    max_length: int,
    preserve_cases: bool,
    remove_illegal: bool,
    allowed_bases: str,
    remove_empty: bool,
    report_to: str
):
    """
    Perform data cleanup on the specified FASTA file
    and output the results to the specified file.
    """
    from omibio.sequence.seq_utils.clean import clean as c_f, write_report

    report: bool = report_to is not None
    seqs = read_fasta(source, strict=False, warn=False).seq_dict()
    if report:
        res, rep = c_f(
            seqs=seqs,
            name_policy=name_policy,
            gap_policy=gap_policy,
            strict=strict,
            min_length=min_length,
            max_length=max_length,
            normalize_case=not preserve_cases,
            remove_empty=remove_empty,
            remove_illegal=remove_illegal,
            allowed_bases=set(allowed_bases),
            report=True,
        )
        write_report(report_to, rep)
    else:
        res = c_f(
            seqs=seqs,
            name_policy=name_policy,
            gap_policy=gap_policy,
            strict=strict,
            min_length=min_length,
            max_length=max_length,
            normalize_case=not preserve_cases,
            remove_empty=remove_empty,
            remove_illegal=remove_illegal,
            allowed_bases=set(allowed_bases),
            report=False,
        )
    if output is not None:
        write_fasta(file_name=output, seqs=res)
    else:
        for line in write_fasta(seqs=res):
            click.echo(line)
