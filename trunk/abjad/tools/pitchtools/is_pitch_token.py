from abjad.pitch import Pitch
from abjad.tools.pitchtools.is_pitch_pair import is_pitch_pair


def is_pitch_token(pitch_token):
   '''True when `pitch_token` has the form of 
   an Abjad pitch token. ::

      abjad> pitchtools.is_pitch_token(('c', 4))
      True
      abjad> pitchtools.is_pitch_token(Pitch('c', 4))
      True

   Otherwise false. ::

      abjad> pitchtools.is_pitch_token('foo')
      False
   '''

   if isinstance(pitch_token, Pitch):
      return True
   elif is_pitch_pair(pitch_token):
      return True
   elif isinstance(pitch_token, (int, long)):
      return True
   elif isinstance(pitch_token, float) and pitch_token % 0.5 == 0:
      return True
   else:
      return False
