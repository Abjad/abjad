# -*- encoding: utf-8 -*-
from abjad import *


def test_notetools_make_notes_with_multiplied_durations_01():

    notes = notetools.make_notes_with_multiplied_durations(
        0, Duration(1, 4), [(1, 2), (1, 3), (1, 4), (1, 5)])
    staff = Staff(notes)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'4 * 2
            c'4 * 4/3
            c'4 * 1
            c'4 * 4/5
        }
        '''
        )
