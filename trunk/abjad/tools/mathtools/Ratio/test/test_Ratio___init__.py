from abjad.tools import *
import py


def test_Ratio___init___01():
    '''Init from integers.
    '''

    ratio = mathtools.Ratio(1, 2, 1)
    assert isinstance(ratio, mathtools.Ratio)


def test_Ratio___init___02():
    '''Init from a tuple or list.
    '''

    ratio = mathtools.Ratio((1, 2, 1))
    assert isinstance(ratio, mathtools.Ratio)


def test_Ratio___init___03():

    assert py.test.raises(Exception, 'mathtools.Ratio(1, 2, 0)')    
