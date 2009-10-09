from abjad import *


def test_pitchtools_PC_transpose_01( ):
   
   pc = pitchtools.PC(1)
   assert pc.transpose(0) == pitchtools.PC(1)
   assert pc.transpose(1) == pitchtools.PC(2)
   assert pc.transpose(-1) == pitchtools.PC(0)
   assert pc.transpose(99) == pitchtools.PC(4)
   assert pc.transpose(-99) == pitchtools.PC(10)
