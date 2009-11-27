from abjad import *


def test_ChromaticInterval_01( ):

   i = pitchtools.ChromaticInterval(3)

   assert abs(i) == pitchtools.ChromaticInterval(3)
   assert -i == pitchtools.ChromaticInterval(-3)
   assert int(i) == 3
   assert float(i) == 3.0
