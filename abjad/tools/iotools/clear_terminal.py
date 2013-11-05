# -*- encoding: utf-8 -*-
import os


def clear_terminal():
    '''Runs ``clear`` if OS is POSIX-compliant (UNIX / Linux / MacOS).

    Runs ``cls`` if OS is not POSIX-compliant (Windows).

    ::

        >>> iotools.clear_terminal() # doctest: +SKIP

    Returns none.
    '''
    from abjad.tools import iotools

    if os.name == 'posix':
        command = 'clear'
    else:
        command = 'cls'
    iotools.spawn_subprocess(command)
