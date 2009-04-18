from abjad.beam.complex.durated.format import _BeamComplexDuratedFormatInterface
from abjad.beam.complex.spanner import BeamComplex
from abjad.rational.rational import Rational
import types


class BeamComplexDurated(BeamComplex):

   def __init__(self, leaves, 
      durations = None, span = 1, lone = False, nibs = 'neither'):
      BeamComplex.__init__(self, leaves)
      self._format = _BeamComplexDuratedFormatInterface(self)
      self.durations = durations
      self.lone = lone
      self.nibs = nibs
      self.span = span

   ## PRIVATE ATTRIBUTES ##

   @property
   def _spanPoints(self):
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
                  arg[i] = Rational(*d)
               else:
                  arg[i] = Rational(d)
            self._durations = arg
         else:
            raise ValueError('durations must be list of Rationals, or None.')
      return property(**locals( ))

   @apply
   def span( ):
      def fget(self):
         return self._span
      def fset(self, arg):
         assert isinstance(arg, (int, types.NoneType))
         self._span = arg 
      return property(**locals( ))
