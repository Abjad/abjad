# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_leaf_numbers_01():
    r'''Leaf numbers start at 1.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_leaf_numbers(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8
                _ \markup {
                    \small
                        1
                    }
            d'8
                _ \markup {
                    \small
                        2
                    }
            e'8
                _ \markup {
                    \small
                        3
                    }
            f'8
                _ \markup {
                    \small
                        4
                    }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_labeltools_label_leaves_in_expr_with_leaf_numbers_02():
    r'''Optional markup direction keyword.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_leaf_numbers(
        staff, markup_direction=Up)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8
                ^ \markup {
                    \small
                        1
                    }
            d'8
                ^ \markup {
                    \small
                        2
                    }
            e'8
                ^ \markup {
                    \small
                        3
                    }
            f'8
                ^ \markup {
                    \small
                        4
                    }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
