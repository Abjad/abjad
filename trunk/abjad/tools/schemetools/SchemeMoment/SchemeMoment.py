from abjad.core import _Abjad
from abjad.core import _Immutable
from abjad.core import Rational


class SchemeMoment(_Abjad, _Immutable):
   '''Abjad representation of LilyPond moment.'''

   def __init__(self, duration):
      object.__setattr__(self, '_duration', duration)

   ## PUBLIC ATTRIBUTES ##

#   @apply
#   def duration(  ):
#      '''Read / write rational-valued duration.'''
#      def fget(self):
#         return self._duration
#      def fset(self, expr):
#         assert isinstance(expr, Rational)
#         self._duration = expr
#      return property(**locals( ))

   @property
   def duration(self):
      '''Rational duration of LilyPond moment.'''
      return self._duration

   @property
   def format(self):
      '''LilyPond input representation of moment.'''
      numerator, denominator = self.duration._n, self.duration._d
      return '#(ly:make-moment %s %s)' % (numerator, denominator)
