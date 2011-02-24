from abjad.tools.treetools import *
from fractions import Fraction


def test_Block_start_offset_01( ):
   b = Block(Fraction(-5, 3), 201, 'hello world!')
   assert b.start_offset == Fraction(-5, 3)
