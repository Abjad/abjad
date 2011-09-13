from abjad import *
from abjad.tools.spannertools._withdraw_components_in_expr_from_crossing_spanners import _withdraw_components_in_expr_from_crossing_spanners
import py.test


def test_spannertools__withdraw_components_in_expr_from_crossing_spanners_01():
    '''Withdraw thread-contiguous components from crossing spanners.'''

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

    _withdraw_components_in_expr_from_crossing_spanners([t])
    assert len(spanners) == 3
    assert beam in spanners
    assert slur in spanners
    assert trill in spanners


def test_spannertools__withdraw_components_in_expr_from_crossing_spanners_02():
    '''Withdraw thread-contiguous components from crossing spanners.'''

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

    spanners = spannertools.get_spanners_contained_by_components(t[0:1])
    assert len(spanners) == 2
    assert beam in spanners
    assert trill in spanners

    _withdraw_components_in_expr_from_crossing_spanners(t[0:1])

    r'''
    \new Voice {
        {
            c'8 [
            d'8 ]
        }
        {
            e'8 ( \startTrillSpan
            f'8 ) \stopTrillSpan
        }
    }
    '''

    spanners = spannertools.get_spanners_contained_by_components(t[0:1])
    assert len(spanners) == 1
    assert beam in spanners

    assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 ( \\startTrillSpan\n\t\tf'8 ) \\stopTrillSpan\n\t}\n}"


def test_spannertools__withdraw_components_in_expr_from_crossing_spanners_03():
    '''Withdraw thread-contiguous components from crossing spanners.'''

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

    spanners = spannertools.get_spanners_contained_by_components(t.leaves[2:3])
    assert len(spanners) == 2
    assert slur in spanners
    assert trill in spanners

    _withdraw_components_in_expr_from_crossing_spanners(t.leaves[2:3])

    spanners = spannertools.get_spanners_contained_by_components(t.leaves[2:3])
    assert spanners == set([])

    "Operation leaves score tree in weird state."
    "Both slur and trill are now discontiguous."

    assert not componenttools.is_well_formed_component(t)
