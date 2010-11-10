from abjad.cfg.cfg import ABJADVERSIONFILE
import os


## TODO: Replace call to os.popen( ) with subprocess ##

def _write_abjad_version_file( ):
   version = os.popen('svnversion').read( ).strip( )
   file(ABJADVERSIONFILE, 'w').write(version)
