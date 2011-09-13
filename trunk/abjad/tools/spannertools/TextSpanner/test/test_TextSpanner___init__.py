from abjad import *


def test_TextSpanner___init___01():
    '''Init empty text spanner.
    '''

    spanner = spannertools.TextSpanner()
    assert isinstance(spanner, spannertools.TextSpanner)
