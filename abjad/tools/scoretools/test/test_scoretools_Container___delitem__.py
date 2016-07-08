# -*- coding: utf-8 -*-
from abjad import *



def test_scoretools_Container___delitem___01():
    r'''Deletes in-score container.
    '''

    voice = Voice("{ c'8 ( d'8 ) } { e'8 ( f'8 ) }")
    leaves = select(voice).by_leaf()
    attach(Beam(), leaves)

    assert format(voice) == stringtools.normalize(
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
    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                e'8 [ (
                f'8 ] )
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()

    # container leaves are still slurred
    assert format(container) == stringtools.normalize(
        r'''
        {
            c'8 (
            d'8 )
        }
        '''
        )

    assert inspect_(container).is_well_formed()


def test_scoretools_Container___delitem___02():
    r'''Deletes in-score leaf.
    '''

    voice = Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[1])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            e'8
            f'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___delitem___03():
    r'''Deletes slice in middle of container.
    '''

    voice = Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[1:3])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            f'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___delitem___04():
    r'''Delete slice at beginning of container.
    '''

    voice = Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[:2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            e'8 [
            f'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___delitem___05():
    r'''Deletes slice at end of container.
    '''

    voice = Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[2:])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Container___delitem___06():
    r'''Deletes container contents.
    '''

    voice = Voice("c'8 [ d'8 e'8 f'8 ]")
    del(voice[:])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
        }
        '''
        )

    assert not len(voice)


def test_scoretools_Container___delitem___07():
    r'''Deletes leaf from tuplet.
    '''

    tuplet = Tuplet(Multiplier((2, 3)), "c'8 [ d'8 e'8 ]")
    del(tuplet[1])

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak edge-height #'(0.7 . 0)
        \times 2/3 {
            c'8 [
            e'8 ]
        }
        '''
        )

    assert inspect_(tuplet).is_well_formed()


def test_scoretools_Container___delitem___08():
    r'''Deletes leaf from nested container.
    '''

    voice = Voice("c'8 [ { d'8 e'8 } f'8 ]")
    leaves = select(voice).by_leaf()
    attach(Glissando(), list(leaves))

    assert format(voice) == stringtools.normalize(
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

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()
    assert inspect_(leaf).is_well_formed()
