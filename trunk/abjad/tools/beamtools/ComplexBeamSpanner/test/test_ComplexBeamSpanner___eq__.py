from abjad import *


def test_ComplexBeamSpanner___eq___01():
    '''Spanner is strict comparator.
    '''

    spanner_1 = beamtools.ComplexBeamSpanner()
    spanner_2 = beamtools.ComplexBeamSpanner()

    assert not spanner_1 == spanner_2
