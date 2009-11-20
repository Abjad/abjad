from abjad.tools.pitchtools.is_name import is_name


def is_pair(arg):
   '''True when `pitch_pair` has the form of an
   Ajbad pitch pair. ::

      abjad> pitchtools.is_pair(('c', 4))
      True

   Otherwise false. ::

      abjad> pitchtools.is_pair(('foo', 4))
      False
      abjad> pitchtools.is_pair('c,,4')
      False
   '''

   if isinstance(arg, tuple) and len(arg) == 2 and \
      is_name(arg[0]) and isinstance(arg[1], (int, long)):
      return True
   else:
      return False
