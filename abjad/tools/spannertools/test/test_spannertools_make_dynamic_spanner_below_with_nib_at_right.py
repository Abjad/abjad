# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_make_dynamic_spanner_below_with_nib_at_right_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.make_dynamic_spanner_below_with_nib_at_right('mp', staff[:])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \override TextSpanner #'bound-details #'left #'text = \markup {
                \dynamic
                    {
                        mp
                    }
                }
            \override TextSpanner #'bound-details #'right #'text = \markup {
                \draw-line
                    #'(0 . 1)
                }
            \override TextSpanner #'bound-details #'right-broken #'text = ##f
            \override TextSpanner #'dash-fraction = #1
            \override TextSpanner #'direction = #down
            c'8 \startTextSpan
            d'8
            e'8
            f'8 \stopTextSpan
            \revert TextSpanner #'bound-details
            \revert TextSpanner #'dash-fraction
            \revert TextSpanner #'direction
        }
        ''',
        )
