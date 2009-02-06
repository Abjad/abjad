from abjad.cfg.cfg import PDFVIEWER
import os
import sys


def _open_pdf(pdf_file_name):
   if os.name == 'nt':
      os.startfile(pdf_file_name)
   else:
      if sys.platform.lower( ) == 'linux2':
         viewer = PDFVIEWER or 'xdg-open'
      else:
         viewer = PDFVIEWER or 'open'
      os.system('%s %s &' % (viewer, pdf_file_name))
#      error = os.system('%s %s &' % (viewer, pdf_file_name))
#      if error:
#         print 'No PDF viewer defined or "%s" not available. \
#         Please export PDFVIEWER.' % PDFVIEWER



#def _open_pdf(pdf_file_name):
#   if PDFVIEWER:
#      os.system('%s %s &' % (PDFVIEWER, pdf_file_name))
#   else:
#      print 'No PDF viewer defined. Please export PDFVIEWER.'
