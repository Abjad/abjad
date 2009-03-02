from abjad.checks.check import _Check
#from abjad.helpers.instances import instances
from abjad.helpers.iterate import iterate


class TiesMispitched(_Check):

   def _run(self, expr):
      violators = [ ]
      #leaves = instances(expr, '_Leaf')
      #for leaf in leaves:
      total = 0
      for leaf in iterate(expr, '_Leaf'):
         total += 1
         #if leaf.tie and leaf.next:
         if leaf.tie.spanned and not leaf.tie.last and leaf.next:
            if leaf.pitch != leaf.next.pitch:
               violators.append(leaf)
      #return violators, len(leaves)
      return violators, total
