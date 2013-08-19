# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NumberedPitchClass___sub___01():
    r'''Subtracting one pitch-class from another.
    '''

    pc1 = pitchtools.NumberedPitchClass(6)
    pc2 = pitchtools.NumberedPitchClass(7)

    assert pc1 - pc2 == pitchtools.InversionEquivalentChromaticIntervalClass(1)
    assert pc2 - pc1 == pitchtools.InversionEquivalentChromaticIntervalClass(1)


def test_NumberedPitchClass___sub___02():
    r'''Subtracting an interval-class from a pitch-class.
    '''

    pc = pitchtools.NumberedPitchClass(0)
    ic = pitchtools.InversionEquivalentChromaticIntervalClass(2)

    assert pc - ic == pitchtools.NumberedPitchClass(10)
    assert py.test.raises(TypeError, 'ic - pc')
