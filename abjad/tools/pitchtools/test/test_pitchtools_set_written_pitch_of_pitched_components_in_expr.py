# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_set_written_pitch_of_pitched_components_in_expr_01():

    staff = Staff("c' d' e' f'")

    r'''
    \new Staff {
        c'4
        d'4
        e'4
        f'4
    }
    '''

    pitchtools.set_written_pitch_of_pitched_components_in_expr(staff)

    r'''
    \new Staff {
        c'4
        c'4
        c'4
        c'4
    }
    '''

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'4
            c'4
            c'4
            c'4
        }
        '''
        )
