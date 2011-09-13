from abjad import *


def test_spannertools_get_spanners_that_dominate_component_pair_01():
    '''Return Python list of (spanner, index) pairs.
        Each spanner dominates a *crack* between components.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    r'''
    \new Voice {
        {
            c'8 [ \startTrillSpan
            d'8
        }
        {
            e'8 \glissando
            f'8 ] \glissando
        }
        {
            g'8 \glissando
            a'8 \stopTrillSpan
        }
    }
    '''

    "No spanners dominate t[0:0]"

    receipt = spannertools.get_spanners_that_dominate_component_pair(None, t[0])

    assert len(receipt) == 0
    assert receipt == set([])


def test_spannertools_get_spanners_that_dominate_component_pair_02():
    '''Beam and trill both dominate crack at t[1:1].'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_component_pair(t[0], t[1])

    assert len(receipt) == 2
    assert (beam, 1) in receipt
    assert (trill, 2) in receipt


def test_spannertools_get_spanners_that_dominate_component_pair_03():
    '''Glissando and trill both dominate crack at t[2:2].'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_component_pair(t[1], t[2])

    assert len(receipt) == 2
    assert (glissando, 1) in receipt
    assert (trill, 4) in receipt


def test_spannertools_get_spanners_that_dominate_component_pair_04():
    '''No spanners dominate 'crack' following voice.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_component_pair(t[2], None)

    assert len(receipt) == 0
    assert receipt == set([])
