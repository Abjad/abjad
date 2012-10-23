from abjad import *


def test_durationtools_Duration_lilypond_duration_string_01():

    assert durationtools.Duration((1, 16)).lilypond_duration_string == '16'
    assert durationtools.Duration((2, 16)).lilypond_duration_string == '8'
    assert durationtools.Duration((3, 16)).lilypond_duration_string == '8.'
    assert durationtools.Duration((4, 16)).lilypond_duration_string == '4'
