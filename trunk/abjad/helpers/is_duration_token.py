from abjad.helpers.is_duration_pair import _is_duration_pair
from abjad.rational.rational import Rational


def _is_duration_token(arg):
   '''Returns True when arg meets the criteria 
      for an Abjad duration token, otherwise False.'''
   if _is_duration_pair(arg):
      return True
   elif isinstance(arg, Rational) and arg > 0:
      return True
   elif isinstance(arg, (int, long)) and arg > 0:
      return True
   else:
      return False
