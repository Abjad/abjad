#from abjad.beam.complex.measured.format import \
#   _BeamComplexMeasuredFormatInterface
#from abjad.beam.complex.spanner import BeamComplex
from abjad.spanners.beam.complex.measured.format import \
   _BeamComplexMeasuredFormatInterface
from abjad.spanners.beam.complex.spanner import BeamComplex
from abjad.rational import Rational
import types


class BeamComplexMeasured(BeamComplex):

   def __init__(self, leaves, lone = False, nibs = 'neither', span = 1):
      BeamComplex.__init__(self, leaves, lone = lone, nibs = nibs)
      self._format = _BeamComplexMeasuredFormatInterface(self)
      self.span = span

   ## PUBLIC ATTRIBUTES ##
      
   @apply
   def span( ):
      def fget(self):
         return self._span
      def fset(self, arg):
         assert isinstance(arg, (int, types.NoneType))
         self._span = arg 
      return property(**locals( ))
