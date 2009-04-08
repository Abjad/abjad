from abjad.beam.spanner import Beam
from abjad.beam.complex import ComplexBeam
from abjad.tools import iterate


def measures_beam(expr, style = 'complex'):
   '''Expr can be any Abjad expression.
      Style must be 'complex' or None.

      Iterate expr. For every measure in expr,
      apply ComplexBeam, Beam for style set
      equal to 'complex', None, respectively.

      Return list of measures treated.'''

   measures_treated = [ ]
   from abjad.measure.measure import _Measure
   for measure in iterate.naive(expr, _Measure):
      if style == 'complex':
         ComplexBeam(measure)
      elif style is None:
         Beam(measure)
      else:
         raise ValueError('unknown beam style.')
      measures_treated.append(measure)

   return measures_treated
