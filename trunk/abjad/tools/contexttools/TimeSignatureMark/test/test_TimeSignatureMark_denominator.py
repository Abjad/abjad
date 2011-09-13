from abjad import *


def test_TimeSignatureMark_denominator_01():
    '''Time signature mark denominator is read / write.
    '''

    meter = contexttools.TimeSignatureMark((3, 8))
    assert meter.denominator == 8

    meter.denominator = 16
    assert meter.denominator == 16
