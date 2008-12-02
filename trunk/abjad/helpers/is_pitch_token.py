from abjad.helpers.is_pitch_pair import _is_pitch_pair
from abjad.pitch.pitch import Pitch


def _is_pitch_token(arg):
   '''Returns True when arg has the form of an
      Abjad pitch token, otherwise False.'''
   if isinstance(arg, Pitch):
      return True
   elif _is_pitch_pair(arg):
      return True
   elif isinstance(arg, (int, long)):
      return True
   elif isinstance(arg, float) and arg % 0.5 == 0:
      return True
   else:
      return False
