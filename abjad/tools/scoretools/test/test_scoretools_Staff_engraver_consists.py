# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Staff_engraver_consists_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff.consists_commands.append('Horizontal_bracket_engraver')
    staff.consists_commands.append('Instrument_name_engraver')

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

    assert abjad.inspect(staff).is_well_formed()
    assert format(staff) == abjad.String.normalize(
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
