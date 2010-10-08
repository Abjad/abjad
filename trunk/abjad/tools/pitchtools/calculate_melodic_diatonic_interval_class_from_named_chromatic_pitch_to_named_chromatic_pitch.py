from abjad.tools.pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch import calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch


def calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic diatonic interval class from `pitch_carrier_1` to 
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(NamedChromaticPitch(-2), NamedChromaticPitch(12))
      MelodicDiatonicIntervalClass(ascending major second)

   ::

      abjad> pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch(NamedChromaticPitch(12), NamedChromaticPitch(-2))
      MelodicDiatonicIntervalClass(descending major second)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.melodic_diatonic_interval_class_from_to( )`` to
      ``pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.calculate_melodic_diatonic_interval_class_from_named_pitch_to_named_pitch( )`` to
      ``pitchtools.calculate_melodic_diatonic_interval_class_from_named_chromatic_pitch_to_named_chromatic_pitch( )``.
   '''

   ## get melodic diatonic interval
   mdi = calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(pitch_carrier_1, pitch_carrier_2)

   ## return melodic diatonic interval class
   return mdi.interval_class
