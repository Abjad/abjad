from abjad import *


def test_resttools_make_rests_01():
    '''Make rest.
    '''

    t = resttools.make_rests((1, 4))
    assert isinstance(t, list)
    assert len(t) == 1
    assert isinstance(t[0], Rest)
    assert t[0].written_duration == Duration(1, 4)
    assert len(t[0].select_tie_chain()) == 1


def test_resttools_make_rests_02():
    '''Do not tie rests.
    '''

    t = resttools.make_rests((5, 8))
    assert len(t) == 2
    assert isinstance(t[0], Rest)
    assert isinstance(t[1], Rest)
    assert t[0].written_duration == Duration(4, 8)
    assert t[1].written_duration == Duration(1, 8)
    assert all(len(x.select_tie_chain()) == 1 for x in t)


def test_resttools_make_rests_03():
    '''Do tie rests.
    '''

    t = resttools.make_rests((5, 8), tie_parts=True)
    assert all(len(x.select_tie_chain()) == 2 for x in t)


def test_resttools_make_rests_04():
    '''Make rests.
    '''

    t = resttools.make_rests([(1, 4), Duration(1, 8)])
    assert t[0].written_duration == Duration(1, 4)
    assert t[1].written_duration == Duration(1, 8)
    assert all(len(x.select_tie_chain()) == 1 for x in t)
