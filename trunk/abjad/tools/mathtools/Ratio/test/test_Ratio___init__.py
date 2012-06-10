from abjad.tools import *
import py


def test_Ratio___init___01():

    ratio = mathtools.Ratio(1, 2, 1)

    assert isinstance(ratio, mathtools.Ratio)


def test_Ratio___init___02():

    assert py.test.raises(Exception, 'mathtools.Ratio(1, 2, 0)')    
