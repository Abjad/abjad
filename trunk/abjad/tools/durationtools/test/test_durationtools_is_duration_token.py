from abjad import *
from abjad.tools import durationtools


def test_durationtools_is_duration_token_01():

    assert durationtools.is_duration_token((5, 16))
    assert durationtools.is_duration_token('8..')
    assert durationtools.is_duration_token(Fraction(5, 16))
    assert durationtools.is_duration_token(5)


def test_durationtools_is_duration_token_02():

    assert not durationtools.is_duration_token((5, 6, 7))
    assert not durationtools.is_duration_token('9..')
    assert not durationtools.is_duration_token('foo')
