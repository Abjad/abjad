from abjad.cfg.cfg import ABJADPATH
from abjad.cfg.cfg import VERSIONFILE
import os


os.chdir(ABJADPATH)
os.system('LANG= svn info > %s' % VERSIONFILE)
abjad_version = file(VERSIONFILE, 'r').readlines( )
abjad_version = [line for line in abjad_version if line.startswith('Revision')]
abjad_version = abjad_version[0].split(':')[1].strip( )
