from abjad import *


def test_pitchtools_list_all_diatonic_interval_classes_01( ):

   all_dics = pitchtools.list_all_diatonic_interval_classes( )

   assert all_dics == [
      pitchtools.DiatonicIntervalClass('perfect', 1),
      pitchtools.DiatonicIntervalClass('augmented', 1),

      pitchtools.DiatonicIntervalClass('minor', 2),
      pitchtools.DiatonicIntervalClass('major', 2),
      pitchtools.DiatonicIntervalClass('augmented', 2),

      pitchtools.DiatonicIntervalClass('diminished', 3),
      pitchtools.DiatonicIntervalClass('minor', 3),
      pitchtools.DiatonicIntervalClass('major', 3),
      
      pitchtools.DiatonicIntervalClass('diminished', 4),
      pitchtools.DiatonicIntervalClass('perfect', 4),
      pitchtools.DiatonicIntervalClass('augmented', 4),
      ]
