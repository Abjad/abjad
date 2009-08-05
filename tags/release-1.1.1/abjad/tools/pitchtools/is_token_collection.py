from abjad.tools.pitchtools.is_token import is_token


def is_token_collection(arg):
   '''Returns True when arg has the form of a list,
      tuple or set of Abjad pitch tokens,
      otherwise False.'''

   if isinstance(arg, (list, tuple, set)):
      if all([is_token(x) for x in arg]):
         return True
   return False
