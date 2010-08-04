from abjad.spanners.Beam.ComplexBeam.format import _ComplexBeamFormatInterface
from abjad.spanners.Beam.Beam import Beam
from abjad.core import Rational
import types


class ComplexBeam(Beam):

   def __init__(self, leaves, lone = False, nibs = 'neither'):
      Beam.__init__(self, leaves)
      self._format = _ComplexBeamFormatInterface(self)
      self.lone = lone
      self.nibs = nibs
   
   ## PUBLIC ATTRIBUTES ##

   @apply
   def lone( ):
      def fget(self):
         return self._lone
      def fset(self, arg):
         assert isinstance(arg, bool) or arg in ('left', 'right', 'both')
         self._lone = arg 
      return property(**locals( ))

   @apply
   def nibs( ):
      def fget(self):
         return self._nibs
      def fset(self, arg):
         assert arg in ('left', 'rigth', 'both', 'neither')
         self._nibs = arg 
      return property(**locals( ))
