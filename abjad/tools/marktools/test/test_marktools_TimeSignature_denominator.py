# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TimeSignature_denominator_01():
    r'''Time signature mark denominator is read / write.
    '''

    time_signature = TimeSignature((3, 8))
    assert time_signature.denominator == 8

    time_signature.denominator = 16
    assert time_signature.denominator == 16
