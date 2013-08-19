# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval_melodic_diatonic_interval_class_01():

    diatonic_interval = pitchtools.NamedMelodicInterval('perfect', 1)
    #assert diatonic_interval.melodic_diatonic_interval_class == 1
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('perfect', 1)

    diatonic_interval = pitchtools.NamedMelodicInterval('minor', 2)
    #assert diatonic_interval.melodic_diatonic_interval_class == 2
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('minor', 2)

    diatonic_interval = pitchtools.NamedMelodicInterval('major', 2)
    #assert diatonic_interval.melodic_diatonic_interval_class == 2
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('major', 2)

    diatonic_interval = pitchtools.NamedMelodicInterval('minor', 3)
    #assert diatonic_interval.melodic_diatonic_interval_class == 3
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('minor', 3)

    diatonic_interval = pitchtools.NamedMelodicInterval('major', 3)
    #assert diatonic_interval.melodic_diatonic_interval_class == 3
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('major', 3)


def test_NamedMelodicInterval_melodic_diatonic_interval_class_02():

    diatonic_interval = pitchtools.NamedMelodicInterval('perfect', 8)
    #assert diatonic_interval.melodic_diatonic_interval_class == 1
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('perfect', 8)

    diatonic_interval = pitchtools.NamedMelodicInterval('minor', 9)
    #assert diatonic_interval.melodic_diatonic_interval_class == 2
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('minor', 2)

    diatonic_interval = pitchtools.NamedMelodicInterval('major', 9)
    #assert diatonic_interval.melodic_diatonic_interval_class == 2
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('major', 2)

    diatonic_interval = pitchtools.NamedMelodicInterval('minor', 10)
    #assert diatonic_interval.melodic_diatonic_interval_class == 3
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('minor', 3)

    diatonic_interval = pitchtools.NamedMelodicInterval('major', 10)
    #assert diatonic_interval.melodic_diatonic_interval_class == 3
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('major', 3)


def test_NamedMelodicInterval_melodic_diatonic_interval_class_03():

    diatonic_interval = pitchtools.NamedMelodicInterval('perfect', -8)
    #assert diatonic_interval.melodic_diatonic_interval_class == -1
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('perfect', -8)

    diatonic_interval = pitchtools.NamedMelodicInterval('minor', -9)
    #assert diatonic_interval.melodic_diatonic_interval_class == -2
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('minor', -2)

    diatonic_interval = pitchtools.NamedMelodicInterval('major', -9)
    #assert diatonic_interval.melodic_diatonic_interval_class == -2
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('major', -2)

    diatonic_interval = pitchtools.NamedMelodicInterval('minor', -10)
    #assert diatonic_interval.melodic_diatonic_interval_class == -3
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('minor', -3)

    diatonic_interval = pitchtools.NamedMelodicInterval('major', -10)
    #assert diatonic_interval.melodic_diatonic_interval_class == -3
    ic = diatonic_interval.melodic_diatonic_interval_class
    assert ic == pitchtools.NamedMelodicIntervalClass('major', -3)
