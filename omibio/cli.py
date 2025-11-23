import click
from omibio.io.fastaReader import read
from omibio.analysis.orfFinder import find_orfs


@click.group
def cli():
    """A lightweight and easy-to-use python bioinformatics toolkit"""
    pass


@cli.command()
@click.argument("fasta_file", type=click.Path(exists=True))
def gc(fasta_file: str) -> None:
    """"Calculate the GC content of a sequence from a fasta file."""
    seqs = read(fasta_file)
    for name, seq in seqs.items():
        gc_val = seq.gc_content(percent=True)
        click.echo(f"{name}\t{gc_val}")


@cli.command()
@click.argument("fasta_file", type=click.Path(exists=True))
@click.option(
    "--min-length",
    type=int,
    default=0,
    help="Minimum length of ORFs to consider. Defaults to 0."
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
    "--translate",
    is_flag=True,
    help="Translate the nucleotide sequences to amino acid sequences."
)
@click.option(
    "--start-codons",
    type=str,
    default="ATG",
    help="Comma-separated start codons (e.g., ATG,GTG). Default: ATG."
)
@click.option(
    "--show-orf-seq",
    is_flag=True,
    help="Whether to show orf sequence."
)
def orf(
    fasta_file: str,
    min_length: int,
    no_reverse: bool,
    no_sort: bool,
    translate: bool,
    start_codons: str,
    show_orf_seq: bool
) -> None:
    """Find orfs of a sequence from a fasta file."""
    start_codon_set = {
        codon.strip().upper() for codon in start_codons.split(",")
    }

    seqs = read(fasta_file)
    all_orfs = []

    for seq_id, seq_obj in seqs.items():
        orfs = find_orfs(
            seq=seq_obj,
            min_length=min_length,
            include_reverse=not no_reverse,
            sort_by_length=not no_sort,
            translate=translate,
            start_codons=start_codon_set,
            seq_id=seq_id
        )
        all_orfs.extend(orfs)

    if not no_sort:
        all_orfs.sort(key=lambda x: x.length, reverse=True)

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
        if show_orf_seq:
            nt_seq = orf.nt_seq
            aa_seq = orf.aa_seq if orf.aa_seq is not None else ""
            base_fields.extend([nt_seq, aa_seq])

        click.echo("\t".join(base_fields))
