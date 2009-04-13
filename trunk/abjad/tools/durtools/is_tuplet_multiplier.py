from abjad.rational.rational import Rational


def is_tuplet_multiplier(multiplier):
   '''True when multiplier is an Abjad rational
      strictly greater than 1/2 and strictly less than 2.'''

   if not isinstance(multiplier, Rational):
      raise TypeError('multiplier must be rational.')

   if Rational(1, 2) < multiplier < Rational(2):
      return True   

   return False
