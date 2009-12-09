from abjad.tools.pitchtools.melodic_diatonic_interval_from_to import \
   melodic_diatonic_interval_from_to


def melodic_diatonic_interval_class_from_to(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return melodic diatonic interval class from `pitch_carrier_1` to 
   `pitch_carrier_2`. ::

      abjad> pitchtools.melodic_diatonic_interval_class_from_to(Pitch(-2), Pitch(12))
      MelodicDiatonicIntervalClass(ascending major second)

   ::

      abjad> pitchtools.melodic_diatonic_interval_class_from_to(Pitch(12), Pitch(-2))
      MelodicDiatonicIntervalClass(descending major second)
   '''

   ## get melodic diatonic interval
   mdi = melodic_diatonic_interval_from_to(pitch_carrier_1, pitch_carrier_2)

   ## return melodic diatonic interval class
   return mdi.interval_class
