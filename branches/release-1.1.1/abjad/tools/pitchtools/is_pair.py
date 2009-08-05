from abjad.tools.pitchtools.is_name import is_name


def is_pair(arg):
   '''Returns True when arg has the form of an
      Ajbad pitch pair, otherwise False.'''

   if isinstance(arg, tuple) and len(arg) == 2 and \
      is_name(arg[0]) and isinstance(arg[1], (int, long)):
      return True
   else:
      return False
