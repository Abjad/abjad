from abjad import *


def test_PitchClassSegment_invert_01( ):

   pcseg = pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])

   assert pcseg.invert( ) == pitchtools.PitchClassSegment([0, 6, 2, 8, 3, 10])
