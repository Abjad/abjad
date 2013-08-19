# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicIntervalSet_harmonic_diatonic_interval_set_01():

    mdiset = pitchtools.NamedMelodicIntervalSet([
        pitchtools.NamedMelodicInterval('minor', -2),
        pitchtools.NamedMelodicInterval('major', -2),
        pitchtools.NamedMelodicInterval('minor', 2),
        pitchtools.NamedMelodicInterval('major', 2)])
    "NamedMelodicIntervalSet(-m2, -M2, +M2, +m2)"

    derived_hdiset = mdiset.harmonic_diatonic_interval_set
    manual_hdiset = pitchtools.HarmonicDiatonicIntervalSet([
        pitchtools.HarmonicDiatonicInterval('minor', 2),
        pitchtools.HarmonicDiatonicInterval('major', 2)])

    assert derived_hdiset == manual_hdiset
