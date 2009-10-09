from abjad import *


def test_pctheory_PC_invert_01( ):
   
   assert pctheory.PC(0).invert( ) == pctheory.PC(0)
   assert pctheory.PC(1).invert( ) == pctheory.PC(11)
   assert pctheory.PC(2).invert( ) == pctheory.PC(10)
   assert pctheory.PC(3).invert( ) == pctheory.PC(9)
   assert pctheory.PC(4).invert( ) == pctheory.PC(8)
   assert pctheory.PC(5).invert( ) == pctheory.PC(7)
   assert pctheory.PC(6).invert( ) == pctheory.PC(6)
   assert pctheory.PC(7).invert( ) == pctheory.PC(5)
   assert pctheory.PC(8).invert( ) == pctheory.PC(4)
   assert pctheory.PC(9).invert( ) == pctheory.PC(3)
   assert pctheory.PC(10).invert( ) == pctheory.PC(2)
   assert pctheory.PC(11).invert( ) == pctheory.PC(1)
