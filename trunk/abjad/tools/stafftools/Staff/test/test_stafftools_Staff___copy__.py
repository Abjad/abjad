# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_stafftools_Staff___copy___01():
    r'''Staves (shallow) copy grob overrides and context settings but not musical content.
    '''

    staff_1 = Staff("c'8 d'8 e'8 f'8")
    staff_1.override.note_head.color = 'red'
    staff_1.set.tuplet_full_length = True


    r'''
    \new Staff \with {
        \override NoteHead #'color = #red
        tupletFullLength = ##t
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    staff_2 = copy.copy(staff_1)

    r'''
    \new Staff \with {
        \override NoteHead #'color = #red
        tupletFullLength = ##t
    } {
    }
    '''

    assert testtools.compare(
        staff_2,
        r'''
        \new Staff \with {
            \override NoteHead #'color = #red
            tupletFullLength = ##t
        } {
        }
        '''
        )
