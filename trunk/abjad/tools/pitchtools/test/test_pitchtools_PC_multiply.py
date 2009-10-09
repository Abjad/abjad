from abjad import *


def test_pitchtools_PC_multiply_01( ):

   assert pitchtools.PC(0).multiply(5) == pitchtools.PC(0)
   assert pitchtools.PC(1).multiply(5) == pitchtools.PC(5)
   assert pitchtools.PC(2).multiply(5) == pitchtools.PC(10)
   assert pitchtools.PC(3).multiply(5) == pitchtools.PC(3)
   assert pitchtools.PC(4).multiply(5) == pitchtools.PC(8)
   assert pitchtools.PC(5).multiply(5) == pitchtools.PC(1)
   assert pitchtools.PC(6).multiply(5) == pitchtools.PC(6)
   assert pitchtools.PC(7).multiply(5) == pitchtools.PC(11)
   assert pitchtools.PC(8).multiply(5) == pitchtools.PC(4)
   assert pitchtools.PC(9).multiply(5) == pitchtools.PC(9)
   assert pitchtools.PC(10).multiply(5) == pitchtools.PC(2)
   assert pitchtools.PC(11).multiply(5) == pitchtools.PC(7)
   
