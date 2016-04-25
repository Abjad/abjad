# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_instantiate_pitch_and_interval_test_collection_01():

    result = pitchtools.instantiate_pitch_and_interval_test_collection()

    assert result == [
        pitchtools.NumberedInversionEquivalentIntervalClass(1),
        pitchtools.NamedInversionEquivalentIntervalClass('M2'),
        pitchtools.NumberedInterval(+1),
        pitchtools.NumberedIntervalClass(+1),
        pitchtools.NamedInterval('+M2'),
        pitchtools.NamedIntervalClass('+M2'),
        pitchtools.NamedPitch('c'),
        pitchtools.NamedPitchClass('c'),
        pitchtools.NumberedPitch(1),
        pitchtools.NumberedPitchClass(1),
        ]
