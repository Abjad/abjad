from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval
from abjad.tools.pitchtools._transpose_pitch_carrier_by_melodic_chromatic_interval import _transpose_pitch_carrier_by_melodic_chromatic_interval
from abjad.tools.pitchtools._transpose_pitch_carrier_by_melodic_diatonic_interval import _transpose_pitch_carrier_by_melodic_diatonic_interval


def transpose_pitch_carrier_by_melodic_interval(pitch_carrier, melodic_interval):
   '''.. versionadded:: 1.1.2

   Transpose `pitch_carrier` by diatonic or chromatic `melodic_interval`::

      abjad> pitch = NamedChromaticPitch(12)
      abjad> pitch
      NamedChromaticPitch(c, 5)

   ::

      abjad> mdi = pitchtools.MelodicDiatonicInterval('minor', 2)
      abjad> mdi
      DiatonicInterval(ascending minor second)
      abjad> pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, mdi)
      NamedChromaticPitch(df, 5)

   ::

      abjad> mci = pitchtools.MelodicChromaticInterval(1)
      abjad> mci
      ChromaticInterval(1)
      abjad> pitchtools.transpose_pitch_carrier_by_melodic_interval(pitch, mci)
      NamedChromaticPitch(cs, 5)

   Return named chromatic pitch.
   '''

   if isinstance(melodic_interval, MelodicDiatonicInterval):
      return _transpose_pitch_carrier_by_melodic_diatonic_interval(
         pitch_carrier, melodic_interval)
   elif isinstance(melodic_interval, MelodicChromaticInterval):
      return _transpose_pitch_carrier_by_melodic_chromatic_interval(
         pitch_carrier, melodic_interval)
   else:
      raise TypeError('must be diatonic or chromatic melodic interval.')
