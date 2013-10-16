# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch___sub___01():

    pitch = pitchtools.NamedPitch(12)
    diatonic_interval = pitchtools.NamedInterval('diminished', 3)

    assert pitch - diatonic_interval == pitchtools.NamedPitch('as', 4)


def test_NamedPitch___sub___02():

    pitch = pitchtools.NamedPitch(12)
    numbered_interval = pitchtools.NumberedInterval(2)

    assert pitch - numbered_interval == pitchtools.NamedPitch('bf', 4)


def test_NamedPitch___sub___03():

    pitch_1 = pitchtools.NamedPitch(12)
    pitch_2 = pitchtools.NamedPitch(10)

    assert pitch_1 - pitch_2 == pitchtools.NamedInterval('major', -2)
    assert pitch_2 - pitch_1 == pitchtools.NamedInterval('major', 2)
