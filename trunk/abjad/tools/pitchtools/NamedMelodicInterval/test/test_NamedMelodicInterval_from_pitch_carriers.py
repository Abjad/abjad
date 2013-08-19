# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval_from_pitch_carriers_01():

    pitch = pitchtools.NamedPitch(12)

    interval = pitchtools.NamedMelodicInterval.from_pitch_carriers(
        pitch,
        pitchtools.NamedPitch(12),
        )
    assert interval == pitchtools.NamedMelodicInterval('perfect', 1)

    interval = pitchtools.NamedMelodicInterval.from_pitch_carriers(
        pitch, 
        pitchtools.NamedPitch('b', 4),
        )
    assert interval == pitchtools.NamedMelodicInterval('minor', -2)

    interval = pitchtools.NamedMelodicInterval.from_pitch_carriers(
        pitch, 
        pitchtools.NamedPitch('bf', 4),
        )
    assert interval == pitchtools.NamedMelodicInterval('major', -2)

    interval = pitchtools.NamedMelodicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12),
        pitchtools.NamedPitch('as', 4),
        )
    assert interval == pitchtools.NamedMelodicInterval('diminished', -3)


def test_NamedMelodicInterval_from_pitch_carriers_02():

    pitch = pitchtools.NamedPitch(12)

    interval = pitchtools.NamedMelodicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12),
        pitchtools.NamedPitch('a', 4),
        )
    assert interval == pitchtools.NamedMelodicInterval('minor', -3)

    interval = pitchtools.NamedMelodicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12),
        pitchtools.NamedPitch('af', 4),
        )
    assert interval == pitchtools.NamedMelodicInterval('major', -3)

    interval = pitchtools.NamedMelodicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12),
        pitchtools.NamedPitch('gs', 4),
        )
    assert interval == pitchtools.NamedMelodicInterval('diminished', -4)

    interval = pitchtools.NamedMelodicInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12),
        pitchtools.NamedPitch('g', 4),
        )
    assert interval == pitchtools.NamedMelodicInterval('perfect', -4)
