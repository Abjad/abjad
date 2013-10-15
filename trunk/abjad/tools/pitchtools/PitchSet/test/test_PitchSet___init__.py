# -*- encoding: utf-8 -*-
from abjad import *


def test_PitchSet___init___01():
    r'''Works with numbers.
    '''

    assert len(pitchtools.PitchSet([12, 14, 18, 19])) == 4


def test_PitchSet___init___02():
    r'''Works with pitches.
    '''

    assert len(pitchtools.PitchSet([pitchtools.NamedPitch(x) 
        for x in [12, 14, 18, 19]])) == 4
