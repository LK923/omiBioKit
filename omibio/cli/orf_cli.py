import click
from omibio.cli import cli
from omibio.io import read_fasta
from omibio.analysis.find_orfs import find_orfs
from omibio.sequence import Polypeptide
import csv
import sys


@cli.command()
@click.argument(
    "fasta_file",
    type=click.File("r"),
    required=False
)
@click.option(
    "--min-length",
    type=int,
    default=100,
    help="Minimum length of ORFs to consider. Defaults to 0."
)
@click.option(
    "--max-length",
    type=int,
    default=10000,
    help="Maximum length of ORFs to consider. Defaults to 10000."
)
@click.option(
    "--start-codons",
    type=str,
    default="ATG",
    help="Comma-separated start codons (e.g., ATG,GTG). Default: ATG."
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Output file path"
)
@click.option(
    "--overlap",
    is_flag=True,
    help="Whether to allow overlapping ORFs."
)
@click.option(
    "--no-reverse",
    is_flag=True,
    help="Whether to include reverse strand ORFs."
)
@click.option(
    "--no-sort",
    is_flag=True,
    help="Whether to sort the results by length in descending order."
)
@click.option(
    "--translate", "-t",
    is_flag=True,
    help=(
        "Whether to translate nucleotide sequences to amino acid sequences."
        " (shown only if --show-seq is used)."
    )
)
@click.option(
    "--show-seq",
    is_flag=True,
    help="Whether to show orf sequence."
)
def orf(
    fasta_file: str,
    min_length: int,
    max_length: int,
    overlap: bool,
    no_reverse: bool,
    no_sort: bool,
    translate: bool,
    start_codons: str,
    show_seq: bool,
    output: str
) -> None:
    """Find orfs of sequences from a FASTA file."""

    start_codon_set = {
        codon.strip().upper() for codon in start_codons.split(",")
    }

    fh = fasta_file or sys.stdin

    seqs = read_fasta(fh).seq_dict()
    all_orfs = []

    for seq_id, seq_obj in seqs.items():
        if isinstance(seq_obj, Polypeptide):
            raise TypeError(
                "Cannot find ORFs in amino acid sequences"
            )
        orfs = find_orfs(
            seq=seq_obj,
            min_length=min_length,
            max_length=max_length,
            overlap=overlap,
            include_reverse=not no_reverse,
            sort_by_length=not no_sort,
            translate=translate,
            start_codons=start_codon_set,
            seq_id=seq_id
        )
        all_orfs.extend(orfs.intervals)

    if not no_sort:
        all_orfs.sort(key=lambda x: x.length, reverse=True)

    res: list[list[str | None]] = []

    for orf in all_orfs:
        frame = f"{orf.frame:+}" if orf.frame > 0 else orf.frame
        base_fields = [
            orf.seq_id,
            str(orf.start),
            str(orf.end),
            orf.strand,
            str(frame),
            str(orf.length)
        ]
        if show_seq:
            nt_seq = str(orf.nt_seq) if orf.nt_seq is not None else "None"
            aa_seq = str(orf.aa_seq) if orf.aa_seq is not None else "None"
            base_fields.extend([nt_seq, aa_seq])
        res.append(base_fields)

    if output is None:
        for base_fields in res:
            click.echo("\t".join(str(f) for f in base_fields))
        click.echo(f"Total: {len(res)} ORFs found")
    else:
        with open(output, "w", newline="", encoding="utf-8") as f:
            header = ["seq_id", "start", "end", "strand", "frame", "length"]
            if show_seq:
                header.append("nt_seq")
                if translate:
                    header.append("aa_seq")
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(res)
        click.echo(f"Result written to {output}")
