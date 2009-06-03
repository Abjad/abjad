from abjad.cfg.wrap_format import _wrap_format
from abjad.cfg.write_preamble import _write_preamble
from abjad.cfg.write_title import _write_title
import os


def write(expr, name, template = None, title = None):
   '''Format *expr* as *LilyPond* input and write to output file *name*.

   * *expr* : Abjad :class:`~abjad.component.component._Component` \
      to be written to disk.
   * *name* : ``str``. The full path name (relative or absolute) of \
      the *LilyPond* file. If only the file name is given, the file \
      is written to the current directory.
   * *template* : ``string``, ``None``. The name of the template to \
      use to format the *LilyPond* file. If ``None`` set, no template is used.
   * *title* : ``str``, ``None``. The title of the file.
   
   Examples:

   Write the *Abjad* component ``t`` to the file ``foo.ly`` in the
   current directory.

   ::

      abjad> t = Note(0, (1, 4))
      abjad> write(t, 'foo.ly')

   
   Write the component ``t`` to file ``foo.ly`` in the 
   ``/home/user`` directory, and add ``paris`` formatting.

   ::

      abjad> t = Note(0, (1, 4))
      abjad> write(t, '/home/user/foo.ly', 'paris') '''

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
         print 'Make sure "%s" exists in your system.' % dirname
