from abjad.pitch import Pitch
from abjad.tools.pitchtools.is_pair import is_pair


def is_token(pitch_token):
   '''True when `pitch_token` has the form of 
   an Abjad pitch token. ::

      abjad> pitchtools.is_token(('c', 4))
      True
      abjad> pitchtools.is_token(Pitch('c', 4))
      True

   Otherwise false. ::

      abjad> pitchtools.is_token('foo')
      False
   '''

   if isinstance(pitch_token, Pitch):
      return True
   elif is_pair(pitch_token):
      return True
   elif isinstance(pitch_token, (int, long)):
      return True
   elif isinstance(pitch_token, float) and pitch_token % 0.5 == 0:
      return True
   else:
      return False
