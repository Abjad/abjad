from abjad.tools.spannertools import BeamSpanner
from abjad.tools import componenttools
from abjad.components.Tuplet import Tuplet


def beam_bottommost_tuplets_in_expr(expr):
   '''Beam every bottommost tuplet in 'expr'.'''

   for tuplet in componenttools.iterate_components_forward_in_expr(expr, Tuplet):
      for component in tuplet:
         if isinstance(component, Tuplet):
            break
      else:
         BeamSpanner(tuplet)
