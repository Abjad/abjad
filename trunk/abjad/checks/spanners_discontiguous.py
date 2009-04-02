from abjad.checks.check import _Check
from abjad.helpers.assess_components import assess_components


class SpannersDiscontiguous(_Check):
   '''Spanner components must be thread-contiguous.'''

   def _run(self, expr):
      violators = [ ]
      total, bad = 0, 0
      for spanner in expr.spanners.contained:
         if not assess_components(spanner[:], contiguity = 'thread'):
            violators.append(spanner)
         total += 1
      return violators, total
