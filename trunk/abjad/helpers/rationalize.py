from abjad.rational.rational import Rational
from abjad.helpers.duration_token_unpack import _duration_token_unpack

def rationalize(duples):
   '''
   Converts a list of duration duples (n, m) into Rationals. 
   The given list can be a list of lists of ... lists of duples.
   The list returned will preserve nesting.
   '''
   assert isinstance(duples, list)
   result = [ ]
   for element in duples:
      if isinstance(element, tuple):
         r = Rational(*_duration_token_unpack(element))
      elif isinstance(element, Rational):
         r = element
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

