from abjad.checks.check import _Check
from abjad.helpers.instances import instances


class QuartersBeamed(_Check):

   def _run(self, expr):
      violators = [ ]
      leaves = instances(expr, '_Leaf')
      for leaf in leaves:
         if hasattr(leaf, 'beam'):
            if leaf.beam.spanned:
               beam = leaf.beam.spanner
               if not beam.__class__.__name__ == 'ComplexBeam':
                  if leaf.beam._flags < 1:
                     violators.append(leaf)
      return violators, len(leaves)
