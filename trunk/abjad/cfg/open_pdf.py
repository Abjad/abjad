from abjad.cfg.cfg import PDFVIEWER
import os


def _open_pdf(pdf_file_name):
   if PDFVIEWER:
      os.system('%s %s &' % (PDFVIEWER, pdf_file_name))
   else:
      print 'No PDF viewer defined. Please export PDFVIEWER.'
