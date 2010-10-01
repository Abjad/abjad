from abjad.tools.spannertools.DuratedComplexBeamSpanner._DuratedComplexBeamSpannerFormatInterface import _DuratedComplexBeamSpannerFormatInterface
from abjad.tools.spannertools.ComplexBeamSpanner import ComplexBeamSpanner
from fractions import Fraction
import types


class DuratedComplexBeamSpanner(ComplexBeamSpanner):

   def __init__(self, leaves, 
      durations = None, span = 1, lone = False, nibs = 'neither'):
      ComplexBeamSpanner.__init__(self, leaves)
      self._format = _DuratedComplexBeamSpannerFormatInterface(self)
      self.durations = durations
      self.lone = lone
      self.nibs = nibs
      self.span = span

   ## PRIVATE ATTRIBUTES ##

   @property
   def _span_points(self):
      result = [ ]
      if self.durations is not None:
         result.append(self.durations[0])
         for d in self.durations[1:]:
            result.append(result[-1] + d)   
      return result

   ## PUBLIC ATTRIBUTES ##
      
   @apply
   def durations( ):
      def fget(self):
         return self._durations
      def fset(self, arg):
         if arg is None:
            self._durations = None
         elif isinstance(arg, list):
            for i, d in enumerate(arg):
               if isinstance(d, tuple):
                  arg[i] = Fraction(*d)
               else:
                  arg[i] = Fraction(d)
            self._durations = arg
         else:
            raise ValueError('durations must be list of Fractions, or None.')
      return property(**locals( ))

   @apply
   def span( ):
      def fget(self):
         return self._span
      def fset(self, arg):
         assert isinstance(arg, (int, type(None)))
         self._span = arg 
      return property(**locals( ))
