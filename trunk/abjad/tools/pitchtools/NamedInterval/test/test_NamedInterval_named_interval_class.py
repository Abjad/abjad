# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedInterval_named_interval_class_01():

    diatonic_interval = pitchtools.NamedInterval('perfect', 1)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 1
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('perfect', 1)

    diatonic_interval = pitchtools.NamedInterval('minor', 2)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 2
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('minor', 2)

    diatonic_interval = pitchtools.NamedInterval('major', 2)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 2
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('major', 2)

    diatonic_interval = pitchtools.NamedInterval('minor', 3)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 3
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('minor', 3)

    diatonic_interval = pitchtools.NamedInterval('major', 3)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 3
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('major', 3)


def test_NamedInterval_named_interval_class_02():

    diatonic_interval = pitchtools.NamedInterval('perfect', 8)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 1
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('perfect', 8)

    diatonic_interval = pitchtools.NamedInterval('minor', 9)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 2
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('minor', 2)

    diatonic_interval = pitchtools.NamedInterval('major', 9)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 2
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('major', 2)

    diatonic_interval = pitchtools.NamedInterval('minor', 10)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 3
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('minor', 3)

    diatonic_interval = pitchtools.NamedInterval('major', 10)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == 3
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('major', 3)


def test_NamedInterval_named_interval_class_03():

    diatonic_interval = pitchtools.NamedInterval('perfect', -8)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == -1
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('perfect', -8)

    diatonic_interval = pitchtools.NamedInterval('minor', -9)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == -2
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('minor', -2)

    diatonic_interval = pitchtools.NamedInterval('major', -9)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == -2
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('major', -2)

    diatonic_interval = pitchtools.NamedInterval('minor', -10)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == -3
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('minor', -3)

    diatonic_interval = pitchtools.NamedInterval('major', -10)
    #assert pitchtools.NamedIntervalClass(diatonic_interval) == -3
    ic = pitchtools.NamedIntervalClass(diatonic_interval)
    assert ic == pitchtools.NamedIntervalClass('major', -3)
