import os
import sys


def _run_abjad():
    try:
        file = sys.argv[1]
    except IndexError:
        file = ''
    os.system('''python -i %s -c "import sys; sys.ps1 = 'abjad> '; del sys; from abjad import *" ''' % file)
