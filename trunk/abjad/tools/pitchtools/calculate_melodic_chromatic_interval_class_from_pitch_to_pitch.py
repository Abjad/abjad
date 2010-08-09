from abjad.tools.pitchtools.calculate_melodic_chromatic_interval_from_pitch_to_pitch import calculate_melodic_chromatic_interval_from_pitch_to_pitch


def calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic chromatic interval class from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(NamedPitch(-2), NamedPitch(12))
      MelodicChromaticIntervalClass(+2)

   ::

      abjad> pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch(NamedPitch(12), NamedPitch(-2))
      MelodicChromaticIntervalClass(-2)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.melodic_chromatic_interval_class_from_to( )`` to
      ``pitchtools.calculate_melodic_chromatic_interval_class_from_pitch_to_pitch( )``.
   '''

   ## get melodic chromatic interval
   mci = calculate_melodic_chromatic_interval_from_pitch_to_pitch(pitch_carrier_1, pitch_carrier_2)

   ## return melodic chromatic interval class
   return mci.interval_class
