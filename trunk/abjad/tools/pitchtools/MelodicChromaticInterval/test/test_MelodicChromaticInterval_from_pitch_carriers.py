# -*- encoding: utf-8 -*-
from abjad import *


def test_MelodicChromaticInterval_from_pitch_carriers_01():

    pitch_1 = pitchtools.NamedPitch(10)
    pitch_2 = pitchtools.NamedPitch(12)

    mci = pitchtools.MelodicChromaticInterval.from_pitch_carriers(
        pitch_1, pitch_2)
    assert mci == pitchtools.MelodicChromaticInterval(2)

    mci = pitchtools.MelodicChromaticInterval.from_pitch_carriers(
        pitch_2, pitch_1)
    assert mci == pitchtools.MelodicChromaticInterval(-2)

    mci = pitchtools.MelodicChromaticInterval.from_pitch_carriers(
        pitch_1, pitch_1)
    assert mci == pitchtools.MelodicChromaticInterval(0)

    mci = pitchtools.MelodicChromaticInterval.from_pitch_carriers(
        pitch_2, pitch_2)
    assert mci == pitchtools.MelodicChromaticInterval(0)


def test_MelodicChromaticInterval_from_pitch_carriers_02():
    r'''Works with quartertones.
    '''

    mci = pitchtools.MelodicChromaticInterval.from_pitch_carriers(
        pitchtools.NamedPitch(12), pitchtools.NamedPitch(9.5))
    assert mci == pitchtools.MelodicChromaticInterval(-2.5)
