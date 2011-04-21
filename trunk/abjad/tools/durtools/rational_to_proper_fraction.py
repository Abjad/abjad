from fractions import Fraction


def rational_to_proper_fraction(rational):
   '''.. versionadded:: 1.1.2

   Change `rational` to proper fraction::

      abjad> durtools.rational_to_proper_fraction(Fraction(116, 8))
      (14, Fraction(1, 2))
   
   Return pair.
   '''

   if not isinstance(rational, Fraction):
      raise TypeError

   quotient = int(rational)
   residue = rational - quotient

   return quotient, residue
