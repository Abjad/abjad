# -*- encoding: utf-8 -*-
from abjad import *


def test_MelodicDiatonicInterval_from_pitch_carriers_01():

    pitch = pitchtools.NamedChromaticPitch(12)

    interval = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
        pitch,
        pitchtools.NamedChromaticPitch(12),
        )
    assert interval == pitchtools.MelodicDiatonicInterval('perfect', 1)

    interval = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
        pitch, 
        pitchtools.NamedChromaticPitch('b', 4),
        )
    assert interval == pitchtools.MelodicDiatonicInterval('minor', -2)

    interval = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
        pitch, 
        pitchtools.NamedChromaticPitch('bf', 4),
        )
    assert interval == pitchtools.MelodicDiatonicInterval('major', -2)

    interval = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12),
        pitchtools.NamedChromaticPitch('as', 4),
        )
    assert interval == pitchtools.MelodicDiatonicInterval('diminished', -3)


def test_MelodicDiatonicInterval_from_pitch_carriers_02():

    pitch = pitchtools.NamedChromaticPitch(12)

    interval = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12),
        pitchtools.NamedChromaticPitch('a', 4),
        )
    assert interval == pitchtools.MelodicDiatonicInterval('minor', -3)

    interval = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12),
        pitchtools.NamedChromaticPitch('af', 4),
        )
    assert interval == pitchtools.MelodicDiatonicInterval('major', -3)

    interval = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12),
        pitchtools.NamedChromaticPitch('gs', 4),
        )
    assert interval == pitchtools.MelodicDiatonicInterval('diminished', -4)

    interval = pitchtools.MelodicDiatonicInterval.from_pitch_carriers(
        pitchtools.NamedChromaticPitch(12),
        pitchtools.NamedChromaticPitch('g', 4),
        )
    assert interval == pitchtools.MelodicDiatonicInterval('perfect', -4)
