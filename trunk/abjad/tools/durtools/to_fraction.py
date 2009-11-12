from abjad.rational import Rational


def to_fraction(rational):
   '''Format `rational` as a string of the form ``p/q``.

   ::

      abjad> durtools.to_fraction(Rational(1, 4))
      '1/4'

   ::

      abjad> durtools.to_fraction(Rational(2, 4))
      '1/2'

   ::

      abjad> durtools.to_fraction(Rational(3, 4))
      '3/4'

   ::

      abjad> durtools.to_fraction(Rational(4, 4))
      '1/1'
   '''

   if not isinstance(rational, Rational):
      raise TypeError('must be rational.')

   return '%s/%s' % (rational._n, rational._d)
