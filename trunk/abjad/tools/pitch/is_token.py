from abjad.tools.pitch.is_pair import is_pair


def is_token(arg):
   '''True when arg has the form of an Abjad pitch token.
      Otherwise False.'''

   from abjad.pitch.pitch import Pitch
   if isinstance(arg, Pitch):
      return True
   elif is_pair(arg):
      return True
   elif isinstance(arg, (int, long)):
      return True
   elif isinstance(arg, float) and arg % 0.5 == 0:
      return True
   else:
      return False
