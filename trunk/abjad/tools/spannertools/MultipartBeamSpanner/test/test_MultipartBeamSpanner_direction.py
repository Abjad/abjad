from abjad import *


def test_MultipartBeamSpanner_direction_01():

    staff = Staff("c'8 d'8 r8 e'8 f'8 g'4")
    spanner = spannertools.MultipartBeamSpanner(staff, direction='up')

    r'''
    \new Staff {
        c'8 ^ [
        d'8 ]
        r8
        e'8 ^ [
        f'8 ]
        g'4
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 ^ [\n\td'8 ]\n\tr8\n\te'8 ^ [\n\tf'8 ]\n\tg'4\n}"

    spanner.direction = 'down'

    assert staff.format == "\\new Staff {\n\tc'8 _ [\n\td'8 ]\n\tr8\n\te'8 _ [\n\tf'8 ]\n\tg'4\n}"
