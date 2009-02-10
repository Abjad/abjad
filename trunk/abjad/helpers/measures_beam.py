from abjad.beam.spanner import Beam
from abjad.helpers.iterate import iterate


def measures_beam(expr):
   '''Beam every measure in expr.'''

   for measure in iterate(expr, '_Measure'):
      Beam(measure)
