# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_LilyPondCommand_format_slot_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    command = indicatortools.LilyPondCommand('break', 'closing')
    attach(command, staff[0])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()
