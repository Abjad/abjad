import subprocess


def get_python_version_string():
    '''.. versionadded:: 2.0

    Get Python version string::

        abjad> from abjad.tools import configurationtools

    ::

        abjad> configurationtools.get_python_version_string() # doctest: +SKIP
        '2.6.1'

    Return string.
    '''

    # python prints to stderr on startup (instead of stdout)
    command = 'python --version'
    proc = subprocess.Popen(command, shell = True, stderr = subprocess.PIPE)
    python_version_string = proc.stderr.readline()

    # massage output string
    python_version_string = python_version_string.split(' ')[-1]
    python_version_string = python_version_string.strip()

    # return trimmed string
    return python_version_string
