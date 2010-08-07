from abjad import *


def test_NamedPitchClassSegment_diatonic_interval_class_segment_01( ):

   npcseg = pitchtools.NamedPitchClassSegment(['c', 'd', 'e', 'f'])
   dicseg = pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
      pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2),
      pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2),
      pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2)])
   npcseg.diatonic_interval_class_segment == dicseg
