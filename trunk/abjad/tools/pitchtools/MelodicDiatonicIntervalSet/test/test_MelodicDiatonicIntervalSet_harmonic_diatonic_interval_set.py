from abjad import *


def test_MelodicDiatonicIntervalSet_harmonic_diatonic_interval_set_01():

    mdiset = pitchtools.MelodicDiatonicIntervalSet([
        pitchtools.MelodicDiatonicInterval('minor', -2),
        pitchtools.MelodicDiatonicInterval('major', -2),
        pitchtools.MelodicDiatonicInterval('minor', 2),
        pitchtools.MelodicDiatonicInterval('major', 2)])
    "MelodicDiatonicIntervalSet(-m2, -M2, +M2, +m2)"

    derived_hdiset = mdiset.harmonic_diatonic_interval_set
    manual_hdiset = pitchtools.HarmonicDiatonicIntervalSet([
        pitchtools.HarmonicDiatonicInterval('minor', 2),
        pitchtools.HarmonicDiatonicInterval('major', 2)])

    assert derived_hdiset == manual_hdiset
