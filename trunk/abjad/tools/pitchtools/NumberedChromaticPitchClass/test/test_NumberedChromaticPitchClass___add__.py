from abjad import *


def test_NumberedChromaticPitchClass___add___01():
    '''Ascending melodic chromatic interval added to pitch-class.'''

    pc = pitchtools.NumberedChromaticPitchClass(0)
    MCI = pitchtools.MelodicChromaticInterval

    assert pc + MCI(1) == pitchtools.NumberedChromaticPitchClass(1)
    assert pc + MCI(2) == pitchtools.NumberedChromaticPitchClass(2)
    assert pc + MCI(3) == pitchtools.NumberedChromaticPitchClass(3)
    assert pc + MCI(4) == pitchtools.NumberedChromaticPitchClass(4)
    assert pc + MCI(5) == pitchtools.NumberedChromaticPitchClass(5)
    assert pc + MCI(6) == pitchtools.NumberedChromaticPitchClass(6)
    assert pc + MCI(7) == pitchtools.NumberedChromaticPitchClass(7)
    assert pc + MCI(8) == pitchtools.NumberedChromaticPitchClass(8)
    assert pc + MCI(9) == pitchtools.NumberedChromaticPitchClass(9)
    assert pc + MCI(10) == pitchtools.NumberedChromaticPitchClass(10)
    assert pc + MCI(11) == pitchtools.NumberedChromaticPitchClass(11)


def test_NumberedChromaticPitchClass___add___02():
    '''Ascending melodic chromatic interval added to pitch-class.'''

    pc = pitchtools.NumberedChromaticPitchClass(0)
    MCI = pitchtools.MelodicChromaticInterval

    assert pc + MCI(12) == pitchtools.NumberedChromaticPitchClass(0)
    assert pc + MCI(13) == pitchtools.NumberedChromaticPitchClass(1)
    assert pc + MCI(14) == pitchtools.NumberedChromaticPitchClass(2)
    assert pc + MCI(15) == pitchtools.NumberedChromaticPitchClass(3)
    assert pc + MCI(16) == pitchtools.NumberedChromaticPitchClass(4)
    assert pc + MCI(17) == pitchtools.NumberedChromaticPitchClass(5)
    assert pc + MCI(18) == pitchtools.NumberedChromaticPitchClass(6)
    assert pc + MCI(19) == pitchtools.NumberedChromaticPitchClass(7)
    assert pc + MCI(20) == pitchtools.NumberedChromaticPitchClass(8)
    assert pc + MCI(21) == pitchtools.NumberedChromaticPitchClass(9)
    assert pc + MCI(22) == pitchtools.NumberedChromaticPitchClass(10)
    assert pc + MCI(23) == pitchtools.NumberedChromaticPitchClass(11)


def test_NumberedChromaticPitchClass___add___03():
    '''Descending melodic chromatic interval added to pitch-class.'''

    pc = pitchtools.NumberedChromaticPitchClass(0)
    MCI = pitchtools.MelodicChromaticInterval

    assert pc + MCI(-1) == pitchtools.NumberedChromaticPitchClass(11)
    assert pc + MCI(-2) == pitchtools.NumberedChromaticPitchClass(10)
    assert pc + MCI(-3) == pitchtools.NumberedChromaticPitchClass(9)
    assert pc + MCI(-4) == pitchtools.NumberedChromaticPitchClass(8)
    assert pc + MCI(-5) == pitchtools.NumberedChromaticPitchClass(7)
    assert pc + MCI(-6) == pitchtools.NumberedChromaticPitchClass(6)
    assert pc + MCI(-7) == pitchtools.NumberedChromaticPitchClass(5)
    assert pc + MCI(-8) == pitchtools.NumberedChromaticPitchClass(4)
    assert pc + MCI(-9) == pitchtools.NumberedChromaticPitchClass(3)
    assert pc + MCI(-10) == pitchtools.NumberedChromaticPitchClass(2)
    assert pc + MCI(-11) == pitchtools.NumberedChromaticPitchClass(1)


def test_NumberedChromaticPitchClass___add___04():
    '''Descending melodic chromatic interval added to pitch-class.'''

    pc = pitchtools.NumberedChromaticPitchClass(0)
    MCI = pitchtools.MelodicChromaticInterval

    assert pc + MCI(-12) == pitchtools.NumberedChromaticPitchClass(0)
    assert pc + MCI(-13) == pitchtools.NumberedChromaticPitchClass(11)
    assert pc + MCI(-14) == pitchtools.NumberedChromaticPitchClass(10)
    assert pc + MCI(-15) == pitchtools.NumberedChromaticPitchClass(9)
    assert pc + MCI(-16) == pitchtools.NumberedChromaticPitchClass(8)
    assert pc + MCI(-17) == pitchtools.NumberedChromaticPitchClass(7)
    assert pc + MCI(-18) == pitchtools.NumberedChromaticPitchClass(6)
    assert pc + MCI(-19) == pitchtools.NumberedChromaticPitchClass(5)
    assert pc + MCI(-20) == pitchtools.NumberedChromaticPitchClass(4)
    assert pc + MCI(-21) == pitchtools.NumberedChromaticPitchClass(3)
    assert pc + MCI(-22) == pitchtools.NumberedChromaticPitchClass(2)
    assert pc + MCI(-23) == pitchtools.NumberedChromaticPitchClass(1)


def test_NumberedChromaticPitchClass___add___05():
    '''Melodic chromatic unison added to pitch-class.'''

    pc = pitchtools.NumberedChromaticPitchClass(0)
    MCI = pitchtools.MelodicChromaticInterval

    assert pc + MCI(0) == pitchtools.NumberedChromaticPitchClass(0)
