from abjad import *


def test_DuratedComplexBeamSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = beamtools.DuratedComplexBeamSpanner()
    spanner_2 = beamtools.DuratedComplexBeamSpanner()

    assert not spanner_1 == spanner_2
