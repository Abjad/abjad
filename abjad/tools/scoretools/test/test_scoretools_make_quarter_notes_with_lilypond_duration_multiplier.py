# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_make_quarter_notes_with_lilypond_duration_multiplier_01():

    multipliers = [(1, 4), (1, 5), (1, 6), (1, 7)]
    notes = scoretools.make_quarter_notes_with_lilypond_duration_multiplier([0], multipliers)
    staff = Staff(notes)

    r'''
    \new Staff {
        c'4 * 1
        c'4 * 4/5
        c'4 * 2/3
        c'4 * 4/7
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'4 * 1
            c'4 * 4/5
            c'4 * 2/3
            c'4 * 4/7
        }
        '''
        )
