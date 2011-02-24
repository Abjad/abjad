from fractions import Fraction
from abjad.tools.treetools import *


def test_Block_stop_offset_01( ):
   b = Block(Fraction(-5, 3), 201, 'hello world!')
   assert b.stop_offset == Fraction(598, 3)
