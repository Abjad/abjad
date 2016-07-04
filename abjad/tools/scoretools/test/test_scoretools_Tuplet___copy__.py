# -*- coding: utf-8 -*-
import copy
from abjad import *


def test_scoretools_Tuplet___copy___01():

    tuplet_1 = Tuplet((2, 3), "c'8 d'8 e'8")
    override(tuplet_1).note_head.color = 'red'

    assert format(tuplet_1) == stringtools.normalize(
        r'''
        \override NoteHead.color = #red
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \revert NoteHead.color
        '''
        )

    tuplet_2 = copy.copy(tuplet_1)

    assert format(tuplet_2) == stringtools.normalize(
        r'''
        \override NoteHead.color = #red
        \times 2/3 {
        }
        \revert NoteHead.color
        '''
        )

    assert not len(tuplet_2)