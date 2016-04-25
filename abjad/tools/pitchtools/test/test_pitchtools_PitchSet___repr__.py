# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import PitchSet


def test_pitchtools_PitchSet___repr___01():
    r'''Pitch set repr is evaluable.
    '''

    pitch_classes =['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    pitch_set_1 = pitchtools.PitchSet(pitch_classes)
    pitch_set_2 = eval(repr(pitch_set_1))

    assert isinstance(pitch_set_1, pitchtools.PitchSet)
    assert isinstance(pitch_set_2, pitchtools.PitchSet)
