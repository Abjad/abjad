from abjad.rational.rational import Rational


class _Ratio(Rational):

   ### OVERLOADS ###

   def __repr__(self):
      return '_Ratio(%s, %s)' % (self._d, self._n)

   def __str__(self):
      return '%s:%s' % (self._d, self._n)
