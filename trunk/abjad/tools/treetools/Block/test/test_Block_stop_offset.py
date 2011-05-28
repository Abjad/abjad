from abjad.tools.treetools import *
from fractions import Fraction


def test_Block_stop_offset_01( ):
   b = Block(Fraction(-5, 3), 201, 'hello world!')
   assert b.stop_offset == Fraction(598, 3)
