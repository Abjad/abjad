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
   lilypond_version = lilypond_version.strip( )
   return lilypond_version
