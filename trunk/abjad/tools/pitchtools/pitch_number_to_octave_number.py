import math


def pitch_number_to_octave_number(pitch_number):
   '''Return integer octave number corresponding to `pitch_number`.

   ::

      abjad> pitchtools.pitch_number_to_octave_number(-12)
      3
      abjad> pitchtools.pitch_number_to_octave_number(-11)
      3
      abjad> pitchtools.pitch_number_to_octave_number(0)
      4
      abjad> pitchtools.pitch_number_to_octave_number(1)
      4
      abjad> pitchtools.pitch_number_to_octave_number(12)
      5
      abjad> pitchtools.pitch_number_to_octave_number(13)
      5

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_number_to_octave( )`` to
      ``pitchtools.pitch_number_to_octave_number( )``.
   '''

   return int(math.floor(pitch_number / 12)) + 4
