from abjad.tools.pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier import calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier


def calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return harmonic chromatic interval class from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(NamedChromaticPitch(-2), NamedChromaticPitch(12))
      HarmonicChromaticIntervalClass(2)

   ::

      abjad> pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(NamedChromaticPitch(12), NamedChromaticPitch(-2))
      HarmonicChromaticIntervalClass(2)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.harmonic_chromatic_interval_class_from_to( )`` to
      ``pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_to_pitch( )`` to
      ``pitchtools.calculate_harmonic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier( )``.
   '''

   ## get melodic chromatic interval
   mci = calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(pitch_carrier_1, pitch_carrier_2)

   ## return harmonic chromatic interval class
   return mci.harmonic_chromatic_interval.interval_class
