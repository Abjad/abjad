from abjad.checks.check import _Check
from abjad.tools.check.assess_components import assess_components


class SpannersDiscontiguous(_Check):
   '''There are now two different types of spanner.
   Most spanners demand that spanner components be thread-contiguous.
   But a few special spanners (like Tempo) do not make such a demand.
   The check here consults the experimental `_contiguity_constraint`.
   '''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      for spanner in expr.spanners.contained:
         if spanner._contiguity_constraint == 'thread':
            if not assess_components(spanner[:], contiguity = 'thread'):
               violators.append(spanner)
         total += 1
      return violators, total
