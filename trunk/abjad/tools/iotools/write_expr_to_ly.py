from abjad.cfg._write_preamble import _write_preamble
from abjad.cfg._write_footer import _write_footer
from abjad.cfg._write_score import _write_score
from abjad.cfg._write_title import _write_title
import os


def write_expr_to_ly(expr, file_name, template = None, 
   title = None, footer = None, lily_time = None):
   '''Format `expr` and write to `file_name`.

   - `expr` : Abjad expression to format.
   - `file_name` : ``str``. The full path name (relative or absolute) of \
      the `LilyPond` file. If only the file name is given, the file \
      is written to the current directory.
   - `template` : ``string``, ``None``. The name of the template to \
      use to format the `LilyPond` file. If ``None``, no template is used.
   - `title` : ``str``, ``None``. The title of the file.
   
   Write ``t`` to ``foo.ly`` in the current directory. ::

      abjad> t = Note(0, (1, 4))
      abjad> write_expr_to_ly(t, 'foo.ly')
   
   Write ``t`` to ``foo.ly`` in the ``/home/user`` directory.
   Include the ``paris.ly`` template in ``foo.ly``. ::

      abjad> t = Note(0, (1, 4))
      abjad> write_expr_to_ly(t, '/home/user/foo.ly', 'paris')

   .. versionadded:: 1.1.1
      Optional `footer` keyword.

   .. versionchanged:: 1.1.2
      renamed ``io.write_ly( )`` to
      ``io.write_expr_to_ly( )``.
   '''

   file_name = os.path.expanduser(file_name)
   if not file_name.endswith('.ly'):
      file_name += '.ly'
   try:
      outfile = open(file_name, 'w')
      _write_preamble(outfile, template)
      _write_title(outfile, title)
      _write_footer(outfile, footer)
      #outfile.write(_wrap_format(expr.format))
      _write_score(outfile, expr.format)
      outfile.close( )
   except IOError:
      print 'ERROR: cound not open file %s' % file_name
      dirname = os.path.dirname(file_name)
      if dirname:
         print 'Make sure "%s" exists in your system.' % dirname

   print 'LilyPond input file written to %s' % os.path.basename(file_name)
