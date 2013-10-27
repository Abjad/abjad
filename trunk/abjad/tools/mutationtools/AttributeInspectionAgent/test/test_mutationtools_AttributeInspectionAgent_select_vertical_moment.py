# -*- encoding: utf-8 -*-
from abjad import *


def test_mutationtools_AttributeInspectionAgent_select_vertical_moment_01():

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

    def piano_staff_moment(expr):
        return inspect(expr).get_vertical_moment(governor=piano_staff)

    moment = piano_staff_moment(piano_staff[1][0])
    assert moment.leaves == (piano_staff[0][0], piano_staff[1][0])

    moment = piano_staff_moment(piano_staff[1][1])
    assert moment.leaves == (piano_staff[0][0], piano_staff[1][1])

    moment = piano_staff_moment(piano_staff[1][2])
    assert moment.leaves == (piano_staff[0][1], piano_staff[1][2])

    moment = piano_staff_moment(piano_staff[1][3])
    assert moment.leaves == (piano_staff[0][1], piano_staff[1][3])


def test_mutationtools_AttributeInspectionAgent_select_vertical_moment_02():

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

    moment = inspect(piano_staff[1][0]).get_vertical_moment()
    assert moment.leaves == (
        score[0][0][0], 
        piano_staff[0][0], 
        piano_staff[1][0],
        )

    moment = inspect(piano_staff[1][1]).get_vertical_moment()
    assert moment.leaves == (
        score[0][0][0], 
        piano_staff[0][0], 
        piano_staff[1][1],
        )

    moment = inspect(piano_staff[1][2]).get_vertical_moment()
    assert moment.leaves == (
        score[0][0][1], 
        piano_staff[0][1], 
        piano_staff[1][2],
        )

    moment = inspect(piano_staff[1][3]).get_vertical_moment()
    assert moment.leaves == (
        score[0][0][2], 
        piano_staff[0][1], 
        piano_staff[1][3],
        )
