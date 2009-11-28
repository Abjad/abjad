from abjad.tools.pitchtools.ChromaticInterval import ChromaticInterval
from abjad.tools.pitchtools.get_pitch import get_pitch


def chromatic_interval_from_to(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return chromatic interval from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.chromatic_interval_from_to(Pitch(12), Pitch(10))
      ChromaticInterval(-2)
   '''

   pitch_1 = get_pitch(pitch_carrier_1)
   pitch_2 = get_pitch(pitch_carrier_2)

   chromatic_interval_number = pitch_2.number - pitch_1.number
   chromatic_interval = ChromaticInterval(chromatic_interval_number)

   return chromatic_interval
