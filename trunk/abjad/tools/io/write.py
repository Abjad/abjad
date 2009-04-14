from abjad.cfg.wrap_format import _wrap_format
from abjad.cfg.write_preamble import _write_preamble
from abjad.cfg.write_title import _write_title
import os


def write(expr, name, template = None, title = None):
   '''Writes a given Abjad expression `expr` out to a 
      LilyPond input file with the given `name`.'''

   name = os.path.expanduser(name)
   if not name.endswith('.ly'):
      name += '.ly'
   try:
      outfile = open(name, 'w')
      _write_preamble(outfile, template)
      _write_title(outfile, title)
      outfile.write(_wrap_format(expr.format))
      outfile.close( )
   except IOError:
      print 'ERROR: cound not open file %s' % name
      dirname = os.path.dirname(name)
      if dirname:
         print 'Make sure "%s" exists in your sistem.' % dirname

