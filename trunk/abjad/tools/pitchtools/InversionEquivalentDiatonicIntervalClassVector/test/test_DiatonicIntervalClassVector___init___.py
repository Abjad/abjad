from abjad import *


def test_DiatonicIntervalClassVector___init____01( ):

   dicv = pitchtools.DiatonicIntervalClassVector(macros.scale(4))

   assert dicv[pitchtools.DiatonicIntervalClass('minor', 2)] == 1
   assert dicv[pitchtools.DiatonicIntervalClass('major', 2)] == 2
   assert dicv[pitchtools.DiatonicIntervalClass('minor', 3)] == 1
   assert dicv[pitchtools.DiatonicIntervalClass('major', 3)] == 1
   assert dicv[pitchtools.DiatonicIntervalClass('perfect', 4)] == 1
