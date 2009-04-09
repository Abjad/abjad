from abjad.rational.rational import Rational
from abjad.tools.durtools.is_pair import is_pair


def is_token(arg):
   '''Returns True when arg meets the criteria 
      for an Abjad duration token, otherwise False.'''

   if is_pair(arg):
      return True
   elif isinstance(arg, Rational) and arg > 0:
      return True
   elif isinstance(arg, (int, long)) and arg > 0:
      return True
   else:
      return False
