import os
import subprocess


def get_lilypond_version_string():
    '''.. versionadded:: 2.0

    Get LilyPond version string::

        >>> configurationtools.get_lilypond_version_string() # doctest: +SKIP
        '2.13.61'

    Return string.
    '''
    from abjad import ABJCFG
    from abjad.tools import configurationtools

    if subprocess.mswindows and not 'LilyPond' in os.environ.get('PATH'):
        command = r'dir "C:\Program Files\*.exe" /s /b | find "lilypond.exe"'
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lilypond = proc.stdout.readline()
        lilypond = lilypond.strip('\r').strip('\n').strip()
        if lilypond == '':
            raise SystemError('Cannot find LilyPond under Windows.')
    else:
        lilypond = ABJCFG['lilypond_path']
        if not lilypond:
            lilypond = 'lilypond'

    command = lilypond + ' --version'
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    lilypond_version_string = proc.stdout.readline()
    lilypond_version_string = lilypond_version_string.split(' ')[-1]
    lilypond_version_string = lilypond_version_string.strip()

    return lilypond_version_string
