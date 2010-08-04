from abjad import *
import copy


def test_NamedPitch___deepcopy___01( ):

   pitch = NamedPitch(13)
   new = copy.deepcopy(pitch)

   assert new is not pitch
   assert new.accidental is not pitch.accidental
