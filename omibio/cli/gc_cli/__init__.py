import click


@click.group()
def gc_group():
    """GC related analysis tools."""
    pass


def register_commands():
    from .gc_compute import compute
    from .gc_sliding_window import sliding_window

    gc_group.add_command(compute, name="compute")
    gc_group.add_command(sliding_window, name="sliding-window")


register_commands()
