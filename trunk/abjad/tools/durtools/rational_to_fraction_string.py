from abjad.core import Rational


def rational_to_fraction_string(rational):
   '''Format `rational` as a string of the form ``p/q``.

   ::

      abjad> durtools.rational_to_fraction_string(Rational(1, 4))
      '1/4'

   ::

      abjad> durtools.rational_to_fraction_string(Rational(2, 4))
      '1/2'

   ::

      abjad> durtools.rational_to_fraction_string(Rational(3, 4))
      '3/4'

   ::

      abjad> durtools.rational_to_fraction_string(Rational(4, 4))
      '1/1'
   '''

   if not isinstance(rational, Rational):
      raise TypeError('must be rational.')

   return '%s/%s' % (rational._n, rational._d)
