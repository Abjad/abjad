# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Staff_engraver_removals_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    staff.remove_commands.append('Time_signature_engraver')
    staff.remove_commands.append('Bar_number_engraver')

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff \with {
            \remove Time_signature_engraver
            \remove Bar_number_engraver
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
