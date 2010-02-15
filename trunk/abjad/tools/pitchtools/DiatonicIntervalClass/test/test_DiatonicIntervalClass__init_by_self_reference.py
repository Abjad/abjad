from abjad import *


def test_DiatonicIntervalClass__init_by_self_reference_01( ):

   dic_1 = pitchtools.DiatonicIntervalClass('major', 2)
   dic_2 = pitchtools.DiatonicIntervalClass(dic_1)

   assert str(dic_1) == 'M2'
   assert str(dic_2) == 'M2'
