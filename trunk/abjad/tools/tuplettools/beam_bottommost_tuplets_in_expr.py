from abjad.spanners import Beam
from abjad.tools import iterate
from abjad._Tuplet import _Tuplet


def beam_bottommost_tuplets_in_expr(expr):
   '''Beam every bottommost tuplet in 'expr'.'''

   for tuplet in iterate.naive_forward_in_expr(expr, _Tuplet):
      for component in tuplet:
         if isinstance(component, _Tuplet):
            break
      else:
         Beam(tuplet)
