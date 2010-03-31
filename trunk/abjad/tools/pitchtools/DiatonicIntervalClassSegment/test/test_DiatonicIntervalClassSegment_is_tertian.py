from abjad import *


def test_DiatonicIntervalClassSegment_is_tertian_01( ):

   dicseg = pitchtools.DiatonicIntervalClassSegment([
      pitchtools.DiatonicIntervalClass('major', 3),
      pitchtools.DiatonicIntervalClass('minor', 3),
      pitchtools.DiatonicIntervalClass('diminshed', 3)])
   
   assert dicseg.is_tertian


def test_DiatonicIntervalClassSegment_is_tertian_02( ):

   dicseg = pitchtools.DiatonicIntervalClassSegment([
      pitchtools.DiatonicIntervalClass('major', 2),
      pitchtools.DiatonicIntervalClass('minor', 3),
      pitchtools.DiatonicIntervalClass('diminshed', 3)])
   
   assert not dicseg.is_tertian
