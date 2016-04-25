# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import PitchClassSegment


def test_pitchtools_PitchClassSegment___repr___01():
    r'''Pitch-class segment repr is evaluable.
    '''

    pitch_class_tokens = ['gs', 'a', 'as', 'c', 'cs']
    pitch_class_segment_1 = pitchtools.PitchClassSegment(pitch_class_tokens)
    pitch_class_segment_2 = eval(repr(pitch_class_segment_1))

    assert isinstance(pitch_class_segment_1, pitchtools.PitchClassSegment)
    assert isinstance(pitch_class_segment_2, pitchtools.PitchClassSegment)


def test_pitchtools_PitchClassSegment___repr___02():
    r'''Pitch-class segment repr is evaluable.
    '''

    pitch_class_tokens = [-2, -1.5, 6, 7, -1.5, 7]
    pitch_class_segment_1 = pitchtools.PitchClassSegment(pitch_class_tokens)
    pitch_class_segment_2 = eval(repr(pitch_class_segment_1))

    assert isinstance(pitch_class_segment_1, pitchtools.PitchClassSegment)
    assert isinstance(pitch_class_segment_2, pitchtools.PitchClassSegment)
