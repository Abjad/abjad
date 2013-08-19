# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedHarmonicIntervalClass___init___01():

    hcic = pitchtools.NumberedHarmonicIntervalClass(0)
    assert repr(hcic) == 'NumberedHarmonicIntervalClass(0)'
    assert str(hcic) == '0'
    assert hcic.number == 0

    hcic = pitchtools.NumberedHarmonicIntervalClass(12)
    assert hcic.number == 12

    hcic = pitchtools.NumberedHarmonicIntervalClass(24)
    assert hcic.number == 12

    hcic = pitchtools.NumberedHarmonicIntervalClass(-12)
    assert hcic.number == 12

    hcic = pitchtools.NumberedHarmonicIntervalClass(-24)
    assert hcic.number == 12


def test_NumberedHarmonicIntervalClass___init___02():

    hcic = pitchtools.NumberedHarmonicIntervalClass(-25)
    assert hcic.number == 1

    hcic = pitchtools.NumberedHarmonicIntervalClass(-13)
    assert hcic.number == 1

    hcic = pitchtools.NumberedHarmonicIntervalClass(-1)
    assert hcic.number == 1

    hcic = pitchtools.NumberedHarmonicIntervalClass(1)
    assert hcic.number == 1

    hcic = pitchtools.NumberedHarmonicIntervalClass(13)
    assert hcic.number == 1

    hcic = pitchtools.NumberedHarmonicIntervalClass(25)
    assert hcic.number == 1


def test_NumberedHarmonicIntervalClass___init___03():
    r'''Works on harmonic chromatic interval instances.
    '''

    hci = pitchtools.NumberedHarmonicInterval(-14)
    hcic = pitchtools.NumberedHarmonicIntervalClass(hci)
    assert hcic.number == 2

    hci = pitchtools.NumberedHarmonicInterval(14)
    hcic = pitchtools.NumberedHarmonicIntervalClass(hci)
    assert hcic.number == 2
