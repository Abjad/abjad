from abjad import *
import py.test


def test_spannertools_get_spanners_contained_by_components_01():
    '''Return unordered set of spanners contained
        within any of the list of thread-contiguous components.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[0][:])
    slur = spannertools.SlurSpanner(t[1][:])
    trill = spannertools.TrillSpanner(t.leaves)

    r'''
    \new Voice {
        {
            c'8 [ \startTrillSpan
            d'8 ]
        }
        {
            e'8 (
            f'8 ) \stopTrillSpan
        }
    }
    '''

    spanners = spannertools.get_spanners_contained_by_components([t])
    assert len(spanners) == 3
    assert beam in spanners
    assert slur in spanners
    assert trill in spanners

    spanners = spannertools.get_spanners_contained_by_components(t.leaves)
    assert len(spanners) == 3
    assert beam in spanners
    assert slur in spanners
    assert trill in spanners

    spanners = spannertools.get_spanners_contained_by_components(t[0:1])
    assert len(spanners) == 2
    assert beam in spanners
    assert trill in spanners

    spanners = spannertools.get_spanners_contained_by_components(t.leaves[0:1])
    assert len(spanners) == 2
    assert beam in spanners
    assert trill in spanners
