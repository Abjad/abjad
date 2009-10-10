from abjad import *


def test_pitchtools_PitchSet___contains___01( ):
   '''Pitch set containment works as expected.'''

   pset = pitchtools.PitchSet([12, 14, 18, 19])
   
   assert Pitch(14) in pset
   assert Pitch(15) not in pset
