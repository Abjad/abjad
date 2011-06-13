from abjad import *


def test_Measure_is_full_01( ):

   assert Measure((3, 8), "c'8 d'8 e'8").is_full
   assert not Measure((3, 8), macros.scale(2)).is_full
   assert not Measure((3, 8), macros.scale(4)).is_full
