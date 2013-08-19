# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NumberedHarmonicInterval_01():

    i = pitchtools.NumberedHarmonicInterval(3)

    assert abs(i) == pitchtools.NumberedHarmonicInterval(3)
    assert int(i) == 3
    assert float(i) == 3.0

    assert py.test.raises(TypeError, '-i')
