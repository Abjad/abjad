from abjad.tools.spannertools.ComplexBeamSpanner._ComplexBeamSpannerFormatInterface import _ComplexBeamSpannerFormatInterface
from abjad.tools.spannertools.BeamSpanner.BeamSpanner import BeamSpanner
from fractions import Fraction
import types


class ComplexBeamSpanner(BeamSpanner):

   def __init__(self, leaves, lone = False, nibs = 'neither'):
      BeamSpanner.__init__(self, leaves)
      self._format = _ComplexBeamSpannerFormatInterface(self)
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
