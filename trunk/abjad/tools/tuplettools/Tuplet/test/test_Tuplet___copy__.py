# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_Tuplet___copy___01():


    tuplet_1 = Tuplet((2, 3), "c'8 d'8 e'8")
    tuplet_1.override.note_head.color = 'red'

    r'''
    \override NoteHead #'color = #red
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    \revert NoteHead #'color
    '''

    tuplet_2 = copy.copy(tuplet_1)


    r'''
    \override NoteHead #'color = #red
    \times 2/3 {
    }
    \revert NoteHead #'color
    '''

    assert testtools.compare(
        tuplet_2.lilypond_format,
        r'''
        \override NoteHead #'color = #red
        \times 2/3 {
        }
        \revert NoteHead #'color
        '''
        )
