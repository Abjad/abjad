from abjad import *
from abjad.tools import durationtools


def test_durationtools_is_lilypond_duration_name_01():

    assert durationtools.is_lilypond_duration_name(r'\breve')
    assert durationtools.is_lilypond_duration_name(r'\longa')
    assert durationtools.is_lilypond_duration_name(r'\maxima')


def test_durationtools_is_lilypond_duration_name_02():

    assert not durationtools.is_lilypond_duration_name('breve')
    assert not durationtools.is_lilypond_duration_name('foo')
    assert not durationtools.is_lilypond_duration_name(12)
