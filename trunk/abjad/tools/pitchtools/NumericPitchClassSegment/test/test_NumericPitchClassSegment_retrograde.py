from abjad import *


def test_NumericPitchClassSegment_retrograde_01( ):

   pcseg = pitchtools.NumericPitchClassSegment([0, 6, 10, 4, 9, 2])
   PCSeg = pitchtools.NumericPitchClassSegment
   
   assert pcseg.retrograde( ) == PCSeg([2, 9, 4, 10, 6, 0])
