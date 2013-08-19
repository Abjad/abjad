# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicInterval___add___01():

    i = pitchtools.NumberedMelodicInterval(3)
    j = pitchtools.NumberedMelodicInterval(14)

    assert i + j == pitchtools.NumberedMelodicInterval(17)
    assert j + i == pitchtools.NumberedMelodicInterval(17)


def test_NumberedMelodicInterval___add___02():

    i = pitchtools.NumberedMelodicInterval(3)
    j = pitchtools.NumberedMelodicInterval(14)

    assert i - j == pitchtools.NumberedMelodicInterval(-11)
    assert j - i == pitchtools.NumberedMelodicInterval(11)
