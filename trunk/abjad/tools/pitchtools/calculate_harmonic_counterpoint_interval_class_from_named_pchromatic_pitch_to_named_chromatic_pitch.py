from abjad.tools.pitchtools.calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch import calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch


def calculate_harmonic_counterpoint_interval_class_from_named_pchromatic_pitch_to_named_chromatic_pitch(
   pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return harmonic counterpoint interval class from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_pchromatic_pitch_to_named_chromatic_pitch(NamedChromaticPitch(-2), NamedChromaticPitch(12))
      HarmonicCounterpointIntervalClass(2)

   ::

      abjad> pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_pchromatic_pitch_to_named_chromatic_pitch(NamedChromaticPitch(12), NamedChromaticPitch(-2))
      HarmonicCounterpointIntervalClass(2)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.harmonic_counterpoint_interval_class_from_to( )`` to
      ``pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_pchromatic_pitch_to_named_chromatic_pitch( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_pitch_to_named_pitch( )`` to
      ``pitchtools.calculate_harmonic_counterpoint_interval_class_from_named_pchromatic_pitch_to_named_chromatic_pitch( )``.
   '''

   ## get melodic diatonic interval
   mdi = calculate_melodic_diatonic_interval_from_named_chromatic_pitch_to_named_chromatic_pitch(pitch_carrier_1, pitch_carrier_2)
  
   ## return harmonic counterpoint interval class
   return mdi.harmonic_counterpoint_interval.interval_class
