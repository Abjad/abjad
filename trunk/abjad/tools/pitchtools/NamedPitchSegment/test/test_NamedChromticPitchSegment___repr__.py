# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NamedPitchSegment


def test_NamedChromticPitchSegment___repr___01():
    r'''Named chromatic pitch segment repr is evaluable.
    '''

    ncps = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_chromatic_pitch_segment_1 = pitchtools.NamedPitchSegment(ncps)
    named_chromatic_pitch_segment_2 = eval(repr(named_chromatic_pitch_segment_1))

    r'''NamedPitchSegment("bf bqf fs' g' bqf g'")
    '''

    assert isinstance(named_chromatic_pitch_segment_1, pitchtools.NamedPitchSegment)
    assert isinstance(named_chromatic_pitch_segment_2, pitchtools.NamedPitchSegment)
