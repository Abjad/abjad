from abjad import *


def test_Clef_middle_c_position_01( ):

   assert Clef('treble').middle_c_position == -6
   assert Clef('alto').middle_c_position == 0
   assert Clef('tenor').middle_c_position == 2
   assert Clef('bass').middle_c_position == 6
