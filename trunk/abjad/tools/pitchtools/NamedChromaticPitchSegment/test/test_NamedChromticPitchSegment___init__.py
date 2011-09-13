from abjad import *


def test_NamedChromticPitchSegment___init___01():
    '''Init named chromatic pitch segment from string.
    '''

    named_chromatic_pitch_segment = pitchtools.NamedChromaticPitchSegment("c'' cs'' d'' ds''")

    assert isinstance(named_chromatic_pitch_segment, pitchtools.NamedChromaticPitchSegment)


def test_NamedChromticPitchSegment___init___02():
    '''Init named chromatic pitch segment from named chromatic pitches.
    '''

    named_chromatic_pitches = []
    named_chromatic_pitches.append(pitchtools.NamedChromaticPitch("c''"))
    named_chromatic_pitches.append(pitchtools.NamedChromaticPitch("cs''"))
    named_chromatic_pitches.append(pitchtools.NamedChromaticPitch("d''"))
    named_chromatic_pitches.append(pitchtools.NamedChromaticPitch("ds''"))
    named_chromatic_pitch_segment = pitchtools.NamedChromaticPitchSegment(named_chromatic_pitches)

    assert isinstance(named_chromatic_pitch_segment, pitchtools.NamedChromaticPitchSegment)
