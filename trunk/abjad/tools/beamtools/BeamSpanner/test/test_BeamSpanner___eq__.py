from abjad import *


def test_BeamSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = beamtools.BeamSpanner()
    spanner_2 = beamtools.BeamSpanner()

    assert not spanner_1 == spanner_2
