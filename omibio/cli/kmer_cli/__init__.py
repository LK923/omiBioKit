import click


@click.group()
def kmer_group():
    """Kmer related analysis tools."""
    pass


def register_commands():
    from .kmer_count import count

    kmer_group.add_command(count)


register_commands()
