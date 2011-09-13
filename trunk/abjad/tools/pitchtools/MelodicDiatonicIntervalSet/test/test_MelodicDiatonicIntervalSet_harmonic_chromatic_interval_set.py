from abjad import *


def test_MelodicDiatonicIntervalSet_harmonic_chromatic_interval_set_01():

    mdiset = pitchtools.MelodicDiatonicIntervalSet([
        pitchtools.MelodicDiatonicInterval('minor', -2),
        pitchtools.MelodicDiatonicInterval('major', -2),
        pitchtools.MelodicDiatonicInterval('minor', 2),
        pitchtools.MelodicDiatonicInterval('major', 2)])
    "MelodicDiatonicIntervalSet(-m2, -M2, +M2, +m2)"

    derived_hciset = mdiset.harmonic_chromatic_interval_set
    manual_hciset = pitchtools.HarmonicChromaticIntervalSet([1, 2])

    assert derived_hciset == manual_hciset
