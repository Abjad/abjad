from abjad import *
from abjad.tools import mathtools


def test_mathtools_sign_01():
    '''Test integer sign.'''

    assert mathtools.sign(-2) == -1
    assert mathtools.sign(-1.5) == -1
    assert mathtools.sign(0) == 0
    assert mathtools.sign(1.5) == 1
    assert mathtools.sign(2) == 1


def test_mathtools_sign_02():
    '''Test rational sign.'''

    assert mathtools.sign(Duration(-3, 2)) == -1
    assert mathtools.sign(Duration(0)) == 0
    assert mathtools.sign(Duration(3, 2)) == 1
