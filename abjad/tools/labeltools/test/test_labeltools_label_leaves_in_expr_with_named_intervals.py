# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_named_intervals_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    labeltools.label_leaves_in_expr_with_named_intervals(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 ^ \markup { +M2 }
            d'8 ^ \markup { +M2 }
            e'8 ^ \markup { +m2 }
            f'8 ^ \markup { +M2 }
            g'8 ^ \markup { +M2 }
            a'8 ^ \markup { +M2 }
            b'8 ^ \markup { +m2 }
            c''8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_labeltools_label_leaves_in_expr_with_named_intervals_02():

    pitch_numbers = [0, 13, 11, 8, 2, 3, 9, 10, 6, 5]
    staff = Staff(scoretools.make_notes(pitch_numbers, [Duration(1, 8)]))
    labeltools.label_leaves_in_expr_with_named_intervals(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 ^ \markup { +aug8 }
            cs''8 ^ \markup { -M2 }
            b'8 ^ \markup { -aug2 }
            af'8 ^ \markup { -dim5 }
            d'8 ^ \markup { +m2 }
            ef'8 ^ \markup { +aug4 }
            a'8 ^ \markup { +m2 }
            bf'8 ^ \markup { -dim4 }
            fs'8 ^ \markup { -aug1 }
            f'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()
