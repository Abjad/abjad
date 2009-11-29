from abjad import *
import py.test
py.test.skip( )


def test_ChromaticInterval_interval_class_01( ):

   assert pitchtools.ChromaticInterval(2).interval_class == 2
   assert pitchtools.ChromaticInterval(14).interval_class == 2
   assert pitchtools.ChromaticInterval(26).interval_class == 2
   assert pitchtools.ChromaticInterval(38).interval_class == 2


def test_ChromaticInterval_interval_class_02( ):

   assert pitchtools.ChromaticInterval(-2).interval_class == -2
   assert pitchtools.ChromaticInterval(-14).interval_class == -2
   assert pitchtools.ChromaticInterval(-26).interval_class == -2
   assert pitchtools.ChromaticInterval(-38).interval_class == -2
