# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent__select_vertical_moment_at_01():

    score = Score([])
    tuplet = scoretools.FixedDurationTuplet(Duration(4, 8), [])
    tuplet.extend("d''8 c''8 b'8")
    score.append(Staff([tuplet]))
    staff_group = StaffGroup([])
    staff_group.context_name = 'PianoStaff'
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

    def staff_group_moment(offset):
        return inspect_(staff_group).get_vertical_moment_at(offset)

    moment = staff_group_moment(Offset(0, 8))
    assert moment.leaves == (staff_group[0][0], staff_group[1][0])

    moment = staff_group_moment(Offset(1, 8))
    assert moment.leaves == (staff_group[0][0], staff_group[1][1])

    moment = staff_group_moment(Offset(2, 8))
    assert moment.leaves == (staff_group[0][1], staff_group[1][2])

    moment = staff_group_moment(Offset(3, 8))
    assert moment.leaves == (staff_group[0][1], staff_group[1][3])

    moment = staff_group_moment(Offset(99, 8))
    assert moment.leaves == ()


def test_agenttools_InspectionAgent__select_vertical_moment_at_02():

    score = Score([])
    tuplet = scoretools.FixedDurationTuplet(Duration(4, 8), [])
    tuplet.extend("d''8 c''8 b'8")
    score.append(Staff([tuplet]))
    staff_group = StaffGroup([])
    staff_group.context_name = 'PianoStaff'
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

    def scorewide_vertical_moment(offset):
        return inspect_(score).get_vertical_moment_at(offset)

    moment = scorewide_vertical_moment(Offset(0, 8))
    assert moment.leaves == (
        score[0][0][0],
        staff_group[0][0],
        staff_group[1][0],
        )

    moment = scorewide_vertical_moment(Offset(1, 8))
    assert moment.leaves == (
        score[0][0][0],
        staff_group[0][0],
        staff_group[1][1],
        )

    moment = scorewide_vertical_moment(Offset(2, 8))
    assert moment.leaves == (
        score[0][0][1],
        staff_group[0][1],
        staff_group[1][2],
        )

    moment = scorewide_vertical_moment(Offset(3, 8))
    assert moment.leaves == (
        score[0][0][2],
        staff_group[0][1],
        staff_group[1][3],
        )

    moment = scorewide_vertical_moment(Offset(99, 8))
    assert moment.leaves == ()
