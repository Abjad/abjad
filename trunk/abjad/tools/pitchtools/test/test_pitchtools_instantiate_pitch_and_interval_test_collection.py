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
        pitchtools.MelodicDiatonicInterval('+M2'),
        pitchtools.MelodicDiatonicIntervalClass('+M2'),
        pitchtools.NamedChromaticPitch('c'),
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NumberedChromaticPitch(1),
        pitchtools.NumberedChromaticPitchClass(1),
        ]
