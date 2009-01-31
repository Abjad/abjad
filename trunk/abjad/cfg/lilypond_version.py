#from abjad.cfg.cfg import VERSIONFILE
#from abjad.cfg.cfg import LILYPONDVERSIONFILE
import os
import subprocess


def _get_lilypond_version( ):
   if subprocess.mswindows and not 'LilyPond' in os.environ.get('PATH'):
      ### TODO this would be better not hard-coded.
      lilypond = '"C:\\Program Files\\LilyPond\\usr\\bin\\lilypond.exe"'
   else:
      lilypond = 'lilypond'
   proc = subprocess.Popen(lilypond + ' --version', shell=True, 
      stdout=subprocess.PIPE)
   lilypond_version = proc.stdout.readline( )
   lilypond_version = lilypond_version.split(' ')[-1]
   return lilypond_version


##os.system('lilypond --version > %s' % VERSIONFILE)
##lilypond_version = file(VERSIONFILE, 'r').read( )
#os.system('lilypond --version > %s' % LILYPONDVERSIONFILE)
#lilypond_version = file(LILYPONDVERSIONFILE, 'r').read( )
#lilypond_version = lilypond_version.split('\n')[0].split(' ')[-1]
#os.remove(LILYPONDVERSIONFILE)

