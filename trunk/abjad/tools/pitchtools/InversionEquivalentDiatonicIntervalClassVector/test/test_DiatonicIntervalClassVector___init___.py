from abjad import *


def test_DiatonicIntervalClassVector___init____01( ):

   dicv = pitchtools.InversionEquivalentDiatonicIntervalClassVector(macros.scale(4))

   assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2)] == 1
   assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2)] == 2
   assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3)] == 1
   assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3)] == 1
   assert dicv[pitchtools.InversionEquivalentDiatonicIntervalClass('perfect', 4)] == 1
