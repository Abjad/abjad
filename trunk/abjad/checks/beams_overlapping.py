from abjad.checks.check import _Check
from abjad.spanners import Beam
from abjad.tools import iterate


class BeamsOverlapping(_Check):
   '''Beams must not overlap.'''

   def _run(self, expr):
      violators = [ ]
      for leaf in iterate.leaves_forward_in(expr):
         beams = [p for p in leaf.spanners.attached
            if isinstance(p, Beam)]
         if len(beams) > 1:
            for beam in beams:
               if beam not in violators:
                  violators.append(beam)
      total = len([p for p in expr.spanners.contained if isinstance(p, Beam)])
      return violators, total
