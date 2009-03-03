from abjad.rational.rational import Rational
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.is_duration_token import _is_duration_token

def rationalize(lst):
   '''
   Converts a list of duration tokens into Rationals. 
   The given list can be a list of lists of ... lists of duration tokens.
   The list returned will preserve nesting.
   '''
   assert isinstance(lst, list)
   result = [ ]
   for element in lst:
      if _is_duration_token(element):
         r = Rational(*_duration_token_unpack(element))
      else:
         r = rationalize(element)
      result.append(r)
   return result


#def _rationalize(meth):
#   '''Convert method argument from list or tuple to Rational.
#      meth((m, n)) --> meth(Rational(m, n))
#   '''
#   def new(self, arg):
#      if isinstance(arg, (list, tuple)):
#         assert len(arg) < 3
#         arg = Rational(*arg)
#      return meth(self, arg)
#   return new

