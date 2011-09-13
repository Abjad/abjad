from abjad import *


def test_SlurSpanner_01():
    '''Slur spanner can attach to a container.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    s = spannertools.SlurSpanner(t)

    r'''
    \new Voice {
        c'8 (
        d'8
        e'8
        f'8 )
    }
    '''

    assert t.spanners == set([s])
    assert t.format == "\\new Voice {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"


def test_SlurSpanner_02():
    '''Slur spanner can attach to leaves.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    s = spannertools.SlurSpanner(t[:])

    assert len(t.spanners) == 0
    for leaf in t.leaves:
        assert leaf.spanners == set([s])
    assert t.format == "\\new Voice {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
