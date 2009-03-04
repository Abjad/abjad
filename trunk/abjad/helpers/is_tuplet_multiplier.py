from abjad.rational.rational import Rational


def _is_tuplet_multiplier(multiplier):
   '''True when multiplier is an Abjad rational
      strictly greater than 1/2 and strictly less than 2.'''

   if not isinstance(multiplier, Rational):
      raise ValueError('multiplier must be rational.')

   if multiplier > Rational(1, 2) and multiplier < Rational(2):
      return True   

   return False
