from abjad.checks._Check import _Check
from abjad.spanners import Beam


class OverlappingBeamCheck(_Check):
   '''Beams must not overlap.'''

   def _run(self, expr):
      from abjad.tools import leaftools
      violators = [ ]
      for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
         beams = [p for p in leaf.spanners.attached
            if isinstance(p, Beam)]
         if 1 < len(beams):
            for beam in beams:
               if beam not in violators:
                  violators.append(beam)
      total = len([p for p in expr.spanners.contained if isinstance(p, Beam)])
      return violators, total
