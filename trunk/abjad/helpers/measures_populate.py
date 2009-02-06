from abjad.helpers.is_duration_token import _is_duration_token
from abjad.helpers.iterate import iterate
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
         skip.duration.multiplied == measure.meter.effective.duration.

      When mode is None:
         Empty the contents of each measure.

      TODO: determine behavior when measures are spanned.
      TODO: make work with nonbinary meters.
      TODO: add population modes for running sixteenths.'''

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
      notes = construct.notes(0, measure.meter.effective.duration)
      measure[ : ] = notes

def _measures_populate_little_endian(expr):
   for measure in iterate(expr, '_Measure'):
      duration = measure.meter.effective.duration
      notes = construct.notes(0, duration, direction = 'little-endian')
      measure[ : ] = notes

def _measures_populate_duration_train(expr, duration):
   duration = Rational(duration)
   for measure in iterate(expr, '_Measure'):
      total = measure.meter.effective.duration
      cur = Rational(0)
      notes = [ ]
      while cur + duration <= total:
         notes.append(Note(0, duration))
         cur += duration
      remainder = total - cur
      if remainder > 0:
         notes.extend(construct.notes(0, remainder))
      measure[ : ] = notes

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
