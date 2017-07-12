# -*- coding: utf-8 -*-
import abjad


def test_agenttools_InspectionAgent_get_vertical_moment_at_01():

    score = abjad.Score([])
    tuplet = abjad.Tuplet((4, 3), "d''8 c''8 b'8")
    score.append(abjad.Staff([tuplet]))
    staff_group = abjad.StaffGroup([])
    staff_group.context_name = 'PianoStaff'
    staff_group.append(abjad.Staff("a'4 g'4"))
    staff_group.append(abjad.Staff("f'8 e'8 d'8 c'8"))
    clef = abjad.Clef('bass')
    abjad.attach(clef, staff_group[1])
    score.append(staff_group)

    assert format(score) == abjad.String.normalize(
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
        return abjad.inspect(staff_group).get_vertical_moment_at(offset)

    moment = staff_group_moment(abjad.Offset(0, 8))
    assert moment.leaves == (staff_group[0][0], staff_group[1][0])

    moment = staff_group_moment(abjad.Offset(1, 8))
    assert moment.leaves == (staff_group[0][0], staff_group[1][1])

    moment = staff_group_moment(abjad.Offset(2, 8))
    assert moment.leaves == (staff_group[0][1], staff_group[1][2])

    moment = staff_group_moment(abjad.Offset(3, 8))
    assert moment.leaves == (staff_group[0][1], staff_group[1][3])

    moment = staff_group_moment(abjad.Offset(99, 8))
    assert moment.leaves == ()


def test_agenttools_InspectionAgent_get_vertical_moment_at_02():

    score = abjad.Score([])
    tuplet = abjad.Tuplet((4, 3), "d''8 c''8 b'8")
    score.append(abjad.Staff([tuplet]))
    staff_group = abjad.StaffGroup([])
    staff_group.context_name = 'PianoStaff'
    staff_group.append(abjad.Staff("a'4 g'4"))
    staff_group.append(abjad.Staff("f'8 e'8 d'8 c'8"))
    clef = abjad.Clef('bass')
    abjad.attach(clef, staff_group[1])
    score.append(staff_group)

    assert format(score) == abjad.String.normalize(
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
        return abjad.inspect(score).get_vertical_moment_at(offset)

    moment = scorewide_vertical_moment(abjad.Offset(0, 8))
    assert moment.leaves == (
        score[0][0][0],
        staff_group[0][0],
        staff_group[1][0],
        )

    moment = scorewide_vertical_moment(abjad.Offset(1, 8))
    assert moment.leaves == (
        score[0][0][0],
        staff_group[0][0],
        staff_group[1][1],
        )

    moment = scorewide_vertical_moment(abjad.Offset(2, 8))
    assert moment.leaves == (
        score[0][0][1],
        staff_group[0][1],
        staff_group[1][2],
        )

    moment = scorewide_vertical_moment(abjad.Offset(3, 8))
    assert moment.leaves == (
        score[0][0][2],
        staff_group[0][1],
        staff_group[1][3],
        )

    moment = scorewide_vertical_moment(abjad.Offset(99, 8))
    assert moment.leaves == ()
