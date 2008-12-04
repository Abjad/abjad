from abjad.cfg.cfg import VERSIONFILE
import os


os.system('lilypond --version > %s' % VERSIONFILE)
lilypond_version = file(VERSIONFILE, 'r').read( )
lilypond_version = lilypond_version.split('\n')[0].split(' ')[-1]
os.remove(VERSIONFILE)
