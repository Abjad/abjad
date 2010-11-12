from fractions import Fraction
from abjad.tools.treetools import *


def test_Block_start_offset( ):
    b = Block(Fraction(-5, 3), 201, 'hello world!')
    assert b.start_offset == Fraction(-5, 3)
