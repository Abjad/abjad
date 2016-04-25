# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSegment___init___01():
    r'''Initialize named pitch segment from named pitches.
    '''

    named_pitches = []
    named_pitches.append(NamedPitch("c''"))
    named_pitches.append(NamedPitch("cs''"))
    named_pitches.append(NamedPitch("d''"))
    named_pitches.append(NamedPitch("ds''"))
    named_pitch_segment = pitchtools.PitchSegment(
        named_pitches, item_class=NamedPitch)

    assert isinstance(named_pitch_segment, pitchtools.PitchSegment)
