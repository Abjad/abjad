# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicIntervalSet_harmonic_chromatic_interval_set_01():

    mdiset = pitchtools.NamedMelodicIntervalSet([
        pitchtools.NamedMelodicInterval('minor', -2),
        pitchtools.NamedMelodicInterval('major', -2),
        pitchtools.NamedMelodicInterval('minor', 2),
        pitchtools.NamedMelodicInterval('major', 2)])
    "NamedMelodicIntervalSet(-m2, -M2, +M2, +m2)"

    derived_hciset = mdiset.harmonic_chromatic_interval_set
    manual_hciset = pitchtools.NumberedHarmonicIntervalSet([1, 2])

    assert derived_hciset == manual_hciset
