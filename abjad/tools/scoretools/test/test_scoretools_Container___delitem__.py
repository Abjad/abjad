# -*- coding: utf-8 -*-
import abjad



def test_scoretools_Container___delitem___01():
    r'''Deletes in-score container.
    '''

    voice = abjad.Voice("{ c'8 ( d'8 ) } { e'8 ( f'8 ) }")
    leaves = abjad.select(voice).by_leaf()
    abjad.attach(abjad.Beam(), leaves)

    assert format(voice) == abjad.String.normalize(
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
        )

    container = voice[0]
    del(voice[0])

    # container no longer appears in score
    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                e'8 [ (
                f'8 ] )
            }
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()

    # container leaves are still slurred
    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8 (
            d'8 )
        }
        '''
        )

    assert abjad.inspect(container).is_well_formed()


def test_scoretools_Container___delitem___02():
    r'''Deletes in-score leaf.
    '''

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[1])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            e'8
            f'8 ]
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Container___delitem___03():
    r'''Deletes slice in middle of container.
    '''

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[1:3])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            f'8 ]
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Container___delitem___04():
    r'''Delete slice at beginning of container.
    '''

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[:2])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            e'8 [
            f'8 ]
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Container___delitem___05():
    r'''Deletes slice at end of container.
    '''

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[2:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Container___delitem___06():
    r'''Deletes container contents.
    '''

    voice = abjad.Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[:])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
        }
        '''
        )

    assert not len(voice)


def test_scoretools_Container___delitem___07():
    r'''Deletes leaf from tuplet.
    '''

    tuplet = abjad.Tuplet(abjad.Multiplier((2, 3)), "c'8 [ d'8 e'8 ]")
    del(tuplet[1])

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            c'8 [
            e'8 ]
        }
        '''
        )

    assert abjad.inspect(tuplet).is_well_formed()


def test_scoretools_Container___delitem___08():
    r'''Deletes leaf from nested container.
    '''

    voice = abjad.Voice("c'8 [ { d'8 e'8 } f'8 ]")
    leaves = abjad.select(voice).by_leaf()
    abjad.attach(abjad.Glissando(), leaves)

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            {
                d'8 \glissando
                e'8 \glissando
            }
            f'8 ]
        }
        '''
        )

    leaf = leaves[1]
    del(voice[1][0])

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            c'8 [ \glissando
            {
                e'8 \glissando
            }
            f'8 ]
        }
        '''
        )

    assert abjad.inspect(voice).is_well_formed()
    assert abjad.inspect(leaf).is_well_formed()
