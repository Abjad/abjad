from abjad.rational.rational import Rational
import math


def _closest_rational_with_denominator(
   rational, denominator, direction='below'):
   '''Given a rational number r = (p, q) and a denominator d, 
      compute Rational s = (n, d) closest to r, 
      either from above or below, depending on given direction. 
      Return rational computed and residue equal to r - s.'''

   assert isinstance(rational, Rational)

   if direction == 'below':
      numerator = int(math.floor(rational * denominator))
   else:
      numerator = int(math.ceil(rational * denominator))
   close_rational =  Rational(numerator, denominator)  
   residue = rational - close_rational

   return close_rational, residue
