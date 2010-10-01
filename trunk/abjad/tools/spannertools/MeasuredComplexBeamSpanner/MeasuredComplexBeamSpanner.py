from abjad.tools.spannertools.MeasuredComplexBeamSpanner._MeasuredComplexBeamSpannerFormatInterface import _MeasuredComplexBeamSpannerFormatInterface
from abjad.tools.spannertools.ComplexBeamSpanner import ComplexBeamSpanner
from fractions import Fraction


class MeasuredComplexBeamSpanner(ComplexBeamSpanner):

   def __init__(self, leaves, lone = False, nibs = 'neither', span = 1):
      ComplexBeamSpanner.__init__(self, leaves, lone = lone, nibs = nibs)
      self._format = _MeasuredComplexBeamSpannerFormatInterface(self)
      self.span = span

   ## PUBLIC ATTRIBUTES ##
      
   @apply
   def span( ):
      def fget(self):
         return self._span
      def fset(self, arg):
         assert isinstance(arg, (int, type(None)))
         self._span = arg 
      return property(**locals( ))
