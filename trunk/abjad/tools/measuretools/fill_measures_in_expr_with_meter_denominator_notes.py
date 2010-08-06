from abjad.components.Note import Note
from abjad.tools import iterate
from abjad.tools import mathtools


def fill_measures_in_expr_with_meter_denominator_notes(expr, iterctrl = None):
   '''Fill measures in `expr` with meter denominator notes.'''
   if iterctrl is None:
      iterctrl = lambda measure, i: True
   for i, measure in enumerate(iterate.measures_forward_in_expr(expr)):
      if iterctrl(measure, i):
         meter = measure.meter.effective
         denominator = mathtools.greatest_power_of_two_less_equal(
            meter.denominator)
         numerator = meter.numerator
         notes = Note(0, (1, denominator)) * numerator
         measure[:] = notes
