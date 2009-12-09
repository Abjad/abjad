from abjad.tools.pitchtools.MelodicChromaticInterval import \
   MelodicChromaticInterval
from abjad.tools.pitchtools.MelodicDiatonicInterval import \
   MelodicDiatonicInterval
from abjad.tools.pitchtools.transpose_by_melodic_chromatic_interval import \
   transpose_by_melodic_chromatic_interval
from abjad.tools.pitchtools.transpose_by_melodic_diatonic_interval import \
   transpose_by_melodic_diatonic_interval


def transpose_by_melodic_interval(pitch_carrier, melodic_interval):
   '''.. versionadded:: 1.1.2

   Transpose `pitch_carrier` by diatonic or chromatic `melodic_interval`. ::

      abjad> pitch = Pitch(12)
      abjad> pitch
      Pitch(c, 5)

   ::

      abjad> mdi = pitchtools.MelodicDiatonicInterval('minor', 2)
      abjad> mdi
      DiatonicInterval(ascending minor second)
      abjad> pitchtools.transpose_by_melodic_interval(pitch, mdi)
      Pitch(df, 5)

   ::

      abjad> mci = pitchtools.MelodicChromaticInterval(1)
      abjad> mci
      ChromaticInterval(1)
      abjad> pitchtools.transpose_by_melodic_interval(pitch, mci)
      Pitch(cs, 5)
   '''

   if isinstance(melodic_interval, MelodicDiatonicInterval):
      return transpose_by_melodic_diatonic_interval(
         pitch_carrier, melodic_interval)
   elif isinstance(melodic_interval, MelodicChromaticInterval):
      return transpose_by_melodic_chromatic_interval(
         pitch_carrier, melodic_interval)
   else:
      raise TypeError('must be diatonic or chromatic melodic interval.')
