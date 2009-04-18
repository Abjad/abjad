from abjad.cfg.cfg import ABJADOUTPUT
from abjad.cfg.get_last_output import _get_last_output
import os


def ly(target = -1):
   '''Open most recent Abjad-generated LilyPond input file.'''

   if isinstance(target, int) and target < 0:
      last_lilypond = _get_last_output( )
      if last_lilypond:
         last_number = last_lilypond.replace('.ly', '')
         target_number = int(last_number) + (target + 1)
         target_str = '%04d' % target_number
         target_ly = os.path.join(ABJADOUTPUT, target_str + '.ly')
      else:
         print 'Target LilyPond input file does not exist.'
   elif isinstance(target, int) and 0 <= target:
      target_str = '%04d' % target
      target_ly = os.path.join(ABJADOUTPUT, target_str + '.ly')
   elif isinstance(target, str):
      target_ly = os.path.join(ABJADOUTPUT, target)
   else:
      raise ValueError('can not get target LilyPond input from %s.' % target)

   if os.stat(target_ly):
      os.system('vi %s' % target_ly)
   else:
      print 'Target LilyPond input file %s does not exist.' % target_ly
