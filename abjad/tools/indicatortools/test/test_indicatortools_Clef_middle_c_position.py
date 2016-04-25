# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Clef_middle_c_position_01():

    assert Clef('treble').middle_c_position == pitchtools.StaffPosition(-6)
    assert Clef('alto').middle_c_position == pitchtools.StaffPosition(0)
    assert Clef('tenor').middle_c_position == pitchtools.StaffPosition(2)
    assert Clef('bass').middle_c_position == pitchtools.StaffPosition(6)
    assert Clef('treble^8').middle_c_position == pitchtools.StaffPosition(-13)
    assert Clef('alto^15').middle_c_position == pitchtools.StaffPosition(-13)
    assert Clef('tenor_8').middle_c_position == pitchtools.StaffPosition(9)
    assert Clef('bass_15').middle_c_position == pitchtools.StaffPosition(19)
