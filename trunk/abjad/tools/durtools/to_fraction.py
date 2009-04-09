from abjad.rational.rational import Rational


def to_fraction(rational):
   assert isinstance(rational, Rational)
   return '%s/%s' % (rational._n, rational._d)
