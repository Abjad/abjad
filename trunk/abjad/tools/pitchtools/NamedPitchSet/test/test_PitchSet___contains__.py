from abjad import *


def test_PitchSet___contains___01( ):
   '''Pitch set containment works as expected.'''

   pset = pitchtools.NamedPitchSet([12, 14, 18, 19])
   
   assert pitchtools.NamedPitch(14) in pset
   assert pitchtools.NamedPitch(15) not in pset
