from abjad.tools import notetools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr


def fill_measures_in_expr_with_big_endian_notes(expr, iterctrl = None):
   '''Fill measures in `expr` with big-endian notes.'''
   if iterctrl is None:
      iterctrl = lambda measure, i: True
   for i, measure in enumerate(iterate_measures_forward_in_expr(expr)):
      if iterctrl(measure, i):
         meter = measure.meter.effective
         #written_duration = ~meter.multiplier * meter.duration
         written_duration = meter.duration / meter.multiplier
         notes = notetools.make_notes(0, written_duration)
         measure[:] = notes
