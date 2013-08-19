# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_instantiate_pitch_and_interval_test_collection_01():

    result = pitchtools.instantiate_pitch_and_interval_test_collection()

    assert result == [
        pitchtools.NumberedHarmonicInterval(1),
        pitchtools.NumberedHarmonicIntervalClass(1),
        pitchtools.NamedHarmonicInterval('M2'),
        pitchtools.NamedHarmonicIntervalClass('M2'),
        pitchtools.NumberedInversionEquivalentIntervalClass(1),
        pitchtools.NamedInversionEquivalentIntervalClass('M2'),
        pitchtools.NumberedMelodicInterval(+1),
        pitchtools.NumberedMelodicIntervalClass(+1),
        pitchtools.NamedMelodicInterval('+M2'),
        pitchtools.NamedMelodicIntervalClass('+M2'),
        pitchtools.NamedPitch('c'),
        pitchtools.NamedPitchClass('c'),
        pitchtools.NumberedPitch(1),
        pitchtools.NumberedPitchClass(1),
        ]
