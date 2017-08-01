# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Tuplet_toggle_prolation_01():
    '''Change augmentation to diminution.
    '''

    tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'8
            d'8
            e'8
        }
        '''
        )

    tuplet.toggle_prolation()

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'4
            d'4
            e'4
        }
        '''
        )

    assert abjad.inspect(tuplet).is_well_formed()


def test_scoretools_Tuplet_toggle_prolation_02():
    '''Change diminution to augmentation.
    '''

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )

    tuplet.toggle_prolation()

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'16
            d'16
            e'16
        }
        '''
        )

    assert abjad.inspect(tuplet).is_well_formed()
