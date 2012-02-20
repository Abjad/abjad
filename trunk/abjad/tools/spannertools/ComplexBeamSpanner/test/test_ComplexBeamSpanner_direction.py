from abjad import *


def test_ComplexBeamSpanner_direction_01():

    staff = Staff("c'16 e'16 r16 f'16 g'2")
    spannertools.ComplexBeamSpanner(staff[:4], direction='up')

    r'''
    \new Staff {
        \set stemLeftBeamCount = #0
        \set stemRightBeamCount = #2
        c'16 ^ [
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #2
        e'16 ]
        r16
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #0
        f'16 ^ [ ]
        g'2
    }
    '''

    assert staff.format == "\\new Staff {\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #2\n\tc'16 ^ [\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #2\n\te'16 ]\n\tr16\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #0\n\tf'16 ^ [ ]\n\tg'2\n}"


def test_ComplexBeamSpanner_direction_02():

    staff = Staff("c'16 e'16 r16 f'16 g'2")
    spannertools.ComplexBeamSpanner(staff[:4], direction='_')

    r'''
    \new Staff {
        \set stemLeftBeamCount = #0
        \set stemRightBeamCount = #2
        c'16 _ [
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #2
        e'16 ]
        r16
        \set stemLeftBeamCount = #2
        \set stemRightBeamCount = #0
        f'16 _ [ ]
        g'2
    }
    '''

    assert staff.format == "\\new Staff {\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #2\n\tc'16 _ [\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #2\n\te'16 ]\n\tr16\n\t\\set stemLeftBeamCount = #2\n\t\\set stemRightBeamCount = #0\n\tf'16 _ [ ]\n\tg'2\n}"

