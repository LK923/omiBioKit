import click


@click.group()
def fastq_group():
    """FASTQ related tools"""
    pass


def register_commands():
    from .fastq_to_fasta import to_fasta
    from .fastq_view import view
    fastq_group.add_command(to_fasta)
    fastq_group.add_command(view)


register_commands()
