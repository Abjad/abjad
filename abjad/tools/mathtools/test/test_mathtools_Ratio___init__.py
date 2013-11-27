# -*- encoding: utf-8 -*-
import pytest
from abjad.tools import *


def test_mathtools_Ratio___init___01():
    r'''Initializes ratio from empty input.
    '''

    ratio = mathtools.Ratio()
    
    assert ratio == mathtools.Ratio(1, 1)


def test_mathtools_Ratio___init___02():
    r'''Initialize from integers.
    '''

    ratio = mathtools.Ratio(1, 2, 1)

    assert isinstance(ratio, mathtools.Ratio)


def test_mathtools_Ratio___init___03():
    r'''Initialize from a tuple or list.
    '''

    ratio = mathtools.Ratio((1, 2, 1))

    assert isinstance(ratio, mathtools.Ratio)


def test_mathtools_Ratio___init___04():

    assert pytest.raises(Exception, 'mathtools.Ratio(1, 2, 0)')
