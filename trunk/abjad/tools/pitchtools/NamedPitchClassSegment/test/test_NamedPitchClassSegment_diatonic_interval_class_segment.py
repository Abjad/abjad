from abjad import *


def test_NamedPitchClassSegment_diatonic_interval_class_segment_01( ):

   npcseg = pitchtools.NamedPitchClassSegment(['c', 'd', 'e', 'f'])
   dicseg = pitchtools.DiatonicIntervalClassSegment([
      pitchtools.DiatonicIntervalClass('major', 2),
      pitchtools.DiatonicIntervalClass('major', 2),
      pitchtools.DiatonicIntervalClass('minor', 2)])
   npcseg.diatonic_interval_class_segment == dicseg
