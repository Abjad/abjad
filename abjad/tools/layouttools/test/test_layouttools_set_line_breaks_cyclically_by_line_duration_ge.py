# -*- encoding: utf-8 -*-
from abjad import *


def test_layouttools_set_line_breaks_cyclically_by_line_duration_ge_01():
    r'''Iterate classes in expr and accumulate duration.
    Add line break after every total le line duration.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    staff.append(Measure((2, 8), "g'8 a'8"))
    staff.append(Measure((2, 8), "b'8 c''8"))
    layouttools.set_line_breaks_cyclically_by_line_duration_ge(
        staff, 
        Duration(4, 8),
        )

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
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
                \break
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_layouttools_set_line_breaks_cyclically_by_line_duration_ge_02():
    r'''Iterate classes in expr and accumulate duration.
    Add line break after every total le line duration.
    '''

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    staff.append(Measure((2, 8), "g'8 a'8"))
    staff.append(Measure((2, 8), "b'8 c''8"))
    layouttools.set_line_breaks_cyclically_by_line_duration_ge(
        staff, 
        Duration(1, 8), 
        line_break_class=scoretools.Leaf,
        )

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                \break
                d'8
                \break
            }
            {
                e'8
                \break
                f'8
                \break
            }
            {
                g'8
                \break
                a'8
                \break
            }
            {
                b'8
                \break
                c''8
                \break
            }
        }
        '''
        )

    assert inspect(staff).is_well_formed()
