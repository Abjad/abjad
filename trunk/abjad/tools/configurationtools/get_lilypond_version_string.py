from abjad.cfg._read_config_file import _read_config_file
import os
import subprocess


def get_lilypond_version_string():
    '''.. versionadded:: 2.0

    Get LilyPond version string::

        abjad> configurationtools.get_lilypond_version_string() # doctest: +SKIP
        '2.13.61'

    Return string.
    '''

    if subprocess.mswindows and not 'LilyPond' in os.environ.get('PATH'):
        command = r'dir "C:\Program Files\*.exe" /s /b | find "lilypond.exe"'
        proc = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
        lilypond = proc.stdout.readline()
        lilypond = lilypond.strip('\r').strip('\n').strip()
        if lilypond == '':
            raise SystemError('LilyPond not found on your Windowz box.')
    else:
        lilypond = _read_config_file()['lilypond_path']
        if not lilypond:
            lilypond = 'lilypond'

    command = lilypond + ' --version'
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    lilypond_version_string = proc.stdout.readline()
    lilypond_version_string = lilypond_version_string.split(' ')[-1]
    lilypond_version_string = lilypond_version_string.strip()

    return lilypond_version_string
