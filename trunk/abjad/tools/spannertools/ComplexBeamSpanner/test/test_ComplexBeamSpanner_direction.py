# -*- encoding: utf-8 -*-
from abjad import *


def test_ComplexBeamSpanner_direction_01():

    staff = Staff("c'16 e'16 r16 f'16 g'2")
    spannertools.ComplexBeamSpanner(staff[:4], direction=Up)

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

    assert testtools.compare(
        staff.lilypond_format,
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
        )


def test_ComplexBeamSpanner_direction_02():

    staff = Staff("c'16 e'16 r16 f'16 g'2")
    spannertools.ComplexBeamSpanner(staff[:4], direction=Down)

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

    assert testtools.compare(
        staff.lilypond_format,
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
        )
