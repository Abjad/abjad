from abjad import *


def test_HarmonicChromaticInterval_harmonic_chromatic_interval_class_01():

    assert pitchtools.HarmonicChromaticInterval(2).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.HarmonicChromaticInterval(14).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.HarmonicChromaticInterval(26).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.HarmonicChromaticInterval(38).harmonic_chromatic_interval_class.number == 2


def test_HarmonicChromaticInterval_harmonic_chromatic_interval_class_02():

    assert pitchtools.HarmonicChromaticInterval(-2).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.HarmonicChromaticInterval(-14).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.HarmonicChromaticInterval(-26).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.HarmonicChromaticInterval(-38).harmonic_chromatic_interval_class.number == 2
