from abjad import *


def test_pctheory_PC_transpose_01( ):
   
   pc = pctheory.PC(1)
   assert pc.transpose(0) == pctheory.PC(1)
   assert pc.transpose(1) == pctheory.PC(2)
   assert pc.transpose(-1) == pctheory.PC(0)
   assert pc.transpose(99) == pctheory.PC(4)
   assert pc.transpose(-99) == pctheory.PC(10)
