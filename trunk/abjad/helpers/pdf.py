from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg.get_last_output import _get_last_output
from abjad.cfg.open_pdf import _open_pdf
import os


def pdf(target = -1):
   '''Open most recent Abjad-generated PDF.'''

   if isinstance(target, int) and target < 0:
      last_lilypond = _get_last_output( )
      if last_lilypond:
         last_number = last_lilypond.replace('.ly', '')
         target_number = int(last_number) + (target + 1)
         target_pdf = '%s%04d.pdf' % (ABJADOUTPUT, target_number)
      else:
         print 'Target PDF does not exist.'
   elif isinstance(target, int) and target >= 0:
      target_pdf = '%s%04d.pdf' % (ABJADOUTPUT, target)
   elif isinstance(target, str):
      target_pdf = ABJADOUTPUT + target
   else:
      raise ValueError('can not get target pdf name from %s.' % target)

   if os.stat(target_pdf):
      _open_pdf(target_pdf)
   else:
      print 'Target PDF %s does not exist.' % target_pdf
