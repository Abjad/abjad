from abjad import *


def test_PitchClassSegment_retrograde_01( ):

   pcseg = pitchtools.PitchClassSegment([0, 6, 10, 4, 9, 2])
   PCSeg = pitchtools.PitchClassSegment
   
   assert pcseg.retrograde( ) == PCSeg([2, 9, 4, 10, 6, 0])
