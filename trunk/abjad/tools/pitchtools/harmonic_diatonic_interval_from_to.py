from abjad.tools.pitchtools.melodic_diatonic_interval_from_to import \
   melodic_diatonic_interval_from_to


def harmonic_diatonic_interval_from_to(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return harmonic diatonic interval from `pitch_carrier_1` to 
   `pitch_carrier_2`. ::

      abjad> pitchtools.harmonic_diatonic_interval_from_to(NamedPitch(-2), NamedPitch(12))
      HarmonicDiatonicInterval(major ninth)

   ::

      abjad> pitchtools.harmonic_diatonic_interval_from_to(NamedPitch(12), NamedPitch(-2))
      HarmonicDiatonicInterval(major ninth)
   '''

   ## get melodic diatonic interval
   mdi = melodic_diatonic_interval_from_to(pitch_carrier_1, pitch_carrier_2)

   ## return harmonic diatonic interval
   return mdi.harmonic_diatonic_interval
