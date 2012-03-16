from abjad.cfg.cfg import ABJADPATH
import subprocess


def get_abjad_revision_string():
    '''.. versionadded:: 2.0

    Get Abjad revision string::

        abjad> configurationtools.get_abjad_revision_string() # doctest: +SKIP
        '5280'

    Return string.
    '''

    command = 'svnversion {}'.format(ABJADPATH)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.stdout.readlines()[0].strip().strip('M')
