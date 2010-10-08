from abjad.tools.pitchtools.diatonic_interval_number_and_chromatic_interval_number_to_melodic_diatonic_interval import diatonic_interval_number_and_chromatic_interval_number_to_melodic_diatonic_interval
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import get_named_chromatic_pitch_from_pitch_carrier


def calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch(
   pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic diatonic interval from `pitch_carrier_1` to 
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch(NamedPitch(-2), NamedPitch(12))
      MelodicDiatonicInterval(ascending major ninth)

   ::

      abjad> pitchtools.calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch(NamedPitch(12), NamedPitch(-2))
      MelodicDiatonicInterval(descending major ninth)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.melodic_diatonic_interval_from_to( )`` to
      ``pitchtools.calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitches_to_diatonic_interval( )`` to
      ``pitchtools.calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch( )``.
   '''

   pitch_1 = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_1)
   pitch_2 = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier_2)

   degree_1 = pitch_1.diatonic_pitch_number
   degree_2 = pitch_2.diatonic_pitch_number
   
   diatonic_interval_number = abs(degree_1 - degree_2) + 1
   
   chromatic_interval_number = abs(pitch_1.pitch_number - pitch_2.pitch_number)

   absolute_diatonic_interval = \
      diatonic_interval_number_and_chromatic_interval_number_to_melodic_diatonic_interval(
      diatonic_interval_number, chromatic_interval_number)

   if pitch_2 < pitch_1:
      diatonic_interval = -absolute_diatonic_interval
   else:
      diatonic_interval = absolute_diatonic_interval

   return diatonic_interval
