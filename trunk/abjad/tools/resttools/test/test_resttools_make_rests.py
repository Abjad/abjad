from abjad import *


def test_resttools_make_rests_01():
    '''
    resttools.make_rests can take a single 2-tuple as duration token.
    '''
    t = resttools.make_rests((1,4))
    assert isinstance(t, list)
    assert len(t) == 1
    assert isinstance(t[0], Rest)
    assert t[0].written_duration == Duration(1, 4)
    assert not tietools.is_component_with_tie_spanner_attached(t[0])


def test_resttools_make_rests_02():
    '''Tied durations result in more than one tied Rest.
    However, rests are not tied by default.'''
    t = resttools.make_rests((5, 8))
    assert len(t) == 2
    assert isinstance(t[0], Rest)
    assert isinstance(t[1], Rest)
    assert t[0].written_duration == Duration(4, 8)
    assert t[1].written_duration == Duration(1, 8)
    assert not tietools.is_component_with_tie_spanner_attached(t[0])
    assert not tietools.is_component_with_tie_spanner_attached(t[1])


def test_resttools_make_rests_03():
    '''The 'tied' keyword can be set to True to return tied Rests.  '''
    t = resttools.make_rests((5, 8), tied=True)
    assert spannertools.get_the_only_spanner_attached_to_component(
        t[0], tietools.TieSpanner) is \
        spannertools.get_the_only_spanner_attached_to_component(
        t[1], tietools.TieSpanner)


def test_resttools_make_rests_04():
    '''resttools.make_rests can take a list of duration tokens.'''
    t = resttools.make_rests([(1, 4), Duration(1, 8)])
    assert t[0].written_duration == Duration(1, 4)
    assert t[1].written_duration == Duration(1, 8)
    assert not tietools.is_component_with_tie_spanner_attached(t[0])
    assert not tietools.is_component_with_tie_spanner_attached(t[1])
