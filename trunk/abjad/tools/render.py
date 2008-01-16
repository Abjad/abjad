from os import system, listdir, chdir
from glob import fnmatch

system('lilypond --version > %s' % VERSIONFILE)
version = file('%s' % VERSIONFILE, 'r').read().split('\n')[0].split(' ')[-1]
system('rm %s' % VERSIONFILE)

def getNextLilyFileName():
   names = fnmatch.filter(listdir(PICTURESDIR), '*.ly')
   names.sort()
   next = str(int(names[-1][:-3]) + 1).zfill(4)
   return next + '.ly'

def show(ly):
   '''
   Interprets a complete .ly file in the pictures directory;
   logs to lily.out;
   removes the intermediate postscript file;
   opens the resulting PDF in Preview.
   '''

   chdir(PICTURESDIR)
   name = getNextLilyFileName()
   outfile = file(name, 'w')
   outfile.write(ly.format)
   outfile.close( )
   system('lilypond %s > lily.out 2>&1' %(name))
   system('rm ' + name[:-3] + '.ps')
   system('open ' + name[:-3] + '.pdf')

def f(expr):
   if hasattr(expr, 'format'):
      print expr.format
   elif isinstance(expr, list):
      for x in expr:
         print x.format
   else:
      raise ValueError('must be LilyObject or list.')
