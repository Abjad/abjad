from abjad import *


def test_MultipartBeamSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = beamtools.MultipartBeamSpanner()
    spanner_2 = beamtools.MultipartBeamSpanner()

    assert not spanner_1 == spanner_2
