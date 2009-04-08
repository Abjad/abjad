from abjad import *


def test_mathtools_chop_01( ):
   '''Return the integer part of x.'''

   assert mathtools.chop(0.1) == 0
   assert mathtools.chop(0.9) == 0
   assert mathtools.chop(1.1) == 1
   assert mathtools.chop(1.9) == 1


def test_mathtools_chop_02( ):
   '''Return the integer part of x.'''

   assert mathtools.chop(-0.1) == 0
   assert mathtools.chop(-0.9) == 0
   assert mathtools.chop(-1.1) == -1
   assert mathtools.chop(-1.9) == -1
