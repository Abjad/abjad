# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_append_spacer_skips_to_underfull_measures_in_expr_01():

    staff = Staff(Measure((3, 8), "c'8 d'8 e'8") * 3)
    detach(TimeSignature, staff[1])
    time_signature = TimeSignature((4, 8))
    attach(time_signature, staff[1])
    detach(TimeSignature, staff[2])
    time_signature = TimeSignature((5, 8))
    attach(time_signature, staff[2])

    assert not staff[0].is_underfull
    assert staff[1].is_underfull
    assert staff[2].is_underfull

    scoretools.append_spacer_skips_to_underfull_measures_in_expr(staff)

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()
