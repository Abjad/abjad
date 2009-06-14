from abjad.rational import Rational
from abjad.tools.durtools.is_token import is_token
from abjad.tools.durtools.token_unpack import token_unpack


def rationalize(lst):
   '''Converts a list of duration tokens into Rationals. 
      The given list can be a list of lists of ... lists of duration tokens.
      The list returned will preserve nesting.'''

   assert isinstance(lst, list)
   result = [ ]
   for element in lst:
      if is_token(element):
         r = Rational(*token_unpack(element))
      else:
         r = rationalize(element)
      result.append(r)
   return result
