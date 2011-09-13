from abjad import *


def test_MelodicChromaticInterval_chromatic_interval_number_01():

    assert pitchtools.MelodicChromaticInterval(-14).chromatic_interval_number == -14
    assert pitchtools.MelodicChromaticInterval(14).chromatic_interval_number == 14
    assert pitchtools.MelodicChromaticInterval(-2).chromatic_interval_number == -2
    assert pitchtools.MelodicChromaticInterval(2).chromatic_interval_number == 2
