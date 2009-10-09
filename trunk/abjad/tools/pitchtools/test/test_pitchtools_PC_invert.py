from abjad import *


def test_pitchtools_PC_invert_01( ):
   
   assert pitchtools.PC(0).invert( ) == pitchtools.PC(0)
   assert pitchtools.PC(1).invert( ) == pitchtools.PC(11)
   assert pitchtools.PC(2).invert( ) == pitchtools.PC(10)
   assert pitchtools.PC(3).invert( ) == pitchtools.PC(9)
   assert pitchtools.PC(4).invert( ) == pitchtools.PC(8)
   assert pitchtools.PC(5).invert( ) == pitchtools.PC(7)
   assert pitchtools.PC(6).invert( ) == pitchtools.PC(6)
   assert pitchtools.PC(7).invert( ) == pitchtools.PC(5)
   assert pitchtools.PC(8).invert( ) == pitchtools.PC(4)
   assert pitchtools.PC(9).invert( ) == pitchtools.PC(3)
   assert pitchtools.PC(10).invert( ) == pitchtools.PC(2)
   assert pitchtools.PC(11).invert( ) == pitchtools.PC(1)
