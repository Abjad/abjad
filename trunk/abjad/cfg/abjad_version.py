#from abjad.cfg.cfg import ABJADPATH
#from abjad.cfg.cfg import VERSIONFILE
from abjad.cfg.cfg import ABJADVERSIONFILE
import os
import subprocess


def _get_abjad_version( ):
   f = open(ABJADVERSIONFILE, 'r')
   abjad_version = f.readlines( )
   f.close( )
   abjad_version = [line for line in abjad_version \
                  if line.startswith('Revision')]
   abjad_version = abjad_version[0].split(':')[1].strip( )
   return abjad_version


def _write_abjad_versionfile( ):
   os.system('LANG= svn info > %s' % ABJADVERSIONFILE)
      

#os.chdir(ABJADPATH)
#### TODO is there a better way to check whether SVN is installed or not?
#if os.system('svn --help > %s' % os.devnull) == 0:
#   os.system('LANG= svn info > %s' % ABJADVERSIONFILE)
##os.system('LANG= svn info > %s' % VERSIONFILE)
##abjad_version = file(VERSIONFILE, 'r').readlines( )
#abjad_version = file(ABJADVERSIONFILE, 'r').readlines( )
#abjad_version = [line for line in abjad_version if line.startswith('Revision')]
#abjad_version = abjad_version[0].split(':')[1].strip( )
