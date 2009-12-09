from abjad.tools.pitchtools.melodic_diatonic_interval_from_to import \
   melodic_diatonic_interval_from_to


def harmonic_counterpoint_interval_from_to(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return harmonic counterpoint interval `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.harmonic_counterpoint_interval_from_to(Pitch(-2), Pitch(12))
      HarmonicCounterpointInterval(9)

   ::

      abjad> pitchtools.harmonic_counterpoint_interval_from_to(Pitch(12), Pitch(-2))
      HarmonicCounterpointInterval(9)
   '''

   ## get melodic diatonic interval
   mdi = melodic_diatonic_interval_from_to(pitch_carrier_1, pitch_carrier_2)
   
   ## return harmonic counterpoint interval
   return mdi.harmonic_counterpoint_interval
