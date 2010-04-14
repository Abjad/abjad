from abjad import *
import copy


def test_Pitch___copy___01( ):

   pitch = Pitch(13)
   new = copy.copy(pitch)

   assert new is not pitch
   assert new.accidental is not pitch.accidental
