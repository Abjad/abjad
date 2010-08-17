from abjad.tools.spannertools import BeamSpanner
from abjad.tools import componenttools
from abjad.components._Tuplet import _Tuplet


def beam_bottommost_tuplets_in_expr(expr):
   '''Beam every bottommost tuplet in 'expr'.'''

   for tuplet in componenttools.iterate_components_forward_in_expr(expr, _Tuplet):
      for component in tuplet:
         if isinstance(component, _Tuplet):
            break
      else:
         BeamSpanner(tuplet)
