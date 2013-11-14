# -*- encoding: utf-8 -*-
from abjad.tools import *
import pytest


def test_mathtools_Ratio___init___01():
    r'''Initialize from integers.
    '''

    ratio = mathtools.Ratio(1, 2, 1)
    assert isinstance(ratio, mathtools.Ratio)


def test_mathtools_Ratio___init___02():
    r'''Initialize from a tuple or list.
    '''

    ratio = mathtools.Ratio((1, 2, 1))
    assert isinstance(ratio, mathtools.Ratio)


def test_mathtools_Ratio___init___03():

    assert pytest.raises(Exception, 'mathtools.Ratio(1, 2, 0)')
