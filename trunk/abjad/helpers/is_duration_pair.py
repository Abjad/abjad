from abjad.rational.rational import Rational


def _is_duration_pair(arg):
   '''Returns True when arg has the form of a pair
      of integers that initialize a positive Rational,
      otherwise False.'''
   try:
      arg = Rational(*arg)
   except:
      return False

   if arg > 0:
      return True
   else:
      return False
