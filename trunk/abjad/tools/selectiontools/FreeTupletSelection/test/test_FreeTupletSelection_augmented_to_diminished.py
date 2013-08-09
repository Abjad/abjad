# -*- encoding: utf-8 -*-
from abjad import *


def test_FreeTupletSelection_augmented_to_diminished_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")

    r'''
    \times 4/3 {
        c'8
        d'8
        e'8
    }
    '''

    tuplets = selectiontools.select_tuplets([tuplet])
    tuplets.augmented_to_diminished()

    r'''
    \times 2/3 {
        c'4
        d'4
        e'4
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'4
            d'4
            e'4
        }
        '''
        )
