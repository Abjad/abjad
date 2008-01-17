from os import system, listdir, chdir
from glob import fnmatch
from .. cfg.cfg import VERSIONFILE, ABJADOUTPUT, PDFVIEWER

system('lilypond --version > %s' % VERSIONFILE)
version = file('%s' % VERSIONFILE, 'r').read().split('\n')[0].split(' ')[-1]
system('rm %s' % VERSIONFILE)

def _getNextLilyFileName():
   names = fnmatch.filter(listdir(ABJADOUTPUT), '*.ly')
   names.sort()
   if not names:
      names = ['0.ly']
   next = str(int(names[-1][:-3]) + 1).zfill(4)
   return next + '.ly'

def show(ly):
   '''
   Interprets a complete .ly file in the pictures directory;
   logs to lily.out;
   removes the intermediate postscript file;
   opens the resulting PDF in Preview.
   '''

   chdir(ABJADOUTPUT)
   name = _getNextLilyFileName()
   outfile = file(name, 'w')
   outfile.write(ly.format)
   outfile.close( )
   system('lilypond %s > lily.out 2>&1' %(name))
   system('rm ' + name[:-3] + '.ps')
   system('%s ' % PDFVIEWER  + name[:-3] + '.pdf')
