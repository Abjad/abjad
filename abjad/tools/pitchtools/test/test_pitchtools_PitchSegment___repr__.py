# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import PitchSegment


def test_pitchtools_PitchSegment___repr___01():
    r'''Named pitch segment repr is evaluable.
    '''

    ncps = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_pitch_segment_1 = pitchtools.PitchSegment(ncps)
    named_pitch_segment_2 = eval(repr(named_pitch_segment_1))

    r'''
    PitchSegment("bf bqf fs' g' bqf g'")
    '''

    assert isinstance(named_pitch_segment_1, pitchtools.PitchSegment)
    assert isinstance(named_pitch_segment_2, pitchtools.PitchSegment)
