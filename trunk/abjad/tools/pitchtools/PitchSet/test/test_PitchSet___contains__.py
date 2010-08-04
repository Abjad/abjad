from abjad import *


def test_PitchSet___contains___01( ):
   '''Pitch set containment works as expected.'''

   pset = pitchtools.PitchSet([12, 14, 18, 19])
   
   assert NamedPitch(14) in pset
   assert NamedPitch(15) not in pset
