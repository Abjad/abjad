# -*- encoding: utf-8 -*-
import copy
from abjad import *


def test_scoretools_FixedDurationTuplet___copy___01():

    tuplet_1 = scoretools.FixedDurationTuplet((2, 8), "c'8 d'8 e'8")
    tuplet_1.override.note_head.color = 'red'

    assert testtools.compare(
        tuplet_1,
        r'''
        \override NoteHead #'color = #red
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \revert NoteHead #'color
        '''
        )

    tuplet_2 = copy.copy(tuplet_1)

    assert tuplet_2.target_duration == tuplet_1.target_duration
