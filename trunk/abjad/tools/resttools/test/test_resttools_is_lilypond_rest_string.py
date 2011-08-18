from abjad import *


def test_resttools_is_lilypond_rest_string_01():

    assert resttools.is_lilypond_rest_string('r4..*1/2')
    assert resttools.is_lilypond_rest_string('r4.. *1/2')
    assert resttools.is_lilypond_rest_string('r4..* 1/2')
    assert resttools.is_lilypond_rest_string('r4.. * 1/2')
    assert resttools.is_lilypond_rest_string('r4 ..*1/2')
    assert resttools.is_lilypond_rest_string('r4 .. *1/2')
    assert resttools.is_lilypond_rest_string('r4 .. * 1/2')


def test_resttools_is_lilypond_rest_string_02():

    assert resttools.is_lilypond_rest_string('r4')
    assert resttools.is_lilypond_rest_string('r4..')
    assert resttools.is_lilypond_rest_string('r4 * 1/2')
    assert resttools.is_lilypond_rest_string(r'r\breve')
    assert resttools.is_lilypond_rest_string(r'r\breve..')
    assert resttools.is_lilypond_rest_string(r'r\breve * 1/2')


def test_resttools_is_lilypond_rest_string_03():

    assert not resttools.is_lilypond_rest_string('foo')
    assert not resttools.is_lilypond_rest_string('')
    assert not resttools.is_lilypond_rest_string(12)
