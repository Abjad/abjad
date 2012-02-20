from abjad import *


def test_BeamSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.BeamSpanner(staff[:4], direction='up')

    r'''
    \new Staff {
        c'8 ^ [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 ^ [\n\td'8\n\te'8\n\tf'8 ]\n\tg'2\n}"


def test_BeamSpanner_direction_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.BeamSpanner(staff[:4], direction='down')

    r'''
    \new Staff {
        c'8 _ [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 _ [\n\td'8\n\te'8\n\tf'8 ]\n\tg'2\n}"


def test_BeamSpanner_direction_03():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    spannertools.BeamSpanner(staff[:4], direction='-')

    r'''
    \new Staff {
        c'8 - [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 - [\n\td'8\n\te'8\n\tf'8 ]\n\tg'2\n}"
