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
