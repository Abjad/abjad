from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_is_unlikely_melodic_diatonic_interval_in_chorale_01():

    mdi = pitchtools.MelodicDiatonicInterval('major', 6)
    result = tonalanalysistools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
    assert result

    mdi = pitchtools.MelodicDiatonicInterval('major', 7)
    result = tonalanalysistools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
    assert result

    mdi = pitchtools.MelodicDiatonicInterval('major', 9)
    result = tonalanalysistools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
    assert result


def test_tonalanalysistools_is_unlikely_melodic_diatonic_interval_in_chorale_02():

    mdi = pitchtools.MelodicDiatonicInterval('perfect', 1)
    result = tonalanalysistools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
    assert result == False

    mdi = pitchtools.MelodicDiatonicInterval('major', 2)
    result = tonalanalysistools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
    assert result == False

    mdi = pitchtools.MelodicDiatonicInterval('major', 3)
    result = tonalanalysistools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
    assert result == False

    mdi = pitchtools.MelodicDiatonicInterval('perfect', 4)
    result = tonalanalysistools.is_unlikely_melodic_diatonic_interval_in_chorale(mdi)
    assert result == False
