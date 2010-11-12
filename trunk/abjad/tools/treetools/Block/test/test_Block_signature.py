from fractions import Fraction
from abjad.tools.treetools import *


def test_Block_signature_01( ):
    block = Block(0, 100, 'hello world!')
    assert block.signature == (0, 100)


def test_Block_signature_02( ):
    block = Block(11, 200, 'hello world!')
    assert block.signature == (11, 211)


def test_Block_signature_03( ):
    block = Block(Fraction(-5, 3), 201, 'hello world')
    assert block.signature == (Fraction(-5, 3), Fraction(598, 3))
