# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondCommandMark_format_slot_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    marktools.LilyPondCommandMark('break', 'closing')(staff[0])

    r'''
    \new Staff {
        c'8
        \break
        d'8
        e'8
        f'8
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            \break
            d'8
            e'8
            f'8
        }
        '''
        )
