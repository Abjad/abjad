from abjad.beam.spanner import Beam
from abjad.tools import iterate


def tuplets_beam_bottommost(expr):
   '''Beam every bottommost tuplet in 'expr'.'''

   from abjad.tuplet.tuplet import _Tuplet
   for tuplet in iterate.naive(expr, _Tuplet):
      for component in tuplet:
         if isinstance(component, _Tuplet):
            break
      else:
         Beam(tuplet)
