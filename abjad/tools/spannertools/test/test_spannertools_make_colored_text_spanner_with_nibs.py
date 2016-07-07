# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_make_colored_text_spanner_with_nibs_01():
    r'''Bracket defaults to solid red line with left and right nibs
    and with no nibs at left and right broken edges.
    '''

    staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = select(staff).by_leaf()
    spanner = spannertools.make_colored_text_spanner_with_nibs()
    attach(spanner, leaves[2:4])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \override TextSpanner.bound-details.left-broken.text = ##f
                \override TextSpanner.bound-details.left.text = \markup {
                    \draw-line
                        #'(0 . -1)
                    }
                \override TextSpanner.bound-details.right-broken.text = ##f
                \override TextSpanner.bound-details.right.text = \markup {
                    \draw-line
                        #'(0 . -1)
                    }
                \override TextSpanner.color = #red
                \override TextSpanner.dash-fraction = #1
                \override TextSpanner.staff-padding = #2
                \override TextSpanner.thickness = #1.5
                e'8 \startTextSpan
                f'8 \stopTextSpan
                \revert TextSpanner.bound-details
                \revert TextSpanner.color
                \revert TextSpanner.dash-fraction
                \revert TextSpanner.staff-padding
                \revert TextSpanner.thickness
            }
            {
                g'8
                a'8
            }
        }
        '''
        )
