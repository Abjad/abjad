# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_append_spacer_skips_to_underfull_measures_in_expr_01():

    staff = Staff(Measure((3, 8), "c'8 d'8 e'8") * 3)
    inspect(staff[1]).get_mark(TimeSignature).detach()
    time_signature = TimeSignature((4, 8))
    attach(time_signature, staff[1])
    inspect(staff[2]).get_mark(TimeSignature).detach()
    time_signature = TimeSignature((5, 8))
    attach(time_signature, staff[2])

    assert not staff[0].is_underfull
    assert staff[1].is_underfull
    assert staff[2].is_underfull

    scoretools.append_spacer_skips_to_underfull_measures_in_expr(staff)

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()
