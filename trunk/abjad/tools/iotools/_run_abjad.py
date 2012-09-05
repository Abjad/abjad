import os
import sys


# TODO: make public and possibly improve function name
def _run_abjad():
    from abjad.tools import iotools

    try:
        file = sys.argv[1]
    except IndexError:
        file = ''

    commands = [
        "from abjad import *;",
        "from abjad.tools import configurationtools;",
        "print configurationtools.get_abjad_startup_string();",
        "del configurationtools",
    ]

    command = '''python -i {} -c "{}"'''.format(file, ' '.join(commands))

    iotools.spawn_subprocess(command)
