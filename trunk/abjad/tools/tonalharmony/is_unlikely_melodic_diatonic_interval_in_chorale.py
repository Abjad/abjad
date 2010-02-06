from abjad.tools import pitchtools


def is_unlikely_melodic_diatonic_interval_in_chorale(mdi):
   '''.. versionadded:: 1.1.2

   True when `mdi` is unlikely melodic diatonic interval in JSB chorale. ::

      abjad> mdi = pitchtools.MelodicDiatonicInterval('major', 7)
      abjad> tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
      True

   Otherwise False. ::

      abjad> mdi = pitchtools.MelodicDiatonicInterval('major', 2)
      abjad> tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
      False
   '''
 
   hdi = mdi.harmonic_diatonic_interval
   hcpi = mdi.harmonic_counterpoint_interval

   if hcpi == pitchtools.HarmonicCounterpointInterval(6):
      return True
   elif hcpi == pitchtools.HarmonicCounterpointInterval(7):
      return True
   elif 8 < hdi.number:
      return True
   elif mdi.quality_string not in ('major', 'minor', 'perfect'):
      return True

   return False
