from abjad.checks.check import _Check
from abjad.tools import iterate


class QuartersBeamed(_Check):

   def _run(self, expr):
      from abjad.leaf.leaf import _Leaf
      violators = [ ]
      total = 0
      for leaf in iterate.naive_forward(expr, _Leaf):
         total += 1
         if hasattr(leaf, 'beam'):
            if leaf.beam.spanned:
               beam = leaf.beam.spanner
               if not beam.__class__.__name__ == 'BeamComplexDurated':
                  if leaf.duration._flags < 1:
                     violators.append(leaf)
      return violators, total
