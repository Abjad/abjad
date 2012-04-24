from abjad.tools.iotools.spawn_subprocess import spawn_subprocess
import sys


def _run_abjad():
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = ''
    command = '''python -i {} -c "import sys; sys.ps1 = 'abjad> '; del sys; from abjad import *" '''
    command = command.format(file_name)
