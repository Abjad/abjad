from abjad import *
import py.test


def test_spannertools_get_spanners_that_dominate_components_01():
    '''Return Python list of (spanner, index) pairs.
        Each (spanner, index) pair gives a spanner which dominates
        all components in list, together with the start-index
        at which spanner attaches to subelement of first
        component in list.'''

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

    receipt = spannertools.get_spanners_that_dominate_components(t[:1])

    "Beam and trill dominate first container."

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_02():
    '''Beam, glissando and trill all dominante second container.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_components(t[1:2])

    assert len(receipt) == 3
    assert (beam, 1) in receipt
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_spannertools_get_spanners_that_dominate_components_03():
    '''Glissando and trill dominate last container.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_components(t[-1:])

    assert len(receipt) == 2
    assert (glissando, 1) in receipt
    assert (trill, 4) in receipt


def test_spannertools_get_spanners_that_dominate_components_04():
    '''Beam and trill dominate first two containers.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_components(t[:2])

    assert len(receipt) == 2
    assert (beam, 0) in receipt
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_05():
    '''Glissando and trill dominate last two containers.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_components(t[-2:])

    assert len(receipt) == 2
    assert (glissando, 0) in receipt
    assert (trill, 2) in receipt


def test_spannertools_get_spanners_that_dominate_components_06():
    '''Only trill dominates all three containers.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_components(t[:])

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_07():
    '''Only trill dominates voice.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_components([t])

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_08():
    '''Only trill dominates first two notes.
        Note that trill attaches to notes.
        Note that beam and glissando attach to containers.'''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    receipt = spannertools.get_spanners_that_dominate_components(t.leaves[:2])

    assert len(receipt) == 1
    assert (trill, 0) in receipt


def test_spannertools_get_spanners_that_dominate_components_09():
    '''Works on empty containers.
        Implementation does not depend on component duration.'''

    t = Voice(Container([]) * 3)
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[1:])
    trill = spannertools.TrillSpanner(t.leaves)

    r'''
    \new Voice {
        {
        }
        {
        }
        {
        }
    }
    '''

    receipt = spannertools.get_spanners_that_dominate_components(t[:1])

    "Only beam dominates first container."

    assert len(receipt) == 1
    assert (beam, 0) in receipt
