from abjad import *
from abjad.tools import durtools


def test_durtools_is_lilypond_duration_string_01( ):

    assert durtools.is_lilypond_duration_string('4..*1/2')
    assert durtools.is_lilypond_duration_string('4.. *1/2')
    assert durtools.is_lilypond_duration_string('4..* 1/2')
    assert durtools.is_lilypond_duration_string('4.. * 1/2')
    assert durtools.is_lilypond_duration_string('4 ..*1/2')
    assert durtools.is_lilypond_duration_string('4 .. *1/2')
    assert durtools.is_lilypond_duration_string('4 .. * 1/2')


def test_durtools_is_lilypond_duration_string_02( ):

    assert durtools.is_lilypond_duration_string('4')
    assert durtools.is_lilypond_duration_string('4..')
    assert durtools.is_lilypond_duration_string('4 * 1/2')
    assert durtools.is_lilypond_duration_string(r'\breve')
    assert durtools.is_lilypond_duration_string(r'\breve..')
    assert durtools.is_lilypond_duration_string(r'\breve * 1/2')


def test_durtools_is_lilypond_duration_string_03( ):

    assert not durtools.is_lilypond_duration_string('foo')
    assert not durtools.is_lilypond_duration_string('')
    assert not durtools.is_lilypond_duration_string(12)

