from abjad.measure.measure import _Measure
from abjad.note.note import Note
from abjad.rational.rational import Rational
#from abjad.skip.skip import Skip
from abjad.skip import Skip
from abjad.tools import construct
from abjad.tools import durtools
from abjad.tools import iterate
from abjad.tools import mathtools


def populate(expr, mode, iterctrl = lambda measure, i: True):
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
         Empty the contents of each measure.'''

   if mode == 'big-endian':
      _measures_populate_big_endian(expr, iterctrl)
   elif mode == 'little-endian':
      _measures_populate_little_endian(expr, iterctrl)
   elif mode == 'meter series':
      _measures_populate_meter_series(expr, iterctrl)
   elif mode == 'skip':
      _measures_populate_skip(expr, iterctrl)
   elif durtools.is_token(mode):
      _measures_populate_duration_train(expr, mode, iterctrl)
   elif mode is None:
      _measures_populate_none(expr, iterctrl)
   else:
      raise ValueError('unknown measure population mode "%s".' % mode)


def _measures_populate_big_endian(expr, iterctrl):
   from abjad.measure.measure import _Measure
   for i, measure in enumerate(iterate.naive(expr, _Measure)):
      if iterctrl(measure, i):
         meter = measure.meter.effective
         written_duration = ~meter.multiplier * meter.duration
         notes = construct.notes(0, written_duration)
         measure[:] = notes


def _measures_populate_little_endian(expr, iterctrl):
   from abjad.measure.measure import _Measure
   for i, measure in enumerate(iterate.naive(expr, _Measure)):
      if iterctrl(measure, i):
         meter = measure.meter.effective
         written_duration = ~meter.multiplier * meter.duration
         notes = construct.notes(
            0, written_duration, direction = 'little-endian')
         measure[:] = notes


def _measures_populate_duration_train(expr, written_duration, iterctrl):
   from abjad.measure.measure import _Measure
   written_duration = Rational(written_duration)
   for i, measure in enumerate(iterate.naive(expr, _Measure)):
      if iterctrl(measure, i):
         meter = measure.meter.effective
         total_duration = meter.duration
         prolation = meter.multiplier
         notes = construct.note_train(
            0, written_duration, total_duration, prolation)
         measure[:] = notes


def _measures_populate_meter_series(expr, iterctrl):
   from abjad.measure.measure import _Measure
   for i, measure in enumerate(iterate.naive(expr, _Measure)):
      if iterctrl(measure, i):
         meter = measure.meter.effective
         denominator = mathtools.greatest_power_of_two_less_equal(
            meter.denominator)
         numerator = meter.numerator
         notes = Note(0, (1, denominator)) * numerator
         measure[:] = notes


def _measures_populate_none(expr, iterctrl):
   from abjad.measure.measure import _Measure
   for i, measure in enumerate(iterate.naive(expr, _Measure)):
      if iterctrl(measure, i):
         measure[:] = [ ]


def _measures_populate_skip(expr, iterctrl):
   from abjad.measure.measure import _Measure
   for i, measure in enumerate(iterate.naive(expr, _Measure)):
      if iterctrl(measure, i):
         skip = Skip(1)
         ## allow zero-update iteration
         forced_meter = measure.meter.forced
         if forced_meter is not None:
            meter = forced_meter
         else:
            meter = measure.meter.effective
         skip.duration.multiplier = meter.duration * ~meter.multiplier
         measure[:] = [skip]
         measure.spanners._detach( )
