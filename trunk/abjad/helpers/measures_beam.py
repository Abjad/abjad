from abjad.beam.spanner import Beam
from abjad.beam.complex import ComplexBeam
from abjad.helpers.iterate import iterate


def measures_beam(expr, style = 'complex'):
   '''Beam every measure in expr.'''

   for measure in iterate(expr, '_Measure'):
      if style == 'complex':
         ComplexBeam(measure)
      elif style is None:
         Beam(measure)
      else:
         raise ValueError('unknown beam style.')
