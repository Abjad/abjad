from abjad.helpers.is_pitch_name import _is_pitch_name


def _is_pitch_pair(arg):
   '''Returns True when arg has the form of an
      Ajbad pitch pair, otherwise False.'''
   if isinstance(arg, tuple) and len(arg) == 2 and \
      _is_pitch_name(arg[0]) and isinstance(arg[1], (int, long)):
      return True
   else:
      return False
