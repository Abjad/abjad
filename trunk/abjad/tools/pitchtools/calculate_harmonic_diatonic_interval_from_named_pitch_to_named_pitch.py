from abjad.tools.pitchtools.calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch import calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch


def calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return harmonic diatonic interval from `pitch_carrier_1` to 
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(NamedPitch(-2), NamedPitch(12))
      HarmonicDiatonicInterval(major ninth)

   ::

      abjad> pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch(NamedPitch(12), NamedPitch(-2))
      HarmonicDiatonicInterval(major ninth)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.harmonic_diatonic_interval_from_to( )`` to
      ``pitchtools.calculate_harmonic_diatonic_interval_from_named_pitch_to_named_pitch( )``.
   '''

   ## get melodic diatonic interval
   mdi = calculate_melodic_diatonic_interval_from_named_pitch_to_named_pitch(pitch_carrier_1, pitch_carrier_2)

   ## return harmonic diatonic interval
   return mdi.harmonic_diatonic_interval
