from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg.cfg import PDFVIEWER
from abjad.cfg.get_last_output import _get_last_output
from abjad.cfg.open_file import _open_file
import os


def pdf(target = -1):
   '''Open most recent Abjad-generated PDF.'''

   if isinstance(target, int) and target < 0:
      last_lilypond = _get_last_output( )
      if last_lilypond:
         last_number = last_lilypond.replace('.ly', '')
         target_number = int(last_number) + (target + 1)
         target_pdf = '%s%s%04d.pdf' % (ABJADOUTPUT, os.sep, target_number)
      else:
         print 'Target PDF does not exist.'
   elif isinstance(target, int) and target >= 0:
      target_pdf = '%s%s%04d.pdf' % (ABJADOUTPUT, os.sep, target)
   elif isinstance(target, str):
      target_pdf = ABJADOUTPUT + os.sep + target
   else:
      raise ValueError('can not get target pdf name from %s.' % target)

   if os.stat(target_pdf):
      _open_file(target_pdf, PDFVIEWER)
   else:
      print 'Target PDF %s does not exist.' % target_pdf
