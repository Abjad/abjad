# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_leaf_indices_01():
    r'''Leaf indices start at 0.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    labeltools.label_leaves_in_expr_with_leaf_indices(staff)

    r'''
    \new Staff {
        c'8
            _ \markup {
                \small
                    0
                }
        d'8
            _ \markup {
                \small
                    1
                }
        e'8
            _ \markup {
                \small
                    2
                }
        f'8
            _ \markup {
                \small
                    3
                }
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
                _ \markup {
                    \small
                        0
                    }
            d'8
                _ \markup {
                    \small
                        1
                    }
            e'8
                _ \markup {
                    \small
                        2
                    }
            f'8
                _ \markup {
                    \small
                        3
                    }
        }
        '''
        )
