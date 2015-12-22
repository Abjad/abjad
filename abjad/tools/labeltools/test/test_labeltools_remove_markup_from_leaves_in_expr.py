# -*- coding: utf-8 -*-
from abjad import *


def test_labeltools_remove_markup_from_leaves_in_expr_01():
    r'''Clear multiple pieces of down-markup.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    label(tuplet).with_durations()

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8
                ^ \markup {
                    \small
                        1/12
                    }
            d'8
                ^ \markup {
                    \small
                        1/12
                    }
            e'8
                ^ \markup {
                    \small
                        1/12
                    }
        }
        '''
        ), repr(format(tuplet))

    labeltools.remove_markup_from_leaves_in_expr(tuplet)

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )

    assert inspect_(tuplet).is_well_formed()