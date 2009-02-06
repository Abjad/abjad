from abjad.helpers.iterate import iterate
from abjad.measure.base import _Measure
from abjad.note.note import Note
from abjad.skip.skip import Skip


def measures_populate(expr, mode):
   '''Populate each measure in 'expr' according to 'mode'.
      
      With mode = 'meter series':
         Populate with n total 1/d notes, where
         n equals measure.meter.effective.numerator, and
         d equals measure.meter.effective.denominator.

      With mode = 'skip':
         Populate with exactly one skip, such that
         skip.duration.multiplied == measure.meter.effective.duration.

      When mode is None:
         Empty the contents of each measure.

      TODO: determine behavior when measures are spanned.
      TODO: make work with nonbinary meters.
      TODO: add population modes for running sixteenths, 
            running eights, big-ending and small-ending notes.'''

   if mode == 'meter series':
      _measures_populate_meter_series(expr)
   elif mode == 'skip':
      _measures_populate_skip(expr)
   elif mode is None:
      _measures_populate_none(expr)
   else:
      raise ValueError('unknown measure population mode "%s".' % mode)

def _measures_populate_meter_series(expr):
   for measure in iterate(expr, '_Measure'):
      denominator = measure.meter.effective.denominator
      numerator = measure.meter.effective.numerator
      notes = Note(0, (1, denominator)) * numerator
      measure[ : ] = notes

def _measures_populate_none(expr):
   for measure in iterate(expr, '_Measure'):
      measure[ : ] = [ ]

def _measures_populate_skip(expr):
   for measure in iterate(expr, '_Measure'):
      skip = Skip(1)
      skip.duration.multiplier = measure.meter.effective.duration
      measure[ : ] = [skip]
