import os
import sys


def run_abjad():
    from abjad.tools import iotools

    try:
        file = sys.argv[1]
    except IndexError:
        file = ''

    commands = [
        "from abjad import *;",
        "print abjad_configuration.get_abjad_startup_string();",
    ]

    command = r'''python -i {} -c "{}"'''.format(file, ' '.join(commands))

    iotools.spawn_subprocess(command)
