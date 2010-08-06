from abjad.tools import iterate
from abjad.tools import leaftools


def fill_measures_in_expr_with_little_endian_notes(expr, iterctrl = None):
   '''Fill measures in `expr` with little-endian notes.'''
   if iterctrl is None:
      iterctrl = lambda measure, i: True
   for i, measure in enumerate(iterate.measures_forward_in_expr(expr)):
      if iterctrl(measure, i):
         meter = measure.meter.effective
         written_duration = ~meter.multiplier * meter.duration
         notes = leaftools.make_notes(
            0, written_duration, direction = 'little-endian')
         measure[:] = notes
