import os


def clear_terminal():
    '''.. versionadded:: 2.0

    Run ``clear`` if OS is POSIX-compliant (UNIX / Linux / MacOS).

    Run ``cls`` if OS is not POSIX-compliant (Windows)::

        >>> iotools.clear_terminal() # doctest: +SKIP

    Return none.
    '''
    from abjad.tools import iotools

    if os.name == 'posix':
        iotools.spawn_subprocess('clear')
    else:
        iotools.spawn_subprocess('cls')
