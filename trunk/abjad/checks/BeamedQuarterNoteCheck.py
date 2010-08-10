from abjad.checks._Check import _Check
from abjad.tools import durtools


class BeamedQuarterNoteCheck(_Check):

   def _run(self, expr):
      from abjad.tools import leaftools
      violators = [ ]
      total = 0
      for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
         total += 1
         if hasattr(leaf, 'beam'):
            if leaf.beam.spanned:
               beam = leaf.beam.spanner
               if not beam.__class__.__name__ == 'DuratedComplexBeam':
                  flag_count = durtools.rational_to_flag_count(leaf.duration.written)
                  if flag_count < 1:
                     violators.append(leaf)
      return violators, total
