# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicIntervalSet_melodic_chromatic_interval_set_01():

    mdiset = pitchtools.NamedMelodicIntervalSet([
        pitchtools.NamedMelodicInterval('minor', -2),
        pitchtools.NamedMelodicInterval('major', -2),
        pitchtools.NamedMelodicInterval('minor', 2),
        pitchtools.NamedMelodicInterval('major', 2)])
    "NamedMelodicIntervalSet(-m2, -M2, +M2, +m2)"

    derived_mciset = mdiset.melodic_chromatic_interval_set
    manual_mciset = pitchtools.MelodicChromaticIntervalSet([-2, -1, 1, 2])

    assert derived_mciset == manual_mciset
