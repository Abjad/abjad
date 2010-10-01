from fractions import Fraction


def rational_to_fraction_string(rational):
   '''Format `rational` as a string of the form ``p/q``.

   ::

      abjad> durtools.rational_to_fraction_string(Fraction(1, 4))
      '1/4'

   ::

      abjad> durtools.rational_to_fraction_string(Fraction(2, 4))
      '1/2'

   ::

      abjad> durtools.rational_to_fraction_string(Fraction(3, 4))
      '3/4'

   ::

      abjad> durtools.rational_to_fraction_string(Fraction(4, 4))
      '1/1'
   '''

   if not isinstance(rational, Fraction):
      raise TypeError('must be rational.')

   return '%s/%s' % (rational.numerator, rational.denominator)
