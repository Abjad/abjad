# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_leaf_durations_01():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    labeltools.label_leaves_in_expr_with_leaf_durations(tuplet)

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8
                _ \markup {
                    \column
                        {
                            \small
                                1/8
                            \small
                                1/12
                        }
                    }
            d'8
                _ \markup {
                    \column
                        {
                            \small
                                1/8
                            \small
                                1/12
                        }
                    }
            e'8
                _ \markup {
                    \column
                        {
                            \small
                                1/8
                            \small
                                1/12
                        }
                    }
        }
        '''
        )

    assert inspect_(tuplet).is_well_formed()
