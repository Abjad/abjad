# -*- encoding: utf-8 -*-
from abjad import *



def test_Container___delitem___01():
    r'''Delete spanned component.
    Component withdraws crossing spanners.
    Component carries covered spanners forward.
    Operation always leaves all expressions in tact.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice[:])
    spannertools.SlurSpanner(voice[0][:])
    spannertools.SlurSpanner(voice[1][:])

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

    old = voice[0]
    del(voice[0])

    "Container voice is now ..."

    r'''
    \new Voice {
        {
            e'8 [ (
            f'8 ] )
        }
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
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

    assert inspect(old).is_well_formed()
    assert testtools.compare(
        old,
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

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])

    del(voice[1])

    r'''
    \new Voice {
        c'8 [
        e'8
        f'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
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

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])

    del(voice[1:3])

    r'''
    \new Voice {
        c'8 [
        f'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
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

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])

    del(voice[:2])

    r'''
    \new Voice {
        e'8 [
        f'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
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

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])

    del(voice[2:])

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
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

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])

    del(voice[:])

    r'''
    \new Voice {
    }
    '''

    assert inspect(voice).is_well_formed()
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
        }
        '''
        )


def test_Container___delitem___07():
    r'''Detach leaf from tuplet and spanner.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(tuplet[:])

    del(tuplet[1])

    r'''
    {
        c'8 [
        e'8 ]
    }
    '''

    assert inspect(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet,
        r'''
        {
            c'8 [
            e'8 ]
        }
        '''
        )
