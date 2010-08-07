from abjad import *


def test_PitchSet_issuperset_01( ):

   pitch_set_1 = pitchtools.NamedPitchSet([-1, 3, 4])
   pitch_set_2 = pitchtools.NamedPitchSet(range(-5, 5))

   assert not pitch_set_1.issuperset(pitch_set_2)
   assert pitch_set_2.issuperset(pitch_set_1)


def test_PitchSet_issuperset_02( ):

   pitch_set_1 = pitchtools.NamedPitchSet([0, 1, 2])
   pitch_set_2 = pitchtools.NamedPitchSet([0, 1, 2])

   assert pitch_set_1.issuperset(pitch_set_2)
   assert pitch_set_2.issuperset(pitch_set_1)
