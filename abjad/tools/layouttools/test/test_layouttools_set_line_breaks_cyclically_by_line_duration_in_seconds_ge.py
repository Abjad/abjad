# -*- encoding: utf-8 -*-
from abjad import *


def test_layouttools_set_line_breaks_cyclically_by_line_duration_in_seconds_ge_01():
    r'''Iterate line-break class instances in expr and 
    accumulate duration in seconds.
    Add line break after every total less than or equal to line_duration.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    staff.append(Measure((2, 8), "g'8 a'8"))
    staff.append(Measure((2, 8), "b'8 c''8"))
    tempo = Tempo(Duration(1, 8), 44, _target_context=Staff)
    attach(tempo, staff)
    layouttools.set_line_breaks_cyclically_by_line_duration_in_seconds_ge(
        staff, 
        Duration(6),
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \tempo 8=44
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
                \break
            }
            {
                g'8
                a'8
            }
            {
                b'8
                c''8
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
