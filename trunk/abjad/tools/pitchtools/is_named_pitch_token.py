from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools.pitchtools.is_named_pitch_pair import is_named_pitch_pair


def is_named_pitch_token(pitch_token):
   '''True when `pitch_token` has the form of 
   an Abjad pitch token. ::

      abjad> pitchtools.is_named_pitch_token(('c', 4))
      True
      abjad> pitchtools.is_named_pitch_token(NamedPitch('c', 4))
      True

   Otherwise false. ::

      abjad> pitchtools.is_named_pitch_token('foo')
      False

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.is_pitch_token( )`` to
      ``pitchtools.is_named_pitch_token( )``.
   '''

   if isinstance(pitch_token, NamedPitch):
      return True
   elif is_named_pitch_pair(pitch_token):
      return True
   elif isinstance(pitch_token, (int, long)):
      return True
   elif isinstance(pitch_token, float) and pitch_token % 0.5 == 0:
      return True
   else:
      return False
