# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedPitchClass___add___01():
    r'''Ascending numbered interval added to pitch-class.
    '''

    pc = pitchtools.NumberedPitchClass(0)
    MCI = pitchtools.NumberedInterval

    assert pc + MCI(1) == pitchtools.NumberedPitchClass(1)
    assert pc + MCI(2) == pitchtools.NumberedPitchClass(2)
    assert pc + MCI(3) == pitchtools.NumberedPitchClass(3)
    assert pc + MCI(4) == pitchtools.NumberedPitchClass(4)
    assert pc + MCI(5) == pitchtools.NumberedPitchClass(5)
    assert pc + MCI(6) == pitchtools.NumberedPitchClass(6)
    assert pc + MCI(7) == pitchtools.NumberedPitchClass(7)
    assert pc + MCI(8) == pitchtools.NumberedPitchClass(8)
    assert pc + MCI(9) == pitchtools.NumberedPitchClass(9)
    assert pc + MCI(10) == pitchtools.NumberedPitchClass(10)
    assert pc + MCI(11) == pitchtools.NumberedPitchClass(11)


def test_pitchtools_NumberedPitchClass___add___02():
    r'''Ascending numbered interval added to pitch-class.
    '''

    pc = pitchtools.NumberedPitchClass(0)
    MCI = pitchtools.NumberedInterval

    assert pc + MCI(12) == pitchtools.NumberedPitchClass(0)
    assert pc + MCI(13) == pitchtools.NumberedPitchClass(1)
    assert pc + MCI(14) == pitchtools.NumberedPitchClass(2)
    assert pc + MCI(15) == pitchtools.NumberedPitchClass(3)
    assert pc + MCI(16) == pitchtools.NumberedPitchClass(4)
    assert pc + MCI(17) == pitchtools.NumberedPitchClass(5)
    assert pc + MCI(18) == pitchtools.NumberedPitchClass(6)
    assert pc + MCI(19) == pitchtools.NumberedPitchClass(7)
    assert pc + MCI(20) == pitchtools.NumberedPitchClass(8)
    assert pc + MCI(21) == pitchtools.NumberedPitchClass(9)
    assert pc + MCI(22) == pitchtools.NumberedPitchClass(10)
    assert pc + MCI(23) == pitchtools.NumberedPitchClass(11)


def test_pitchtools_NumberedPitchClass___add___03():
    r'''Descending numbered interval added to pitch-class.
    '''

    pc = pitchtools.NumberedPitchClass(0)
    MCI = pitchtools.NumberedInterval

    assert pc + MCI(-1) == pitchtools.NumberedPitchClass(11)
    assert pc + MCI(-2) == pitchtools.NumberedPitchClass(10)
    assert pc + MCI(-3) == pitchtools.NumberedPitchClass(9)
    assert pc + MCI(-4) == pitchtools.NumberedPitchClass(8)
    assert pc + MCI(-5) == pitchtools.NumberedPitchClass(7)
    assert pc + MCI(-6) == pitchtools.NumberedPitchClass(6)
    assert pc + MCI(-7) == pitchtools.NumberedPitchClass(5)
    assert pc + MCI(-8) == pitchtools.NumberedPitchClass(4)
    assert pc + MCI(-9) == pitchtools.NumberedPitchClass(3)
    assert pc + MCI(-10) == pitchtools.NumberedPitchClass(2)
    assert pc + MCI(-11) == pitchtools.NumberedPitchClass(1)


def test_pitchtools_NumberedPitchClass___add___04():
    r'''Descending numbered interval added to pitch-class.
    '''

    pc = pitchtools.NumberedPitchClass(0)
    MCI = pitchtools.NumberedInterval

    assert pc + MCI(-12) == pitchtools.NumberedPitchClass(0)
    assert pc + MCI(-13) == pitchtools.NumberedPitchClass(11)
    assert pc + MCI(-14) == pitchtools.NumberedPitchClass(10)
    assert pc + MCI(-15) == pitchtools.NumberedPitchClass(9)
    assert pc + MCI(-16) == pitchtools.NumberedPitchClass(8)
    assert pc + MCI(-17) == pitchtools.NumberedPitchClass(7)
    assert pc + MCI(-18) == pitchtools.NumberedPitchClass(6)
    assert pc + MCI(-19) == pitchtools.NumberedPitchClass(5)
    assert pc + MCI(-20) == pitchtools.NumberedPitchClass(4)
    assert pc + MCI(-21) == pitchtools.NumberedPitchClass(3)
    assert pc + MCI(-22) == pitchtools.NumberedPitchClass(2)
    assert pc + MCI(-23) == pitchtools.NumberedPitchClass(1)


def test_pitchtools_NumberedPitchClass___add___05():
    r'''numbered unison added to pitch-class.
    '''

    pc = pitchtools.NumberedPitchClass(0)
    MCI = pitchtools.NumberedInterval

    assert pc + MCI(0) == pitchtools.NumberedPitchClass(0)
