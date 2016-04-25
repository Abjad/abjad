# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval___add___01():

    i = pitchtools.NumberedInterval(3)
    j = pitchtools.NumberedInterval(14)

    assert i + j == pitchtools.NumberedInterval(17)
    assert j + i == pitchtools.NumberedInterval(17)


def test_pitchtools_NumberedInterval___add___02():

    i = pitchtools.NumberedInterval(3)
    j = pitchtools.NumberedInterval(14)

    assert i - j == pitchtools.NumberedInterval(-11)
    assert j - i == pitchtools.NumberedInterval(11)
