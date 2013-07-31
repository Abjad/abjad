# -*- encoding: utf-8 -*-
from abjad import *


def test_TimeSignatureMark_denominator_01():
    r'''Time signature mark denominator is read / write.
    '''

    time_signature = contexttools.TimeSignatureMark((3, 8))
    assert time_signature.denominator == 8

    time_signature.denominator = 16
    assert time_signature.denominator == 16
