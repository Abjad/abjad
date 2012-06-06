from abjad.tools.iotools.spawn_subprocess import spawn_subprocess
import os


def clear_terminal():
    '''.. versionadded:: 2.0

    Run ``clear`` if OS is POSIX-compliant (UNIX / Linux / MacOS).

    Run ``cls`` if OS is not POSIX-compliant (Windows)::

        >>> iotools.clear_terminal() # doctest: +SKIP

    Return none.
    '''

    if os.name == 'posix':
        spawn_subprocess('clear')
    else:
        spawn_subprocess('cls')
