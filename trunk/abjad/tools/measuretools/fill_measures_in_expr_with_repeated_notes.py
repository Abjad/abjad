from abjad.core.Rational import Rational
from abjad.tools import iterate
from abjad.tools import leaftools


def fill_measures_in_expr_with_repeated_notes(expr, written_duration, iterctrl = None):
   '''Fill measures in `expr` with repeated notes.'''
   if iterctrl is None:
      iterctrl = lambda measure, i: True
   written_duration = Rational(written_duration)
   for i, measure in enumerate(iterate.measures_forward_in_expr(expr)):
      if iterctrl(measure, i):
         meter = measure.meter.effective
         total_duration = meter.duration
         prolation = meter.multiplier
         notes = leaftools.make_repeated_notes_with_shorter_notes_at_end(
            0, written_duration, total_duration, prolation)
         measure[:] = notes
