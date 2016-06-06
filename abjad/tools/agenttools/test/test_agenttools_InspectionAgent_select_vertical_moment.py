# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_select_vertical_moment_01():

    score = Score([])
    tuplet = scoretools.FixedDurationTuplet(Duration(4, 8), "d''8 c''8 b'8")
    score.append(Staff([tuplet]))
    staff_group = StaffGroup(context_name='PianoStaff')
    staff_group.append(Staff("a'4 g'4"))
    staff_group.append(Staff("f'8 e'8 d'8 c'8"))
    clef = Clef('bass')
    attach(clef, staff_group[1])
    score.append(staff_group)

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    d''8
                    c''8
                    b'8
                }
            }
            \new PianoStaff <<
                \new Staff {
                    a'4
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    f'8
                    e'8
                    d'8
                    c'8
                }
            >>
        >>
        '''
        )

    def staff_group_moment(expr):
        return inspect_(expr).get_vertical_moment(governor=staff_group)

    moment = staff_group_moment(staff_group[1][0])
    assert moment.leaves == (staff_group[0][0], staff_group[1][0])

    moment = staff_group_moment(staff_group[1][1])
    assert moment.leaves == (staff_group[0][0], staff_group[1][1])

    moment = staff_group_moment(staff_group[1][2])
    assert moment.leaves == (staff_group[0][1], staff_group[1][2])

    moment = staff_group_moment(staff_group[1][3])
    assert moment.leaves == (staff_group[0][1], staff_group[1][3])


def test_agenttools_InspectionAgent_select_vertical_moment_02():

    score = Score([])
    tuplet = scoretools.FixedDurationTuplet(Duration(4, 8), "d''8 c''8 b'8")
    score.append(Staff([tuplet]))
    staff_group = StaffGroup(context_name='PianoStaff')
    staff_group.append(Staff("a'4 g'4"))
    staff_group.append(Staff("f'8 e'8 d'8 c'8"))
    clef = Clef('bass')
    attach(clef, staff_group[1])
    score.append(staff_group)

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    d''8
                    c''8
                    b'8
                }
            }
            \new PianoStaff <<
                \new Staff {
                    a'4
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    f'8
                    e'8
                    d'8
                    c'8
                }
            >>
        >>
        '''
        )

    moment = inspect_(staff_group[1][0]).get_vertical_moment()
    assert moment.leaves == (
        score[0][0][0],
        staff_group[0][0],
        staff_group[1][0],
        )

    moment = inspect_(staff_group[1][1]).get_vertical_moment()
    assert moment.leaves == (
        score[0][0][0],
        staff_group[0][0],
        staff_group[1][1],
        )

    moment = inspect_(staff_group[1][2]).get_vertical_moment()
    assert moment.leaves == (
        score[0][0][1],
        staff_group[0][1],
        staff_group[1][2],
        )

    moment = inspect_(staff_group[1][3]).get_vertical_moment()
    assert moment.leaves == (
        score[0][0][2],
        staff_group[0][1],
        staff_group[1][3],
        )
