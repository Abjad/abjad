from abjad.core import _StrictComparator
from abjad.core import _Immutable
from abjad.core import Rational


class SchemeMoment(_StrictComparator, _Immutable):
   '''Abjad representation of LilyPond moment.
   
   ::

      abjad> moment = schemetools.SchemeMoment(Rational(1, 56))
      abjad> f(moment)
      #(ly:make-moment 1 56)
   '''

   __slots__ = ('_duration')

   def __init__(self, duration):
      object.__setattr__(self, '_duration', duration)

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
