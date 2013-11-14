# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSegment___init___01():
    r'''Initializenamed pitch segment from named pitches.
    '''

    named_pitches = []
    named_pitches.append(pitchtools.NamedPitch("c''"))
    named_pitches.append(pitchtools.NamedPitch("cs''"))
    named_pitches.append(pitchtools.NamedPitch("d''"))
    named_pitches.append(pitchtools.NamedPitch("ds''"))
    named_pitch_segment = pitchtools.PitchSegment(
        named_pitches, item_class=pitchtools.NamedPitch)

    assert isinstance(named_pitch_segment, pitchtools.PitchSegment)
