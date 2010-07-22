from abjad.checks.check import _Check
from abjad.tools import durtools
from abjad.tools import iterate


class FlagsMisrepresented(_Check):

   def _run(self, expr):
      violators = [ ] 
      total = 0
      for leaf in iterate.leaves_forward_in_expr(expr):
         total += 1
         #flags = leaf.duration._flags
         flags = durtools.rational_to_flag_count(leaf.duration.written)
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
