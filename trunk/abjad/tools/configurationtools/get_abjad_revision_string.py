import subprocess


def get_abjad_revision_string():
    '''.. versionadded:: 2.0

    Get Abjad revision string::

        >>> configurationtools.get_abjad_revision_string() # doctest: +SKIP
        '5280'

    Return string.
    '''

    from abjad import ABJCFG

    command = 'svnversion {}'.format(ABJCFG.ABJAD_PATH)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.stdout.readlines()[0].strip().strip('M')
