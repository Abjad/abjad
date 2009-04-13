from abjad.beam.spanner import Beam
from abjad.tools import iterate
from abjad.tuplet.tuplet import _Tuplet


def beam_bottommost(expr):
   '''Beam every bottommost tuplet in 'expr'.'''

   for tuplet in iterate.naive(expr, _Tuplet):
      for component in tuplet:
         if isinstance(component, _Tuplet):
            break
      else:
         Beam(tuplet)
