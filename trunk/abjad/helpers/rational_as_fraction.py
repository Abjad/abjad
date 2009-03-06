from abjad.rational.rational import Rational


def _rational_as_fraction(rational):
   assert isinstance(rational, Rational)
   return '%s/%s' % (rational._n, rational._d)
