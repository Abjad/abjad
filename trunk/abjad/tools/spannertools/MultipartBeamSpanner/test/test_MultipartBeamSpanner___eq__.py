from abjad import *


def test_MultipartBeamSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.MultipartBeamSpanner()
    spanner_2 = spannertools.MultipartBeamSpanner()

    assert not spanner_1 == spanner_2
