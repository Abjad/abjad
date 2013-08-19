# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_instantiate_pitch_and_interval_test_collection_01():

    result = pitchtools.instantiate_pitch_and_interval_test_collection()

    assert result == [
        pitchtools.HarmonicChromaticInterval(1),
        pitchtools.HarmonicChromaticIntervalClass(1),
        pitchtools.HarmonicDiatonicInterval('M2'),
        pitchtools.HarmonicDiatonicIntervalClass('M2'),
        pitchtools.InversionEquivalentChromaticIntervalClass(1),
        pitchtools.InversionEquivalentDiatonicIntervalClass('M2'),
        pitchtools.MelodicChromaticInterval(+1),
        pitchtools.MelodicChromaticIntervalClass(+1),
        pitchtools.NamedMelodicInterval('+M2'),
        pitchtools.NamedMelodicIntervalClass('+M2'),
        pitchtools.NamedPitch('c'),
        pitchtools.NamedPitchClass('c'),
        pitchtools.NumberedPitch(1),
        pitchtools.NumberedPitchClass(1),
        ]
