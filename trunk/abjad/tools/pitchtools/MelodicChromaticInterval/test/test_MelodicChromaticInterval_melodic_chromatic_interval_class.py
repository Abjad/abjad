from abjad import *


def testMelodicObjectChromaticInterval_melodic_chromatic_interval_class_01():

    assert pitchtools.MelodicChromaticInterval(2).melodic_chromatic_interval_class.number == 2
    assert pitchtools.MelodicChromaticInterval(14).melodic_chromatic_interval_class.number == 2
    assert pitchtools.MelodicChromaticInterval(26).melodic_chromatic_interval_class.number == 2
    assert pitchtools.MelodicChromaticInterval(38).melodic_chromatic_interval_class.number == 2


def testMelodicObjectChromaticInterval_melodic_chromatic_interval_class_02():

    assert pitchtools.MelodicChromaticInterval(-2).melodic_chromatic_interval_class.number == -2
    assert pitchtools.MelodicChromaticInterval(-14).melodic_chromatic_interval_class.number == -2
    assert pitchtools.MelodicChromaticInterval(-26).melodic_chromatic_interval_class.number == -2
    assert pitchtools.MelodicChromaticInterval(-38).melodic_chromatic_interval_class.number == -2
