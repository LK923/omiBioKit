import click


@click.group()
def plot_group():
    pass


def register_commands():
    from .plot_window_gc_cli import window
    from .plot_kmer_cli import kmer

    plot_group.add_command(window)
    plot_group.add_command(kmer)


register_commands()
