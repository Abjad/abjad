from abjad import *
from abjad.tools import tonalitytools


def test_ExtentIndicator___init___01():
    '''Init from number.'''

    assert tonalitytools.ExtentIndicator(7).number == 7


def test_ExtentIndicator___init___02():
    '''Init by reference.'''

    extent_indicator = tonalitytools.ExtentIndicator(7)
    new = tonalitytools.ExtentIndicator(extent_indicator)

    assert new.number == 7
    assert new == extent_indicator
    assert new is not extent_indicator
