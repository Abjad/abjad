from fractions import Fraction
from abjad.tools.treetools import *


def test_Block_duration_01( ):
    b = Block(5, 101, 'hello world!')
    assert b.duration == 101


def test_Block_duration_02( ):
    b = Block(Fraction(-5, 3), Fraction(101, 2), 'hello world!')
    assert b.duration == Fraction(101, 2)
