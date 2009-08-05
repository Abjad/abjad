from abjad.rational import Rational


def is_pair(arg):
   '''Returns True when arg has the form of a pair
      of integers that initialize a positive Rational,
      otherwise False.'''

   if isinstance(arg, (list, tuple)) and len(arg) != 2:
      return False

   try:
      arg = Rational(*arg)
   except:
      return False

   if arg > 0:
      return True
   else:
      return False
