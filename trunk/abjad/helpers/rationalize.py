from abjad.rational.rational import Rational
from abjad.tools import durtools
from abjad.tools import durtools


def rationalize(lst):
   '''Converts a list of duration tokens into Rationals. 
      The given list can be a list of lists of ... lists of duration tokens.
      The list returned will preserve nesting.'''

   assert isinstance(lst, list)
   result = [ ]
   for element in lst:
      if durtools.is_token(element):
         r = Rational(*durtools.token_unpack(element))
      else:
         r = rationalize(element)
      result.append(r)
   return result
