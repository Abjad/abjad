from abjad.tools.pitchtools.melodic_chromatic_interval_from_to import \
   melodic_chromatic_interval_from_to


def melodic_chromatic_interval_class_from_to(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic chromatic interval class from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.melodic_chromatic_interval_class_from_to(Pitch(-2), Pitch(12))
      MelodicChromaticIntervalClass(+2)

   ::

      abjad> pitchtools.melodic_chromatic_interval_class_from_to(Pitch(12), Pitch(-2))
      MelodicChromaticIntervalClass(-2)
   '''

   ## get melodic chromatic interval
   mci = melodic_chromatic_interval_from_to(pitch_carrier_1, pitch_carrier_2)

   ## return melodic chromatic interval class
   return mci.interval_class
