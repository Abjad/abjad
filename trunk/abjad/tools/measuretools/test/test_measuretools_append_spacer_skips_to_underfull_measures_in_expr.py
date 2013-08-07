# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_append_spacer_skips_to_underfull_measures_in_expr_01():

    staff = Staff(Measure((3, 8), "c'8 d'8 e'8") * 3)
    staff[1].select().detach_marks(contexttools.TimeSignatureMark)
    contexttools.TimeSignatureMark((4, 8))(staff[1])
    staff[2].select().detach_marks(contexttools.TimeSignatureMark)
    contexttools.TimeSignatureMark((5, 8))(staff[2])

    assert not staff[0].is_underfull
    assert staff[1].is_underfull
    assert staff[2].is_underfull

    measuretools.append_spacer_skips_to_underfull_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 3/8
            c'8
            d'8
            e'8
        }
        {
            \time 4/8
            c'8
            d'8
            e'8
            s1 * 1/8
        }
        {
            \time 5/8
            c'8
            d'8
            e'8
            s1 * 1/4
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            {
                \time 3/8
                c'8
                d'8
                e'8
            }
            {
                \time 4/8
                c'8
                d'8
                e'8
                s1 * 1/8
            }
            {
                \time 5/8
                c'8
                d'8
                e'8
                s1 * 1/4
            }
        }
        '''
        )
