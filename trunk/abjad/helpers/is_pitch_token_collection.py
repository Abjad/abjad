from abjad.helpers.is_pitch_token import _is_pitch_token


def _is_pitch_token_collection(arg):
   '''Returns True when arg has the form of a list,
      tuple or set of Abjad pitch tokens,
      otherwise False.'''
   if isinstance(arg, (list, tuple, set)):
      if all([_is_pitch_token(x) for x in arg]):
         return True
   return False
