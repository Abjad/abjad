from abjad.cfg._open_file import _open_file
from abjad.cfg._read_config_file import _read_config_file
from write_ly import write_ly
from write_pdf import write_pdf
from show import show


def write_and_show(
   expr, name, template = None, title = None, footer = None, 
   lilytime = 10, write = True):
   '''When ``write = True`` (default) call ``write_ly(expr)`` and 
   ``write_pdf(expr)`` and then open the resulting PDF.

   When ``write = False`` call ``show(expr)`` only.

   The purpose of this function is to conditionally save named PDF
   and named ``.ly`` output corresponding to `expr`.

   .. versionadded:: 1.1.1
      Optional `footer` keyword.
   '''

   if write:
      write_ly(expr, name + '.ly', template = template, title = title, 
         footer = footer, lilytime = lilytime)
      write_pdf(expr, name + '.pdf', template = template, title = title,
         footer = footer, lilytime = lilytime)
      pdf_viewer = _read_config_file( )['pdf_viewer']
      _open_file(name + '.pdf', pdf_viewer)
   else:
      show(expr, template = template, title = title, 
         footer = footer, lilytime = lilytime)
