# -*- encoding: utf-8 -*-
from abjad import *


def test_FreeTupletSelection_diminished_to_augmented_01():

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    tuplets = selectiontools.select_tuplets([tuplet])
    tuplets.diminished_to_augmented()

    r'''
    \tweak #'text #tuplet-number::calc-fraction-text
    \times 4/3 {
        c'16
        d'16
        e'16
    }
    '''

    assert select(tuplet).is_well_formed()
    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'16
            d'16
            e'16
        }
        '''
        )
