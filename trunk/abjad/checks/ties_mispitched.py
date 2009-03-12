from abjad.checks.check import _Check
from abjad.helpers.iterate import iterate


class TiesMispitched(_Check):

   def _run(self, expr):
      from abjad.leaf.leaf import _Leaf
      violators = [ ]
      total = 0
      for leaf in iterate(expr, _Leaf):
         total += 1
         if leaf.tie.spanned and not leaf.tie.last and leaf.next:
            if leaf.pitch != leaf.next.pitch:
               violators.append(leaf)
      return violators, total
