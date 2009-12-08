from abjad.tools.pitchtools.MelodicChromaticInterval import \
   MelodicChromaticInterval
from abjad.tools.pitchtools.get_pitch import get_pitch


def melodic_chromatic_interval_from_to(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic chromatic interval from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.melodic_chromatic_interval_from_to(Pitch(12), Pitch(10))
      MelodicChromaticInterval(-2)
   '''

   pitch_1 = get_pitch(pitch_carrier_1)
   pitch_2 = get_pitch(pitch_carrier_2)

   chromatic_interval_number = pitch_2.number - pitch_1.number
   chromatic_interval = MelodicChromaticInterval(chromatic_interval_number)

   return chromatic_interval
