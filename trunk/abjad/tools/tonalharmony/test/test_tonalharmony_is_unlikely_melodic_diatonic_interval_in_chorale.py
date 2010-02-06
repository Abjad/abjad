from abjad import *


def test_tonalharmony_is_unlikely_melodic_diatonic_interval_in_chorale_01( ):

   mdi = pitchtools.MelodicDiatonicInterval('major', 6)
   result = tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
   assert result
   
   mdi = pitchtools.MelodicDiatonicInterval('major', 7)
   result = tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
   assert result
   
   mdi = pitchtools.MelodicDiatonicInterval('major', 9)
   result = tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
   assert result
   

def test_tonalharmony_is_unlikely_melodic_diatonic_interval_in_chorale_02( ):

   mdi = pitchtools.MelodicDiatonicInterval('perfect', 1)
   result = tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
   assert result == False
   
   mdi = pitchtools.MelodicDiatonicInterval('major', 2)
   result = tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
   assert result == False
   
   mdi = pitchtools.MelodicDiatonicInterval('major', 3)
   result = tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
   assert result == False
   
   mdi = pitchtools.MelodicDiatonicInterval('perfect', 4)
   result = tonalharmony.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
   assert result == False
