from abjad import *


def test_MelodicDiatonicIntervalSet_melodic_chromatic_interval_set_01():

    mdiset = pitchtools.MelodicDiatonicIntervalSet([
        pitchtools.MelodicDiatonicInterval('minor', -2),
        pitchtools.MelodicDiatonicInterval('major', -2),
        pitchtools.MelodicDiatonicInterval('minor', 2),
        pitchtools.MelodicDiatonicInterval('major', 2)])
    "MelodicDiatonicIntervalSet(-m2, -M2, +M2, +m2)"

    derived_mciset = mdiset.melodic_chromatic_interval_set
    manual_mciset = pitchtools.MelodicChromaticIntervalSet([-2, -1, 1, 2])

    assert derived_mciset == manual_mciset
