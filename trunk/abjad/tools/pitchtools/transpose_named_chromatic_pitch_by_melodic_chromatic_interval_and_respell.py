from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name import one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name


def transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(
   pitch, staff_spaces, melodic_chromatic_interval):
   '''.. versionadded:: 1.1.1

   Transpose named chromatic pitch by `melodic_chromatic_interval` and respell `staff_spaces`
   above or below::

      abjad> pitch = NamedChromaticPitch(0)
      abjad> pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 0.5)
      NamedChromaticPitch('dtqf', 4)

   Return new named chromatic pitch.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.staff_space_transpose( )`` to
      ``pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell( )``.
   '''

   pitch_number = abs(pitch.numbered_chromatic_pitch) + melodic_chromatic_interval
   diatonic_scale_degree = \
      (pitch.numbered_diatonic_pitch_class._diatonic_pitch_class_number + 1) + staff_spaces
   letter = one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(
      diatonic_scale_degree)
   return NamedChromaticPitch(pitch_number, letter)
