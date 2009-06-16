from abjad.cfg.open_file import _open_file
from abjad.cfg.read_config_value import _read_config_value
from write_ly import write_ly
from write_pdf import write_pdf
from show import show


def write_and_show(
   expr, name, template = None, title = None, lilytime = 10, write = True):
   '''When ``write = True`` (default) call ``write_ly(expr)`` and 
   ``write_pdf(expr)`` and then open the resulting PDF.

   When ``write = False`` call ``show(expr)`` only.

   The purpose of this function is to conditionally save named PDF
   and named ``.ly`` output corresponding to *expr*.
   '''

   if write:
      write_ly(expr, name + '.ly', template = template, title = title)
      write_pdf(expr, name + '.pdf', template = template, title = title)
      pdfviewer = _read_config_value('pdfviewer')
      _open_file(name + '.pdf', pdfviewer)
   else:
      show(expr, template = template, title = title, lilytime = lilytime)
