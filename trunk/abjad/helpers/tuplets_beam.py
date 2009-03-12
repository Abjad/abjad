from abjad.beam.spanner import Beam
from abjad.helpers.iterate import iterate


def tuplets_beam(expr):
   '''Beam every tuplet in expr.

      TODO: this should probably beam only top-level 
            or bottom-level tuplets; the current implementation
            will beam nested tuplets in a nested way.'''

   from abjad.tuplet.tuplet import _Tuplet
   for measure in iterate(expr, _Tuplet):
      Beam(measure)
