from abjad import *


def test_pctheory_PC___add__01( ):

   pc1 = pctheory.PC(6)
   pc2 = pctheory.PC(7)

   assert pc1 + pc2 == pctheory.PC(1)
