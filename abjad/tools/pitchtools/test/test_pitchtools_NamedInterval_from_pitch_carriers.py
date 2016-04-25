# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval_from_pitch_carriers_01():

    pitch = NamedPitch(12)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        pitch,
        NamedPitch(12),
        )
    assert interval == pitchtools.NamedInterval('perfect', 1)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        pitch,
        NamedPitch('b', 4),
        )
    assert interval == pitchtools.NamedInterval('minor', -2)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        pitch,
        NamedPitch('bf', 4),
        )
    assert interval == pitchtools.NamedInterval('major', -2)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('as', 4),
        )
    assert interval == pitchtools.NamedInterval('diminished', -3)


def test_pitchtools_NamedInterval_from_pitch_carriers_02():

    pitch = NamedPitch(12)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('a', 4),
        )
    assert interval == pitchtools.NamedInterval('minor', -3)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('af', 4),
        )
    assert interval == pitchtools.NamedInterval('major', -3)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('gs', 4),
        )
    assert interval == pitchtools.NamedInterval('diminished', -4)

    interval = pitchtools.NamedInterval.from_pitch_carriers(
        NamedPitch(12),
        NamedPitch('g', 4),
        )
    assert interval == pitchtools.NamedInterval('perfect', -4)
