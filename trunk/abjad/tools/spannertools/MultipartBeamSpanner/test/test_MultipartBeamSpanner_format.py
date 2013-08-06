# -*- encoding: utf-8 -*-
from abjad import *


def test_MultipartBeamSpanner_format_01():

    staff = Staff("c'8 d'8 r8 e'8 f'8 g'4")
    spannertools.MultipartBeamSpanner(staff)

    r'''
    \new Staff {
        c'8 [
        d'8 ]
        r8
        e'8 [
        f'8 ]
        g'4
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 [
            d'8 ]
            r8
            e'8 [
            f'8 ]
            g'4
        }
        '''
        )
