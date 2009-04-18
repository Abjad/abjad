from abjad.beam.spanner import Beam
from abjad.beam.complex import BeamComplex
from abjad.measure.measure import _Measure
from abjad.tools import iterate


def beam(expr, style = 'complex'):
   '''Expr can be any Abjad expression.
      Style must be 'complex' or None.

      Iterate expr. For every measure in expr,
      apply BeamComplex, Beam for style set
      equal to 'complex', None, respectively.

      Return list of measures treated.'''

   measures_treated = [ ]
   for measure in iterate.naive(expr, _Measure):
      if style == 'complex':
         BeamComplex(measure)
      elif style is None:
         Beam(measure)
      else:
         raise ValueError('unknown beam style.')
      measures_treated.append(measure)

   return measures_treated
