from abjad import *


def test_TrillSpanner___init___01():
    '''Init empty trill spanner.
    '''

    trill = spannertools.TrillSpanner()
    assert isinstance(trill, spannertools.TrillSpanner)
