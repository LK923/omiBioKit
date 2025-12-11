import click
from omibio.cli.fasta_cli import fasta_group
from omibio.io import read_fasta_iter


@fasta_group.command()
@click.argument("fasta_file", type=click.Path(exists=True))
@click.option(
    "--head", "-h",
    type=int,
)
@click.option(
    "--tail", "-t",
    type=int,
)
@click.option(
    "--lengths", "-l",
    is_flag=True
)
@click.option(
    "--id-only", "-id",
    is_flag=True
)
@click.option(
    "--min-length", "-min",
    type=int,
)
@click.option(
    "--max-length", "-max",
    type=int,
)
def view(
    fasta_file: str,
    head: bool,
    tail: bool,
    id_only: bool,
    lengths: bool,
    min_length: int,
    max_length: int
):
    """View FASTA file."""
    count = 0

    def message(entry) -> str:
        nonlocal count
        count += 1
        if id_only:
            return entry.seq_id
        elif lengths:
            return (f"{entry.seq_id}\t{len(entry.seq)}")
        return f">{entry.seq_id}\n{entry.seq}"

    def check_length(entry) -> bool:
        length = len(entry.seq)
        return not (
            (min_length and length < min_length)
            or (max_length and length > max_length)
        )

    result = read_fasta_iter(fasta_file)

    if head is not None:
        for entry in result:
            if not check_length(entry):
                continue

            click.echo(message(entry))
            if count >= head:
                break

    if tail is not None:
        from collections import deque
        entries: deque = deque(maxlen=tail)
        for entry in result:
            if not check_length(entry):
                continue

            entries.append(entry)
        for entry in entries:
            click.echo(message(entry))

    if not head and not tail:
        for entry in result:
            if not check_length(entry):
                continue

            click.echo(message(entry))

    click.echo(f"All {count} sequence(s) showed")
