from abjad.tools.pitchtools.MelodicChromaticInterval import \
   MelodicChromaticInterval
from abjad.tools.pitchtools.MelodicDiatonicInterval import \
   MelodicDiatonicInterval
from abjad.tools.pitchtools.transpose_by_chromatic_interval import \
   transpose_by_chromatic_interval
from abjad.tools.pitchtools.transpose_by_diatonic_interval import \
   transpose_by_diatonic_interval


def transpose_by_interval(pitch_carrier, interval):
   '''.. versionadded:: 1.1.2

   Transpose `pitch_carrier` by diatonic or chromatic `interval`. ::

      abjad> pitch = Pitch(12)
      abjad> pitch
      Pitch(c, 5)

   ::

      abjad> diatonic_interval = pitchtools.MelodicDiatonicInterval('minor', 2)
      abjad> diatonic_interval
      DiatonicInterval(ascending minor second)
      abjad> pitchtools.transpose_by_interval(pitch, diatonic_interval)
      Pitch(df, 5)

   ::

      abjad> chromatic_interval = pitchtools.MelodicChromaticInterval(1)
      abjad> chromatic_interval
      ChromaticInterval(1)
      abjad> pitchtools.transpose_by_interval(pitch, chromatic_interval)
      Pitch(cs, 5)
   '''

   if isinstance(interval, MelodicDiatonicInterval):
      return transpose_by_diatonic_interval(pitch_carrier, interval)
   elif isinstance(interval, MelodicChromaticInterval):
      return transpose_by_chromatic_interval(pitch_carrier, interval)
   else:
      raise TypeError('must be diatonic or chromatic interval.')
