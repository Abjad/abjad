from abjad.tools.pitchtools.is_pitch_name import is_pitch_name


def is_named_pitch_pair(arg):
   '''True when `pitch_pair` has the form of an
   Ajbad pitch pair. ::

      abjad> pitchtools.is_named_pitch_pair(('c', 4))
      True

   Otherwise false. ::

      abjad> pitchtools.is_named_pitch_pair(('foo', 4))
      False
      abjad> pitchtools.is_named_pitch_pair('c,,4')
      False

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.is_pair( )`` to
      ``pitchtools.is_named_pitch_pair( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.is_pitch_pair( )`` to
      ``pitchtools.is_named_pitch_pair( )``.
   '''

   if isinstance(arg, tuple) and len(arg) == 2 and \
      is_pitch_name(arg[0]) and isinstance(arg[1], (int, long)):
      return True
   else:
      return False
