from abjad.checks.check import _Check
from abjad.helpers.iterate import iterate


class FlagsMisrepresented(_Check):

   def _run(self, expr):
      #from abjad.leaf.leaf import _Leaf
      violators = [ ] 
      total = 0
      for leaf in iterate(expr, '_Leaf'):
         total += 1
         flags = leaf.beam._flags
         left, right = leaf.beam.counts
         if left is not None:
            if left > flags or (left < flags and right not in (flags, None)):
               if leaf not in violators:
                  violators.append(leaf)
         if right is not None:
            if right > flags or (right < flags and left not in (flags, None)):
               if leaf not in violators:
                  violators.append(leaf)
      return violators, total
