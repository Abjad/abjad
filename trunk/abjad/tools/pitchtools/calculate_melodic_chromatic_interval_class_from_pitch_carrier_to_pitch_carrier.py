from abjad.tools.pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier import calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier


def calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic chromatic interval class from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(NamedChromaticPitch(-2), NamedChromaticPitch(12))
      MelodicChromaticIntervalClass(+2)

   ::

      abjad> pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier(NamedChromaticPitch(12), NamedChromaticPitch(-2))
      MelodicChromaticIntervalClass(-2)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.melodic_chromatic_interval_class_from_to( )`` to
      ``pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch( )`` to
      ``pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_carrier_to_pitch_carrier( )``.
   '''

   ## get melodic chromatic interval
   mci = calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(pitch_carrier_1, pitch_carrier_2)

   ## return melodic chromatic interval class
   return mci.interval_class
