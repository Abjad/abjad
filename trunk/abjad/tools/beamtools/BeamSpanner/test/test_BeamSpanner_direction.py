from abjad import *


def test_BeamSpanner_direction_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beamtools.BeamSpanner(staff[:4], direction=Up)

    r'''
    \new Staff {
        c'8 ^ [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 ^ [\n\td'8\n\te'8\n\tf'8 ]\n\tg'2\n}"


def test_BeamSpanner_direction_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beamtools.BeamSpanner(staff[:4], direction=Down)

    r'''
    \new Staff {
        c'8 _ [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 _ [\n\td'8\n\te'8\n\tf'8 ]\n\tg'2\n}"


def test_BeamSpanner_direction_03():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    beamtools.BeamSpanner(staff[:4], direction=Center)

    r'''
    \new Staff {
        c'8 - [
        d'8
        e'8
        f'8 ]
        g'2
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 - [\n\td'8\n\te'8\n\tf'8 ]\n\tg'2\n}"
