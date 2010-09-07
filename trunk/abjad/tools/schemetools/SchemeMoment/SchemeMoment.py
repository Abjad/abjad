from abjad.core import _StrictComparator
from abjad.core import _Immutable
from fractions import Fraction


class SchemeMoment(_StrictComparator, _Immutable):
   '''Abjad representation of LilyPond moment.
   
   ::

      abjad> moment = schemetools.SchemeMoment(Fraction(1, 56))
      abjad> f(moment)
      #(ly:make-moment 1 56)
   '''

   __slots__ = ('_duration')

   def __new__(klass, duration):
      self = object.__new__(klass)
      object.__setattr__(self, '_duration', duration)
      return self

   def __getnewargs__(self):
      return (self.duration,)

#   def __init__(self, duration):
#      duration = Fraction(duration)
#      object.__setattr__(self, '_duration', duration)

   ## PUBLIC ATTRIBUTES ##

   @property
   def duration(self):
      '''Rational duration of LilyPond moment.
      '''
      return self._duration

   @property
   def format(self):
      '''LilyPond input representation of moment.
      '''
      numerator, denominator = self.duration.numerator, self.duration.denominator
      return '#(ly:make-moment %s %s)' % (numerator, denominator)
