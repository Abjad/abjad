from abjad import *


def test_HarmonicDiatonicIntervalSet_harmonic_chromatic_interval_set_01():

    hdiset = pitchtools.HarmonicDiatonicIntervalSet([
        pitchtools.HarmonicDiatonicInterval('minor', 2),
        pitchtools.HarmonicDiatonicInterval('major', 2)])
    "HarmonicDiatonicIntervalSet(m2, M2)"

    derived_hciset = hdiset.harmonic_chromatic_interval_set
    manual_hciset = pitchtools.HarmonicChromaticIntervalSet([1, 2])

    assert derived_hciset == manual_hciset
