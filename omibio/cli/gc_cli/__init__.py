import click


@click.group()
def gc_group():
    """GC related analysis tools."""
    pass


def register_commands():
    from .gc_compute import compute
    from .gc_sliding_window import window

    gc_group.add_command(compute)
    gc_group.add_command(window)


register_commands()
