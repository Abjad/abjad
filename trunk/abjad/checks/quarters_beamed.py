from abjad.checks.check import _Check
#from abjad.helpers.instances import instances
from abjad.helpers.iterate import iterate


class QuartersBeamed(_Check):

   def _run(self, expr):
      violators = [ ]
      #leaves = instances(expr, '_Leaf')
      #for leaf in leaves:
      total = 0
      for leaf in iterate(expr, '_Leaf'):
         total += 1
         if hasattr(leaf, 'beam'):
            if leaf.beam.spanned:
               beam = leaf.beam.spanner
               if not beam.__class__.__name__ == 'ComplexBeam':
                  if leaf.beam._flags < 1:
                     violators.append(leaf)
      #return violators, len(leaves)
      return violators, total
