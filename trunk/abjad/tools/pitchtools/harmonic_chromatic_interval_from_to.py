from abjad.tools.pitchtools.melodic_diatonic_interval_from_to import \
   melodic_diatonic_interval_from_to


def harmonic_chromatic_interval_from_to(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return harmonic chromatic interval from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.harmonic_chromatic_interval_from_to(Pitch(-2), Pitch(12))
      HarmonicChromaticInterval(14)

   ::

      abjad> pitchtools.harmonic_chromatic_interval_from_to(Pitch(12), Pitch(-2))
      HarmonicChromaticInterval(14)
   '''

   ## get melodic diatonic interval
   mdi = melodic_diatonic_interval_from_to(pitch_carrier_1, pitch_carrier_2)

   ## return harmonic chromatic interval
   return mdi.harmonic_chromatic_interval
