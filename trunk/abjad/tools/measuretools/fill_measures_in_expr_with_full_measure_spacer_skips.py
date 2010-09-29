from abjad.tools.skiptools.Skip import Skip
from abjad.tools import contexttools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr
from abjad.tools.spannertools._withdraw_component_from_attached_spanners import _withdraw_component_from_attached_spanners


def fill_measures_in_expr_with_full_measure_spacer_skips(expr, iterctrl = None):
   '''Fill measures in `expr` with full-measure spacer skips.'''
   if iterctrl is None:
      iterctrl = lambda measure, i: True
   for i, measure in enumerate(iterate_measures_forward_in_expr(expr)):
      if iterctrl(measure, i):
         skip = Skip(1)
         ## allow zero-update iteration
         forced_meter = measure._explicit_meter
         if forced_meter is not None:
            meter = forced_meter
         else:
            meter = contexttools.get_effective_time_signature(measure)
         skip.duration.multiplier = meter.duration / meter.multiplier
         measure[:] = [skip]
         _withdraw_component_from_attached_spanners(measure)
