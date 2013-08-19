# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedHarmonicInterval_harmonic_chromatic_interval_class_01():

    assert pitchtools.NumberedHarmonicInterval(2).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.NumberedHarmonicInterval(14).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.NumberedHarmonicInterval(26).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.NumberedHarmonicInterval(38).harmonic_chromatic_interval_class.number == 2


def test_NumberedHarmonicInterval_harmonic_chromatic_interval_class_02():

    assert pitchtools.NumberedHarmonicInterval(-2).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.NumberedHarmonicInterval(-14).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.NumberedHarmonicInterval(-26).harmonic_chromatic_interval_class.number == 2
    assert pitchtools.NumberedHarmonicInterval(-38).harmonic_chromatic_interval_class.number == 2
