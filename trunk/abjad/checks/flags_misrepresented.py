from abjad.checks.check import _Check
from abjad.helpers.instances import instances


class FlagsMisrepresented(_Check):

   def _run(self, expr):
      violators = [ ] 
      leaves = instances(expr, '_Leaf')
      for leaf in leaves:
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
      return violators, len(leaves)
