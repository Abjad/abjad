from abjad.cfg.cfg import ABJADVERSIONFILE
import os


## TODO: Break this two functions into separate, private modules. ##

def _get_abjad_version( ):
   return file(ABJADVERSIONFILE, 'r').read( ).strip( )


## TODO: Replace call to os.popen( ) with subprocess ##

def _write_abjad_versionfile( ):
   version = os.popen('svnversion').read( ).strip( )
   file(ABJADVERSIONFILE, 'w').write(version)
