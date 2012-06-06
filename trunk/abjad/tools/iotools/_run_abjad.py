from abjad.tools.iotools.spawn_subprocess import spawn_subprocess
import sys


# TODO: remove this file entirely?
def _run_abjad():
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = ''
    command = '''python -i {} -c "from abjad import *" '''
    command = command.format(file_name)
