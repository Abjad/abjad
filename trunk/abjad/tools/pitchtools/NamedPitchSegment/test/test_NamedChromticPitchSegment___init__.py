# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedChromticPitchSegment___init___01():
    r'''Init named chromatic pitch segment from string.
    '''

    named_chromatic_pitch_segment = pitchtools.NamedPitchSegment("c'' cs'' d'' ds''")

    assert isinstance(named_chromatic_pitch_segment, pitchtools.NamedPitchSegment)


def test_NamedChromticPitchSegment___init___02():
    r'''Init named chromatic pitch segment from named chromatic pitches.
    '''

    named_chromatic_pitches = []
    named_chromatic_pitches.append(pitchtools.NamedPitch("c''"))
    named_chromatic_pitches.append(pitchtools.NamedPitch("cs''"))
    named_chromatic_pitches.append(pitchtools.NamedPitch("d''"))
    named_chromatic_pitches.append(pitchtools.NamedPitch("ds''"))
    named_chromatic_pitch_segment = pitchtools.NamedPitchSegment(named_chromatic_pitches)

    assert isinstance(named_chromatic_pitch_segment, pitchtools.NamedPitchSegment)
