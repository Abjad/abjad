# -*- encoding: utf-8 -*-
from abjad.tools import *
import py


def test_mathtools_Ratio___init___01():
    r'''Init from integers.
    '''

    ratio = mathtools.Ratio(1, 2, 1)
    assert isinstance(ratio, mathtools.Ratio)


def test_mathtools_Ratio___init___02():
    r'''Init from a tuple or list.
    '''

    ratio = mathtools.Ratio((1, 2, 1))
    assert isinstance(ratio, mathtools.Ratio)


def test_mathtools_Ratio___init___03():

    assert py.test.raises(Exception, 'mathtools.Ratio(1, 2, 0)')
