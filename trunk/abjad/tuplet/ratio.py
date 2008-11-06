from abjad.duration.rational import Rational


class _Ratio(Rational):

   def __init__(self, p, q = 1):
      Rational.__init__(self, q, p)

   ### REPR ###

   def __repr__(self):
      return '_Ratio(%s, %s)' % (self._d, self._n)

   def __str__(self):
      return '%s:%s' % (self._d, self._n)
