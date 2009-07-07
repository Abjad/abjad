import os
import subprocess


def _get_lilypond_version( ):
   if subprocess.mswindows and not 'LilyPond' in os.environ.get('PATH'):
      #lilypond = '"C:\\Program Files\\LilyPond\\usr\\bin\\lilypond.exe"'
      command = r'dir "C:\Program Files\*.exe" /s /b | find "lilypond.exe"'
      proc = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
      lilypond = proc.stdout.readline( )
      lilypond = lilypond.strip('\r').strip('\n').strip( )
      if lilypond == '':
         raise SystemError('LilyPond not found on your Windowz box.')
   else:
      lilypond = 'lilypond'

   command = lilypond + ' --version'
   proc = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
   lilypond_version = proc.stdout.readline( )
   lilypond_version = lilypond_version.split(' ')[-1]
   lilypond_version = lilypond_version.strip( )
   return lilypond_version
