# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_multiplied_quarter_notes_01():

    multipliers = [(1, 4), (1, 5), (1, 6), (1, 7)]
    notes = scoretools.make_multiplied_quarter_notes([0], multipliers)
    staff = Staff(notes)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'4 * 1
            c'4 * 4/5
            c'4 * 2/3
            c'4 * 4/7
        }
        '''
        )

    assert inspect_(staff).is_well_formed()
