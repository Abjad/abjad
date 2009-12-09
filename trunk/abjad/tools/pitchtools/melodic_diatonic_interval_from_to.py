from abjad.tools.pitchtools.diatonic_and_chromatic_interval_numbers_to_diatonic_interval import diatonic_and_chromatic_interval_numbers_to_diatonic_interval
from abjad.tools.pitchtools.get_pitch import get_pitch


def melodic_diatonic_interval_from_to(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic diatonic interval from `pitch_carrier_1` to 
   `pitch_carrier_2`. ::

      abjad> pitchtools.melodic_diatonic_interval_from_to(Pitch(-2), Pitch(12))
      MelodicDiatonicInterval(ascending major ninth)

   ::

      abjad> pitchtools.melodic_diatonic_interval_from_to(Pitch(12), Pitch(-2))
      MelodicDiatonicInterval(descending major ninth)
   '''

   pitch_1 = get_pitch(pitch_carrier_1)
   pitch_2 = get_pitch(pitch_carrier_2)

   degree_1 = pitch_1.absolute_diatonic_scale_degree
   degree_2 = pitch_2.absolute_diatonic_scale_degree

   diatonic_interval_number = abs(degree_1 - degree_2) + 1
   
   chromatic_interval_number = abs(pitch_1.number - pitch_2.number)

   absolute_diatonic_interval = \
      diatonic_and_chromatic_interval_numbers_to_diatonic_interval(
      diatonic_interval_number, chromatic_interval_number)

   if pitch_2 < pitch_1:
      diatonic_interval = -absolute_diatonic_interval
   else:
      diatonic_interval = absolute_diatonic_interval

   return diatonic_interval
