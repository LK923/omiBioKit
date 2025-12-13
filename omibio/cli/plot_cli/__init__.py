import click


@click.group()
def plot_group():
    pass


def register_commands():
    from .plot_window_gc_cli import window

    plot_group.add_command(window)


register_commands()
