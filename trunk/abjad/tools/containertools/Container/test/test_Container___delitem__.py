# -*- encoding: utf-8 -*-
from abjad import *



def test_Container___delitem___01():
    r'''Delete spanned component.
    Component withdraws crossing spanners.
    Component carries covered spanners forward.
    Operation always leaves all expressions in tact.
    '''

    t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t[:])
    spannertools.SlurSpanner(t[0][:])
    spannertools.SlurSpanner(t[1][:])

    r'''
    \new Voice {
        {
            c'8 [ (
            d'8 )
        }
        {
            e'8 (
            f'8 ] )
        }
    }
    '''

    old = t[0]
    del(t[0])

    "Container t is now ..."

    r'''
    \new Voice {
        {
            e'8 [ (
            f'8 ] )
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            {
                e'8 [ (
                f'8 ] )
            }
        }
        '''
        )

    "Deleted component is now ..."

    r'''
    {
        c'8 (
        d'8 )
    }
    '''

    assert select(old).is_well_formed()
    assert testtools.compare(
        old.lilypond_format,
        r'''
        {
            c'8 (
            d'8 )
        }
        '''
        )


def test_Container___delitem___02():
    r'''Delete 1 leaf in container.
    Spanner structure is preserved.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[1])

    r'''
    \new Voice {
        c'8 [
        e'8
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            e'8
            f'8 ]
        }
        '''
        )


def test_Container___delitem___03():
    r'''Delete slice in middle of container.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[1:3])

    r'''
    \new Voice {
        c'8 [
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            f'8 ]
        }
        '''
        )


def test_Container___delitem___04():
    r'''Delete slice from beginning to middle of container.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[:2])

    r'''
    \new Voice {
        e'8 [
        f'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            e'8 [
            f'8 ]
        }
        '''
        )


def test_Container___delitem___05():
    r'''Delete slice from middle to end of container.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[2:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )


def test_Container___delitem___06():
    r'''Delete slice from beginning to end of container.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    del(t[:])

    r'''
    \new Voice {
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Voice {
        }
        '''
        )


def test_Container___delitem___07():
    r'''Detach leaf from tuplet and spanner.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])

    del(t[1])

    r'''
    {
        c'8 [
        e'8 ]
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        {
            c'8 [
            e'8 ]
        }
        '''
        )
