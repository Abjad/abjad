from abjad import *


def test_chop_01( ):
   '''Return the integer part of x.'''

   assert chop(0.1) == 0
   assert chop(0.9) == 0
   assert chop(1.1) == 1
   assert chop(1.9) == 1


def test_chop_02( ):
   '''Return the integer part of x.'''

   assert chop(-0.1) == 0
   assert chop(-0.9) == 0
   assert chop(-1.1) == -1
   assert chop(-1.9) == -1
