import click
from omibio.cli.fastq_cli import fastq_group
from omibio.io import read_fastq_iter


@fastq_group.command()
@click.argument("fastq_file", type=click.Path(exists=True))
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
    fastq_file: str,
    head: int,
    tail: int,
    lengths: bool,
    id_only: bool,
    min_length: int,
    max_length: int
):
    """View FASTQ file."""
    count = 0
    result = read_fastq_iter(fastq_file)

    if min_length and max_length:
        if min_length > max_length:
            raise ValueError(
                "fasta view argument 'min_length' cannot be"
                "larger than 'max_length'"
            )

    def message(entry):
        nonlocal count
        count += 1
        if id_only:
            return entry.seq_id
        elif lengths:
            return f"{entry.seq_id}\t{len(entry.seq)}"
        return f"@{entry.seq_id}\n{entry.seq}\n+\n{entry.qual}"

    def check_length(entry) -> bool:
        length = len(entry.seq)
        return not (
            (min_length and length < min_length)
            or (max_length and length > max_length)
        )

    click.echo(f"File: {fastq_file}")

    if head is not None:
        for entry in result:
            if check_length(entry):
                click.echo(message(entry))
            if count >= head:
                break

    if tail is not None:
        from collections import deque
        entries: deque = deque(maxlen=tail)
        for entry in result:
            if check_length(entry):
                entries.append(entry)
        for entry in entries:
            click.echo(message(entry))

    if not head and not tail:
        for entry in result:
            if check_length(entry):
                click.echo(message(entry))

    click.echo(f"All {count} sequence(s) showed")
