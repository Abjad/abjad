from abjad.tools.pitchtools.calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier import calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier


def calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(pitch_carrier_1, pitch_carrier_2):
   '''.. versionadded:: 1.1.2

   Return harmonic chromatic interval from `pitch_carrier_1` to
   `pitch_carrier_2`. ::

      abjad> pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(NamedPitch(-2), NamedPitch(12))
      HarmonicChromaticInterval(14)

   ::

      abjad> pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(NamedPitch(12), NamedPitch(-2))
      HarmonicChromaticInterval(14)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.harmonic_chromatic_interval_from_to( )`` to
      ``pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.calculate_harmonic_chromatic_interval_from_pitch_to_pitch( )`` to
      ``pitchtools.calculate_harmonic_chromatic_interval_from_pitch_carrier_to_pitch_carrier( )``.
   '''

   ## get melodic chromatic interval
   mci = calculate_melodic_chromatic_interval_from_pitch_carrier_to_pitch_carrier(pitch_carrier_1, pitch_carrier_2)

   ## return harmonic chromatic interval
   return mci.harmonic_chromatic_interval
