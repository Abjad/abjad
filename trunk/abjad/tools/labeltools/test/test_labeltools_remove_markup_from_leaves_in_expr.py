# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_remove_markup_from_leaves_in_expr_01():
    r'''Clear multiple pieces of down-markup.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    labeltools.label_leaves_in_expr_with_leaf_durations(t)

    r'''
    \times 2/3 {
        c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
        d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
        e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
    }
    '''

    labeltools.remove_markup_from_leaves_in_expr(t)

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )
