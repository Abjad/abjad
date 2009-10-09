from abjad import *


def test_pitchtools_ChromaticInterval___add___01( ):

   i = pitchtools.ChromaticInterval(3)
   j = pitchtools.ChromaticInterval(14)

   assert i + j == pitchtools.ChromaticInterval(17)
   assert j + i == pitchtools.ChromaticInterval(17)


def test_pitchtools_ChromaticInterval___add___01( ):

   i = pitchtools.ChromaticInterval(3)
   j = pitchtools.ChromaticInterval(14)

   assert i - j == pitchtools.ChromaticInterval(-11)
   assert j - i == pitchtools.ChromaticInterval(11)
