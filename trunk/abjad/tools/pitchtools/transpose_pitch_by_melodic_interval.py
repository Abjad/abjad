from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval
from abjad.tools.pitchtools.transpose_pitch_by_melodic_chromatic_interval import transpose_pitch_by_melodic_chromatic_interval
from abjad.tools.pitchtools.tranpose_pitch_by_melodic_diatonic_interval import tranpose_pitch_by_melodic_diatonic_interval


def transpose_pitch_by_melodic_interval(pitch_carrier, melodic_interval):
   '''.. versionadded:: 1.1.2

   Transpose `pitch_carrier` by diatonic or chromatic `melodic_interval`. ::

      abjad> pitch = NamedPitch(12)
      abjad> pitch
      NamedPitch(c, 5)

   ::

      abjad> mdi = pitchtools.MelodicDiatonicInterval('minor', 2)
      abjad> mdi
      DiatonicInterval(ascending minor second)
      abjad> pitchtools.transpose_pitch_by_melodic_interval(pitch, mdi)
      NamedPitch(df, 5)

   ::

      abjad> mci = pitchtools.MelodicChromaticInterval(1)
      abjad> mci
      ChromaticInterval(1)
      abjad> pitchtools.transpose_pitch_by_melodic_interval(pitch, mci)
      NamedPitch(cs, 5)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.transpose_by_melodic_interval( )`` to
      ``pitchtools.transpose_pitch_by_melodic_interval( )``.
   '''

   if isinstance(melodic_interval, MelodicDiatonicInterval):
      return tranpose_pitch_by_melodic_diatonic_interval(
         pitch_carrier, melodic_interval)
   elif isinstance(melodic_interval, MelodicChromaticInterval):
      return transpose_pitch_by_melodic_chromatic_interval(
         pitch_carrier, melodic_interval)
   else:
      raise TypeError('must be diatonic or chromatic melodic interval.')
