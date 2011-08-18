import os


def clear_terminal():
    '''.. versionadded:: 2.0

    Run ``clear`` if OS is POSIX-compliant (UNIX / Linux / MacOS).

    Run ``cls`` if OS is not POSIX-compliant (Windows)::

        abjad> iotools.clear_terminal()

    Return none.
    '''

    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
