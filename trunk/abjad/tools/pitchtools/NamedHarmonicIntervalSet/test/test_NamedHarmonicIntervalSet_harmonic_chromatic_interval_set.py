# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicIntervalSet_harmonic_chromatic_interval_set_01():

    hdiset = pitchtools.NamedHarmonicIntervalSet([
        pitchtools.NamedHarmonicInterval('minor', 2),
        pitchtools.NamedHarmonicInterval('major', 2)])
    "NamedHarmonicIntervalSet(m2, M2)"

    derived_hciset = hdiset.harmonic_chromatic_interval_set
    manual_hciset = pitchtools.NumberedHarmonicIntervalSet([1, 2])

    assert derived_hciset == manual_hciset
