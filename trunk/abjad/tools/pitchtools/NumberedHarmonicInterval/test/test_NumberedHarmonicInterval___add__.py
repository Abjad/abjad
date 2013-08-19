# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedHarmonicInterval___add___01():

    i = pitchtools.NumberedHarmonicInterval(3)
    j = pitchtools.NumberedHarmonicInterval(14)

    assert i + j == pitchtools.NumberedHarmonicInterval(17)
    assert j + i == pitchtools.NumberedHarmonicInterval(17)


def test_NumberedHarmonicInterval___add___02():

    i = pitchtools.NumberedHarmonicInterval(3)
    j = pitchtools.NumberedHarmonicInterval(14)

    assert i - j == pitchtools.NumberedHarmonicInterval(11)
    assert j - i == pitchtools.NumberedHarmonicInterval(11)
