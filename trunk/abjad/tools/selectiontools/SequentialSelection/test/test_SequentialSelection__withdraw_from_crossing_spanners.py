from abjad import *
import py.test


def test_SequentialSelection__withdraw_from_crossing_spanners_01():
    '''Withdraw thread-contiguous components from crossing spanners.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beam = spannertools.BeamSpanner(t[0][:])
    slur = spannertools.SlurSpanner(t[1][:])
    trill = spannertools.TrillSpanner(t.select_leaves())

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

    voice_selection = selectiontools.SequentialSelection([t])
    voice_selection._withdraw_from_crossing_spanners()
    assert len(spanners) == 3
    assert beam in spanners
    assert slur in spanners
    assert trill in spanners


def test_SequentialSelection__withdraw_from_crossing_spanners_02():
    '''Withdraw thread-contiguous components from crossing spanners.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beam = spannertools.BeamSpanner(t[0][:])
    slur = spannertools.SlurSpanner(t[1][:])
    trill = spannertools.TrillSpanner(t.select_leaves())

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

    t[:1]._withdraw_from_crossing_spanners()

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

    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 ( \\startTrillSpan\n\t\tf'8 ) \\stopTrillSpan\n\t}\n}"


def test_SequentialSelection__withdraw_from_crossing_spanners_03():
    '''Withdraw thread-contiguous components from crossing spanners.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beam = spannertools.BeamSpanner(t[0][:])
    slur = spannertools.SlurSpanner(t[1][:])
    trill = spannertools.TrillSpanner(t.select_leaves())

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

    spanners = spannertools.get_spanners_contained_by_components(t.select_leaves()[2:3])
    assert len(spanners) == 2
    assert slur in spanners
    assert trill in spanners

    t.select_leaves()[2:3]._withdraw_from_crossing_spanners()

    spanners = spannertools.get_spanners_contained_by_components(t.select_leaves()[2:3])
    assert spanners == set([])

    "Operation leaves score tree in weird state."
    "Both slur and trill are now discontiguous."

    assert not inspect(t).is_well_formed()
