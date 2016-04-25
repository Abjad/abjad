# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch___sub___01():

    pitch = NamedPitch(12)
    named_interval = pitchtools.NamedInterval('diminished', 3)

    assert pitch - named_interval == NamedPitch('as', 4)


def test_pitchtools_NamedPitch___sub___02():

    pitch = NamedPitch(12)
    numbered_interval = pitchtools.NumberedInterval(2)

    assert pitch - numbered_interval == NamedPitch('bf', 4)


def test_pitchtools_NamedPitch___sub___03():

    pitch_1 = NamedPitch(12)
    pitch_2 = NamedPitch(10)

    assert pitch_1 - pitch_2 == pitchtools.NamedInterval('major', -2)
    assert pitch_2 - pitch_1 == pitchtools.NamedInterval('major', 2)
