from abjad.core.abjadcore import _Abjad
from abjad.rational import Rational


class Moment(_Abjad):
   '''*Abjad* representation of *LilyPond* moment.'''

   def __init__(self, duration):
      '''Initialize duration.'''
      self.duration = duration

   ## PUBLIC ATTRIBUTES ##

   @apply
   def duration(  ):
      '''Read / write rational-valued duration.'''
      def fget(self):
         return self._duration
      def fset(self, expr):
         assert isinstance(expr, Rational)
         self._duration = expr
      return property(**locals( ))

   @property
   def format(self):
      '''*LilyPond* input representation of moment.'''
      numerator, denominator = self.duration._n, self.duration._d
      return '(ly:make-moment %s %s)' % (numerator, denominator)
