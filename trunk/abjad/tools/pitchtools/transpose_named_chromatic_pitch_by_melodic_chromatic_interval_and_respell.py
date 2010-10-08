from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name import \
   one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name


def transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(
   pitch, staff_spaces, absolute_interval):
   '''Transpose `pitch` by `absolute_interval` and renotate on the
   scale degree `staff_spaces` above or below. 

   Return new pitch instance. ::

      abjad> pitch = NamedChromaticPitch(0)
      abjad> pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 0.5)
      NamedChromaticPitch('dtqf', 4)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.staff_space_transpose( )`` to
      ``pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell_enharmonically( )`` to
      ``pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell( )``.
   '''

   pitch_number = pitch.pitch_number + absolute_interval
   #diatonic_scale_degree = pitch.degree + staff_spaces
   diatonic_scale_degree = (pitch.diatonic_pitch_class_number + 1) + staff_spaces
   letter = one_indexed_diatonic_scale_degree_number_to_diatonic_pitch_class_name(diatonic_scale_degree)
   return NamedChromaticPitch(pitch_number, letter)
