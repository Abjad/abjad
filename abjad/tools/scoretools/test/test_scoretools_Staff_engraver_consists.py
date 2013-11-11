# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Staff_engraver_consists_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.engraver_consists.append('Horizontal_bracket_engraver')
    staff.engraver_consists.append('Instrument_name_engraver')

    r'''
    \new Staff \with {
        \consists Horizontal_bracket_engraver
        \consists Instrument_name_engraver
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert inspect(staff).is_well_formed()
    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff \with {
            \consists Horizontal_bracket_engraver
            \consists Instrument_name_engraver
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
