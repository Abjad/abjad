from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitchSegment


def test_NamedChromticPitchSegment___repr___01():
    '''Named chromatic pitch segment repr is evaluable.
    '''

    ncps = ['bf', 'bqf', "fs'", "g'", 'bqf', "g'"]
    named_chromatic_pitch_segment_1 = pitchtools.NamedChromaticPitchSegment(ncps)
    named_chromatic_pitch_segment_2 = eval(repr(named_chromatic_pitch_segment_1))

    '''NamedChromaticPitchSegment("bf bqf fs' g' bqf g'")'''

    assert isinstance(named_chromatic_pitch_segment_1, pitchtools.NamedChromaticPitchSegment)
    assert isinstance(named_chromatic_pitch_segment_2, pitchtools.NamedChromaticPitchSegment)
