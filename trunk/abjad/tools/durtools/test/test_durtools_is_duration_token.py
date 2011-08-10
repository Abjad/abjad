from abjad import *
from abjad.tools import durtools


def test_durtools_is_duration_token_01( ):

    assert durtools.is_duration_token((5, 16))
    assert durtools.is_duration_token('8..')
    assert durtools.is_duration_token(Fraction(5, 16))
    assert durtools.is_duration_token(5)


def test_durtools_is_duration_token_02( ):

    assert not durtools.is_duration_token((5, 6, 7))
    assert not durtools.is_duration_token('9..')
    assert not durtools.is_duration_token('foo')
