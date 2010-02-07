from abjad.checks.check import _Check
from abjad.tools import durtools
from abjad.tools import iterate


class QuartersBeamed(_Check):

   def _run(self, expr):
      violators = [ ]
      total = 0
      for leaf in iterate.leaves_forward_in(expr):
         total += 1
         if hasattr(leaf, 'beam'):
            if leaf.beam.spanned:
               beam = leaf.beam.spanner
               if not beam.__class__.__name__ == 'BeamComplexDurated':
                  flag_count = durtools.rational_to_flag_count(
                     leaf.duration.written)
                  #if leaf.duration._flags < 1:
                  if flag_count < 1:
                     violators.append(leaf)
      return violators, total
