from abjad import *


def test_NamedChromticPitchSegment_transpose_01():
    '''Transpose pitch segment by melodic chromatic interval.'''

    pitch_segment = pitchtools.NamedChromaticPitchSegment([-2, -1, 6, 7, -1, 7])
    mci = pitchtools.MelodicChromaticInterval(-15)
    new_pitch_segment = pitch_segment.transpose(mci)

    "PitchSegment(g,, af,, ef, e, af,, e)"

    assert new_pitch_segment.chromatic_pitch_numbers == [-17, -16, -9, -8, -16, -8]


def test_NamedChromticPitchSegment_transpose_02():
    '''Transpose pitch segment by melodic diatonic interval.'''

    pitch_segment = pitchtools.NamedChromaticPitchSegment([-2, -1, 6, 7, -1, 7])
    mdi = pitchtools.MelodicDiatonicInterval('major', 2)
    new_pitch_segment = pitch_segment.transpose(mdi)

    "PitchSegment(c', cs', gs', a', cs', a')"

    assert new_pitch_segment.chromatic_pitch_numbers == [0, 1, 8, 9, 1, 9]
