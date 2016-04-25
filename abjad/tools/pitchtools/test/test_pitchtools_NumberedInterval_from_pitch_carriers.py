# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInterval_from_pitch_carriers_01():

    pitch_1 = NamedPitch(10)
    pitch_2 = NamedPitch(12)

    mci = pitchtools.NumberedInterval.from_pitch_carriers(
        pitch_1, pitch_2)
    assert mci == pitchtools.NumberedInterval(2)

    mci = pitchtools.NumberedInterval.from_pitch_carriers(
        pitch_2, pitch_1)
    assert mci == pitchtools.NumberedInterval(-2)

    mci = pitchtools.NumberedInterval.from_pitch_carriers(
        pitch_1, pitch_1)
    assert mci == pitchtools.NumberedInterval(0)

    mci = pitchtools.NumberedInterval.from_pitch_carriers(
        pitch_2, pitch_2)
    assert mci == pitchtools.NumberedInterval(0)


def test_pitchtools_NumberedInterval_from_pitch_carriers_02():
    r'''Works with quartertones.
    '''

    mci = pitchtools.NumberedInterval.from_pitch_carriers(
        NamedPitch(12), NamedPitch(9.5))
    assert mci == pitchtools.NumberedInterval(-2.5)
