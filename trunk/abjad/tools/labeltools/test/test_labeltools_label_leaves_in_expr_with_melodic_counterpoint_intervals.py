# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_melodic_counterpoint_intervals_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    labeltools.label_leaves_in_expr_with_melodic_counterpoint_intervals(staff)

    r'''
      \new Staff {
            c'8 ^ \markup { +2 }
            d'8 ^ \markup { +2 }
            e'8 ^ \markup { +2 }
            f'8 ^ \markup { +2 }
            g'8 ^ \markup { +2 }
            a'8 ^ \markup { +2 }
            b'8 ^ \markup { +2 }
            c''8
      }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 ^ \markup { +2 }
            d'8 ^ \markup { +2 }
            e'8 ^ \markup { +2 }
            f'8 ^ \markup { +2 }
            g'8 ^ \markup { +2 }
            a'8 ^ \markup { +2 }
            b'8 ^ \markup { +2 }
            c''8
        }
        '''
        )


def test_labeltools_label_leaves_in_expr_with_melodic_counterpoint_intervals_02():

    staff = Staff(notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)]))
    labeltools.label_leaves_in_expr_with_melodic_counterpoint_intervals(staff)

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r"""
        \new Staff {
            c'8 ^ \markup { +15 }
            cs'''8 ^ \markup { -9 }
            b'8 ^ \markup { -9 }
            af8 ^ \markup { -7 }
            bf,8 ^ \markup { 1 }
            b,8 ^ \markup { +14 }
            a'8 ^ \markup { +2 }
            bf'8 ^ \markup { -4 }
            fs'8 ^ \markup { 1 }
            f'8
        }
        """
        )
