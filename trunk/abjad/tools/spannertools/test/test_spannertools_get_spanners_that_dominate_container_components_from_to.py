from abjad import *


def test_spannertools_get_spanners_that_dominate_container_components_from_to_01():
    '''Get dominant spanners over zero-length 'crack'.'''

    t = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[:])

    r'''
    \new Voice {
        c'8 [ \glissando
        d'8 ] \glissando
        e'8 \glissando
        f'8
    }
    '''

    receipt = spannertools.get_spanners_that_dominate_container_components_from_to(t, 2, 2)

    assert len(receipt) == 1
    assert (glissando, 2) in receipt


def test_spannertools_get_spanners_that_dominate_container_components_from_to_02():
    '''Get dominant spanners over one-component slice.'''

    t = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[:])

    r'''
    \new Voice {
        c'8 [ \glissando
        d'8 ] \glissando
        e'8 \glissando
        f'8
    }
    '''

    receipt = spannertools.get_spanners_that_dominate_container_components_from_to(t, 1, 2)

    assert len(receipt) == 2
    assert (beam, 1) in receipt
    assert (glissando, 1) in receipt


def test_spannertools_get_spanners_that_dominate_container_components_from_to_03():
    '''Get dominant spanners over four-component slice.'''

    t = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(t[:2])
    glissando = spannertools.GlissandoSpanner(t[:])

    r'''
    \new Voice {
        c'8 [ \glissando
        d'8 ] \glissando
        e'8 \glissando
        f'8
    }
    '''

    receipt = spannertools.get_spanners_that_dominate_container_components_from_to(t, 0, 4)

    assert len(receipt) == 1
    assert (glissando, 0) in receipt
