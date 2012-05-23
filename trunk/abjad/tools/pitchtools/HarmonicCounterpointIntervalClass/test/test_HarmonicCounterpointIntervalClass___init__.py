from abjad import *


def test_HarmonicCounterpointIntervalClass___init___01():
    '''Works with numbers from 1 - 8.'''

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(1)
    assert hcpic.number == 1

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(2)
    assert hcpic.number == 2

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(3)
    assert hcpic.number == 3

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(4)
    assert hcpic.number == 4

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(5)
    assert hcpic.number == 5

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(6)
    assert hcpic.number == 6

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(7)
    assert hcpic.number == 7

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(8)
    assert hcpic.number == 8


def test_HarmonicCounterpointIntervalClass___init___02():
    '''Works with numbers greater than 8.'''

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(9)
    assert hcpic.number == 2

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(10)
    assert hcpic.number == 3

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(11)
    assert hcpic.number == 4

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(12)
    assert hcpic.number == 5

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(13)
    assert hcpic.number == 6

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(14)
    assert hcpic.number == 7

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(15)
    assert hcpic.number == 8


def test_HarmonicCounterpointIntervalClass___init___03():
    '''Works with numbers from -1 to -8.'''

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-1)
    assert hcpic.number == 1

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-2)
    assert hcpic.number == 2

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-3)
    assert hcpic.number == 3

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-4)
    assert hcpic.number == 4

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-5)
    assert hcpic.number == 5

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-6)
    assert hcpic.number == 6

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-7)
    assert hcpic.number == 7

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-8)
    assert hcpic.number == 8


def test_HarmonicCounterpointIntervalClass___init___04():
    '''Works with less than -8.'''

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-9)
    assert hcpic.number == 2

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-10)
    assert hcpic.number == 3

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-11)
    assert hcpic.number == 4

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-12)
    assert hcpic.number == 5

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-13)
    assert hcpic.number == 6

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-14)
    assert hcpic.number == 7

    hcpic = pitchtools.HarmonicCounterpointIntervalClass(-15)
    assert hcpic.number == 8
