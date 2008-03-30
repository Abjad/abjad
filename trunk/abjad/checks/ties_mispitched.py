from abjad.checks.check import _Check
from abjad.helpers.instances import instances


class TiesMispitched(_Check):

   def _run(self, expr):
      violators = [ ]
      leaves = instances(expr, '_Leaf')
      for leaf in leaves:
         if leaf.tie and leaf.next:
            if leaf.pitch != leaf.next.pitch:
               violators.append(leaf)
      return violators, len(leaves)
