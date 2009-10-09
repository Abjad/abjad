from abjad import *


def test_pctheory_PC_multiply_01( ):

   assert pctheory.PC(0).multiply(5) == pctheory.PC(0)
   assert pctheory.PC(1).multiply(5) == pctheory.PC(5)
   assert pctheory.PC(2).multiply(5) == pctheory.PC(10)
   assert pctheory.PC(3).multiply(5) == pctheory.PC(3)
   assert pctheory.PC(4).multiply(5) == pctheory.PC(8)
   assert pctheory.PC(5).multiply(5) == pctheory.PC(1)
   assert pctheory.PC(6).multiply(5) == pctheory.PC(6)
   assert pctheory.PC(7).multiply(5) == pctheory.PC(11)
   assert pctheory.PC(8).multiply(5) == pctheory.PC(4)
   assert pctheory.PC(9).multiply(5) == pctheory.PC(9)
   assert pctheory.PC(10).multiply(5) == pctheory.PC(2)
   assert pctheory.PC(11).multiply(5) == pctheory.PC(7)
   
