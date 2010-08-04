from abjad.spanners.Beam.MeasuredComplexBeam.format import _MeasuredComplexBeamFormatInterface
from abjad.spanners.Beam.ComplexBeam import ComplexBeam
from abjad.core import Rational
import types


class MeasuredComplexBeam(ComplexBeam):

   def __init__(self, leaves, lone = False, nibs = 'neither', span = 1):
      ComplexBeam.__init__(self, leaves, lone = lone, nibs = nibs)
      self._format = _MeasuredComplexBeamFormatInterface(self)
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
