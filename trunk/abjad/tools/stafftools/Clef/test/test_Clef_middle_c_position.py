from abjad import *


def test_Clef_middle_c_position_01( ):

   assert stafftools.Clef('treble').middle_c_position == -6
   assert stafftools.Clef('alto').middle_c_position == 0
   assert stafftools.Clef('tenor').middle_c_position == 2
   assert stafftools.Clef('bass').middle_c_position == 6
