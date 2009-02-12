from abjad.helpers.is_duration_token import _is_duration_token
from abjad.helpers.iterate import iterate
from abjad.helpers.next_least_power_of_two import _next_least_power_of_two
from abjad.measure.base import _Measure
from abjad.note.note import Note
from abjad.rational.rational import Rational
from abjad.skip.skip import Skip
from abjad.tools import construct


def measures_populate(expr, mode):
   '''Populate each measure in 'expr' according to 'mode'.

      With mode = 'big-endian':
         Populate with big-endian series of notes
         summing to measure.meter.effective.duration.
      
      With mode = 'little-endian':
         Populate with little-endian series of notes
         summing to measure.meter.effective.duration.
      
      With mode = 'meter series':
         Populate with n total 1/d notes, where
         n equals measure.meter.effective.numerator, and
         d equals measure.meter.effective.denominator.

      With mode = 'skip':
         Populate with exactly one skip, such that
         skip.duration.prolated == measure.meter.effective.duration.
         Remove spanners attaching to measure.

      When mode is None:
         Empty the contents of each measure.

      TODO: determine behavior when measures are spanned.
      TODO: make work with nonbinary meters.'''

   if mode == 'big-endian':
      _measures_populate_big_endian(expr)
   elif mode == 'little-endian':
      _measures_populate_little_endian(expr)
   elif mode == 'meter series':
      _measures_populate_meter_series(expr)
   elif mode == 'skip':
      _measures_populate_skip(expr)
   elif _is_duration_token(mode):
      _measures_populate_duration_train(expr, mode)
   elif mode is None:
      _measures_populate_none(expr)
   else:
      raise ValueError('unknown measure population mode "%s".' % mode)


def _measures_populate_big_endian(expr):
   for measure in iterate(expr, '_Measure'):
      meter = measure.meter.effective
      written_duration = ~meter.multiplier * meter.duration
      notes = construct.notes_prolated(0, written_duration)
      measure[ : ] = notes


def _measures_populate_little_endian(expr):
   for measure in iterate(expr, '_Measure'):
      meter = measure.meter.effective
      written_duration = ~meter.multiplier * meter.duration
      notes = construct.notes_prolated(
         0, written_duration, direction = 'little-endian')
      measure[ : ] = notes


def _measures_populate_duration_train(expr, written_duration):
   written_duration = Rational(written_duration)
   for measure in iterate(expr, '_Measure'):
      meter = measure.meter.effective
      total_duration = meter.duration
      prolation = meter.multiplier
      notes = construct.note_train(
         0, written_duration, total_duration, prolation)
      measure[ : ] = notes


def _measures_populate_meter_series(expr):
   for measure in iterate(expr, '_Measure'):
      meter = measure.meter.effective
      denominator = _next_least_power_of_two(meter.denominator)
      numerator = meter.numerator
      notes = Note(0, (1, denominator)) * numerator
      measure[ : ] = notes


def _measures_populate_none(expr):
   for measure in iterate(expr, '_Measure'):
      measure[ : ] = [ ]


def _measures_populate_skip(expr):
   for measure in iterate(expr, '_Measure'):
      skip = Skip(1)
      meter = measure.meter.effective
      skip.duration.multiplier = meter.duration * ~meter.multiplier
      measure[ : ] = [skip]
      measure.spanners.detach( )
