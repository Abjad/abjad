# -*- encoding: utf-8 -*-
from abjad import *


def test_mutationtools_AttributeInspectionAgent__select_vertical_moment_at_01():

    score = Score([])
    score.append(Staff([tuplettools.FixedDurationTuplet(
        Duration(4, 8), "d''8 c''8 b'8")]))
    piano_staff = scoretools.PianoStaff([])
    piano_staff.append(Staff("a'4 g'4"))
    piano_staff.append(Staff("f'8 e'8 d'8 c'8"))
    clef = contexttools.ClefMark('bass')
    clef.attach(piano_staff[1])
    score.append(piano_staff)

    assert testtools.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
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

    def piano_staff_moment(offset):
        return inspect(piano_staff).get_vertical_moment_at(offset)

    moment = piano_staff_moment(Offset(0, 8))
    assert moment.leaves == (piano_staff[0][0], piano_staff[1][0])

    moment = piano_staff_moment(Offset(1, 8))
    assert moment.leaves == (piano_staff[0][0], piano_staff[1][1])

    moment = piano_staff_moment(Offset(2, 8))
    assert moment.leaves == (piano_staff[0][1], piano_staff[1][2])

    moment = piano_staff_moment(Offset(3, 8))
    assert moment.leaves == (piano_staff[0][1], piano_staff[1][3])

    moment = piano_staff_moment(Offset(99, 8))
    assert moment.leaves == ()


def test_mutationtools_AttributeInspectionAgent__select_vertical_moment_at_02():

    score = Score([])
    score.append(Staff([tuplettools.FixedDurationTuplet(
        Duration(4, 8), "d''8 c''8 b'8")]))
    piano_staff = scoretools.PianoStaff([])
    piano_staff.append(Staff("a'4 g'4"))
    piano_staff.append(Staff("f'8 e'8 d'8 c'8"))
    clef = contexttools.ClefMark('bass')
    clef.attach(piano_staff[1])
    score.append(piano_staff)

    assert testtools.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
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
        return inspect(score).get_vertical_moment_at(offset)

    moment = scorewide_vertical_moment(Offset(0, 8))
    assert moment.leaves == (
        score[0][0][0], 
        piano_staff[0][0], 
        piano_staff[1][0],
        )

    moment = scorewide_vertical_moment(Offset(1, 8))
    assert moment.leaves == (
        score[0][0][0], 
        piano_staff[0][0], 
        piano_staff[1][1],
        )

    moment = scorewide_vertical_moment(Offset(2, 8))
    assert moment.leaves == (
        score[0][0][1], 
        piano_staff[0][1], 
        piano_staff[1][2],
        )

    moment = scorewide_vertical_moment(Offset(3, 8))
    assert moment.leaves == (
        score[0][0][2], 
        piano_staff[0][1], 
        piano_staff[1][3],
        )

    moment = scorewide_vertical_moment(Offset(99, 8))
    assert moment.leaves == ()
