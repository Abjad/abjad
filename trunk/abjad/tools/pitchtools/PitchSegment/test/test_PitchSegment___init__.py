# -*- encoding: utf-8 -*-
from abjad import *


def test_PitchSegment___init___02():
    r'''Init named chromatic pitch segment from named chromatic pitches.
    '''

    named_pitches = []
    named_pitches.append(pitchtools.NamedPitch("c''"))
    named_pitches.append(pitchtools.NamedPitch("cs''"))
    named_pitches.append(pitchtools.NamedPitch("d''"))
    named_pitches.append(pitchtools.NamedPitch("ds''"))
    named_pitch_segment = pitchtools.PitchSegment(
        named_pitches, item_class=pitchtools.NamedPitch)

    assert isinstance(named_pitch_segment, pitchtools.PitchSegment)
