from abjad import *
from abjad.tools import durationtools


def test_durationtools_is_lilypond_duration_string_01():

    assert durationtools.is_lilypond_duration_string('4..*1/2')
    assert durationtools.is_lilypond_duration_string('4.. *1/2')
    assert durationtools.is_lilypond_duration_string('4..* 1/2')
    assert durationtools.is_lilypond_duration_string('4.. * 1/2')
    assert durationtools.is_lilypond_duration_string('4 ..*1/2')
    assert durationtools.is_lilypond_duration_string('4 .. *1/2')
    assert durationtools.is_lilypond_duration_string('4 .. * 1/2')


def test_durationtools_is_lilypond_duration_string_02():

    assert durationtools.is_lilypond_duration_string('4')
    assert durationtools.is_lilypond_duration_string('4..')
    assert durationtools.is_lilypond_duration_string('4 * 1/2')
    assert durationtools.is_lilypond_duration_string(r'\breve')
    assert durationtools.is_lilypond_duration_string(r'\breve..')
    assert durationtools.is_lilypond_duration_string(r'\breve * 1/2')


def test_durationtools_is_lilypond_duration_string_03():

    assert not durationtools.is_lilypond_duration_string('foo')
    assert not durationtools.is_lilypond_duration_string('')
    assert not durationtools.is_lilypond_duration_string(12)
